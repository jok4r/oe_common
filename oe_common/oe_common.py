import math
import shutil
import string
import random
import time
import errno
import os
import re
import datetime
import pathlib
import hashlib
import subprocess
import requests
import json


def fix_block_encoding_errors(block):
    fixed = []
    for line in block.splitlines(True):
        try:
            fixed.append(line.decode('utf-8'))
        except UnicodeDecodeError:
            fixed.append(fix_unicode_string(line).decode('utf-8'))
    return ''.join(fixed)


def fix_file_encoding_errors(*file):
    files = [file]
    if isinstance(file, tuple):
        files = file

    for wf in files:
        with open(wf, 'rb') as f:
            cnt = 0
            wa = []
            for line in f:
                try:
                    line.decode('utf-8')
                except UnicodeDecodeError as e:
                    r_line = fix_unicode_string(line)
                    wa.append([line, r_line])
                cnt += 1

            f.seek(0)
            b = f.read()
            # b = re.sub(b"\xd1 ", b'\x3f', b)
            for w in wa:
                b = b.replace(w[0], w[1])

        with open(wf, 'wb') as f:
            f.write(b)


def fix_unicode_string(line):
    if not isinstance(line, bytes):
        raise TypeError('line is not bytes')
    tl = line
    # print('line: %s' % line)
    rb = []
    while len(tl) > 0:
        # print('byte: %s' % tl[0:1])
        dec, ct = _decode_byte(tl[0:4])
        rb.append(dec)
        tl = tl[ct:]
    # print('bytes: %s' % ''.join(rb))
    return b''.join(rb)


def _decode_byte(bt, bytes_count=1):
    if bytes_count > len(bt):
        return b'?', bytes_count
    else:
        try:
            bt[0:bytes_count].decode('utf-8')
            return bt[0:bytes_count], bytes_count
        except UnicodeDecodeError:
            return _decode_byte(bt, bytes_count+1)


def convert_size(size_bytes, prefix='B'):
    if size_bytes == 0:
       return "0B"
    size_name = [f'{i}{prefix}' for i in ("", "K", "M", "G", "T", "P", "E", "Z", "Y")]
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return "%s %s" % (s, size_name[i])


def get_rnd_string(length=20, complexity=None):
    if complexity and length < 8:
        print('[%s] Warning! Length with complexity cannot be lower, than 8 (fixed to 8)' % os.path.basename(__file__).split('.')[0])
        length = 8
    letters = string.ascii_letters + string.digits
    password = ''.join(random.choice(letters) for i in range(length))
    if complexity:
        if complexity == 1:
            #  at least one upper case, lower case and digit symbol
            if not re.match(r'^(?=.*[A-Z].*[A-Z])(?=.*[0-9].*[0-9])(?=.*[a-z].*[a-z].*[a-z]).{%s}$' % len(password), password):
                print(f'password "{password} is too simple, generating new..."')
                return get_rnd_string(length, complexity)
            return password

    else:
        return password


def generate_password(length=20, complexity=None):
    return get_rnd_string(length, complexity)


def create_dir(*filename, is_file=True):
    filenames = [filename]
    if isinstance(filename, tuple):
        filenames = filename

    for f in filenames:
        if is_file:
            d = os.path.dirname(f)
        else:
            d = f
        if not os.path.exists(d):
            os.makedirs(d, exist_ok=True)


def check_create_dir(*filename):
    create_dir(*filename)


def rm(*filename):
    filenames = [filename]
    if isinstance(filename, tuple):
        filenames = filename

    for f in filenames:
        if os.path.isfile(f):
            os.remove(f)
        elif os.path.isdir(f):
            shutil.rmtree(f, ignore_errors=True)


def replace_string_in_file(path, regex, replaced, flags=0):
    if os.path.isfile(path):
        with open(path, 'r+') as f:
            file = f.read()
            f.seek(0)
            f.truncate()
            file = re.sub(regex, replaced, file, flags=flags)
            f.write(file)
        return True
    else:
        print("Warning! %s not found" % path)
        return False


start_time = 0


def get_directory_size(path, lvl=0, max_lvl=100, time_limit=5, verbose=False):
    global start_time
    total = 0

    if lvl == 0:
        start_time = time.perf_counter()

    lvl += 1
    if not os.path.isdir(path):
        return 0
    with os.scandir(path) as it:
        for entry in it:
            exec_time = time.perf_counter() - start_time
            if exec_time > time_limit:
                print('time limit reached (%ss)' % time_limit)
                return total
            try:
                if entry.is_file() or entry.is_symlink():
                    size = entry.stat(follow_symlinks=False).st_size

                    if entry.stat().st_nlink > 1 and not entry.is_symlink():
                        if verbose:
                            print('nlink: %s %s delim: %s/%s' % (entry.stat().st_nlink, entry.name, size, entry.stat().st_nlink))
                        size = size / entry.stat().st_nlink
                    if verbose:
                        print('%s : %s' % (entry.name, size))

                    total += size
                elif lvl >= max_lvl:
                    if verbose:
                        print('lvl break (%s), total: %s, path: %s' % (lvl, total, path))
                    return total
                elif entry.is_dir():
                    if verbose:
                        print('opening dir: %s' % entry.name)
                    total += get_directory_size(entry.path, lvl=lvl)
            except (OSError, FileNotFoundError):
                pass
    # print('lvl: %s' % lvl)
    return total


def get_filename_and_extension(path):
    return os.path.splitext(os.path.basename(path))


