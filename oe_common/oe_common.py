import math
import string
import random
import time
import errno
import os
import re


def fix_block_encoding_errors(block):
    fixed = []
    for line in block.splitlines(True):
        try:
            fixed.append(line.decode('utf-8'))
        except UnicodeDecodeError:
            fixed.append(fix_unicode_string(line).decode('utf-8'))
    return ''.join(fixed)


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


def check_create_dir(*filename):
    filenames = [filename]
    if isinstance(filename, tuple):
        filenames = filename

    for f in filenames:
        if not os.path.exists(os.path.dirname(f)):
            try:
                os.makedirs(os.path.dirname(f))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise


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