def get_disk_stats():
    if os.name == 'posix':
        with open('/proc/diskstats') as f:
            stats_file = f.readlines()
            stats = {}
            for disk_stats_text in stats_file:
                sp = disk_stats_text.split()
                device_name = sp[2]
                if re.match(r'sd.$|nvme\dn\d$', device_name):
                    stats[device_name] = {
                        'major number': int(sp[0]),
                        'minor number': int(sp[1]),
                        'device name': sp[2],
                        'reads completed successfully': int(sp[3]),
                        'reads merged': int(sp[4]),
                        'sectors read': int(sp[5]),
                        'time spent reading (ms)': int(sp[6]),
                        'writes completed': int(sp[7]),
                        'writes merged': int(sp[8]),
                        'sectors written': int(sp[9]),
                        'time spent writing (ms)': int(sp[10]),  # time spent writing (ms)
                        'I/Os currently in progress': int(sp[11]),  # I/Os currently in progress
                        'tot_ticks': int(sp[12]),  # time spent doing I/Os (ms)
                        'weighted time spent doing I/Os (ms)': int(sp[13]),
                        'discards completed successfully': int(sp[14]) if len(sp) > 14 else 0,
                        'discards merged': int(sp[15]) if len(sp) > 15 else 0,
                        'sectors discarded': int(sp[16]) if len(sp) > 16 else 0,
                        'time spent discarding': int(sp[17]) if len(sp) > 17 else 0,
                        'flush requests completed successfully': int(sp[18]) if len(sp) > 18 else 0,
                        'time spent flushing': int(sp[19]) if len(sp) > 19 else 0,
                    }
            return stats
    else:
        raise RuntimeError('get_disk_stats can be run only on Linux')


def get_disk_utilization(prev_ticks, ticks, itv):
    # prev_ticks - previous get_disk_stats()['tot_ticks']
    # ticks - current get_disk_stats()['tot_ticks']
    # itv - time between previous and current calls of get_disk_stats
    util = (float(ticks - prev_ticks)) / itv * 100
    util_percent = util / 10.0 / 100.0
    if util_percent > 100.0:
        util_percent = 100.0
    return util_percent


def get_array_hash(d):
    h = hashlib.sha1()
    if isinstance(d, list):
        for v in d:
            h.update(str(v).encode())
    elif isinstance(d, dict):
        for k, v in d.items():
            h.update(str(k).encode())
            h.update(str(v).encode())
    else:
        raise RuntimeError("Unsupported array type: %s" % type(d))
    return h.hexdigest()


def chown(path, username, group=None, recursive=True):
    if os.path.exists(path):
        if not group:
            group = username
        if recursive:
            r_str = '-R '
        else:
            r_str = ''
        os.system('chown {0}{1}:{2} "{3}"'.format(r_str, username, group, path))


default_interfaces = ['enp', 'eth']


def get_interface(interfaces=None):
    if not interfaces:
        interfaces = default_interfaces
    for inet in os.listdir('/sys/class/net/'):
        for interface in interfaces:
            if interface in inet:
                return inet
    return False


def get_ip_addresses(interface=None):
    if os.name == 'posix':
        return _get_ip_addresses_linux(interface)
    elif os.name == 'nt':
        return _get_ip_addresses_windows()
    else:
        raise RuntimeError("Unsupported OS")


def get_external_ip():
    group = json.loads(requests.get('http://jsonip.com/').content.decode())
    return group['ip']


def _get_ip_addresses_linux(interface=None):
    if not interface:
        interface = get_interface()
    output = subprocess.getoutput('ip address show %s' % interface)
    ips_list = re.findall(r'inet (\d+\.\d+\.\d+\.\d+)', output)

    return ips_list


def _get_ip_addresses_windows():
    output = subprocess.getoutput('ipconfig')
    ips_list = re.findall(r'IPv4 Address.*: (\d+\.\d+\.\d+\.\d+)', output)

    return ips_list


class Logger:
    def __init__(self, to_console=True, file=None):
        self._to_console = to_console
        if isinstance(file, str):
            if file[0] != '/':
                full_path = os.path.join(pathlib.Path().absolute(), file)
            else:
                full_path = file
            self._file = full_path
            check_create_dir(self._file)
            pathlib.Path(self._file).touch()
        else:
            self._file = None

    def log(self, *data):
        now_date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        data_string = ' '.join([str(a) for a in data])
        log_text = '%s %s' % (now_date, data_string)
        if self._to_console:
            print(log_text)
        if self._file:
            with open(self._file, 'a') as f:
                f.write(log_text + '\n')


class DinConsole:
    def __init__(self):
        self.prev_len = 0
        self.prev_str = ''

    def clear(self):
        print(' ' * self.prev_len, end="\r")

    def stay(self):
        self.clear()
        print(self.prev_str)

    def update(self, p_str=''):
        self.clear()
        self.prev_str = p_str
        print(p_str, end="\r")
        self.prev_len = len(p_str)


class SpeedChecker:
    def __init__(self, name, bts):
        self.speed = 0
        self._name = name
        self._c_time = time.perf_counter()
        self._ar_len = 10
        self._speeds_ar = [0] * self._ar_len
        self.bts = bts
        self.every = 1000
        self.counter = 0

    def _update_speeds(self, speed):
        self._speeds_ar.append(speed)
        self._speeds_ar.pop(0)

    def get_speed(self):
        self.counter += 1
        if self.counter >= self.every:
            self.counter = 0
            new_time = time.perf_counter()
            diff = new_time - self._c_time
            self._c_time = new_time
            speed = self.bts / diff * self.every * 8  # bits per second from bytes
            self._update_speeds(speed)
        return convert_size(sum(self._speeds_ar) / self._ar_len, prefix=self._name)
