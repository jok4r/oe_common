# OE Common

Simple module with some functions such as generate password (get_random_string), fix unicode strings, size converter, dynamic console, read/write speed checker, etc.
## Prerequisites

	- Python3.7 or newer

## Installion
$ python3 -m pip install oe_common<br /><br />
**OR**<br /><br />
$ python3 -m pip install git+https://github.com/jok4r/oe_common.git

## Usage / Eng

### Functions

**fix_block_encoding_errors(text)** - Decode block of text from bytes. In some cases, **.decode()** can raise exception (bad encoding, etc.). This function resolves the problem. Unreaded symbols will be replaced by "?" symbol.

**fix_unicode_string(line)** - Its the same function as above, but do this only for one line.

**convert_size(size_bytes, prefix='B')** - Convert input value to human readable format (KB, MB, GB, etc.).

**get_rnd_string(length=20, complexity=None)** - Generates random string (password) with given size. If *complexity* is *True*, password will be strength, with 2 letters uppercase, 3 letters lowercase and 2 digits (minimum).

**generate_password** - Alias of function above.

**check_create_dir(\*filename)** - Almost the same as *os.makedirs*, but input value is full path to filename. Can specify multiple values: *check_create_dir(file1, file2)*

**replace_string_in_file(path, regex, replaced)** - Search and replace string in file. Example: *replace_string_in_file("file.txt", r'string', r'replaced')*

**get_directory_size(path)** - Get size of specified directory. This function uses C++ module for work faster. If directory is not exists, not raises an exeption, just return zero size.

**get_filename_and_extension(path)** - Get filename and extension of file. Using simple os.path.splitext with basename of path.

**get_disk_stats()** - Reads data from /proc/diskstats and parse it.

**get_disk_utilization(prev_tot_ticks, tot_ticks, itv)** - Count disk utilization (0-100). Ticks is "tot_ticks" from function above. Itv is time between previous and current ticks.

**get_array_hash(array)** - Get hash from array (list or dict). Currently hash func is SHA-1.

**rm(\*filename)** - Remove file or directory without errors if file is not exist (like rm -rf). Can specify multiple values: *rm(file1, dir1)*

**chown(path, username, group=None, recursive=True)** - Change owner of directory/file. If *group* is not assigned, it will have same value as *username*

**get_interface(interfaces=None)** - Get default network interface. If *interfaces* arg is None (default), will be used default array of interfaces: ['enp', 'eth']

**get_ip_addresses(interface=None)** - Get all ip addresses on external interface (if interface is not specified, will be select default interface by function above)

**get_external_ip()** - Get external ip

### Classes

#### Logger
Simple logger, can write output to console and file. In begin of log string, adds current datetime. Argument *file* - path to log file (will be created if not exists).

* *Logger(to_console=True, file=None)*
    * *log(\*data)* - Write to log. Can input multiple values: logger.log('foo', 'bar')

#### DinConsole / Dynamic Console
With this object, you can print text to console, then update it. Can be used to print progress bar, or another data, which can be updated (files copy, etc.)

* *DinConsole()*
    * *update(text)* - Update text in console.
    * *stay()* - Stay text in console. Usually used before printing another data, which not need to be updated.
    * *clear()* - Clear the current string in console.

#### Speed Checker
Check read/write speed.

* *SpeedChecker(name, bts)*
    * get_speed() - Every time when call this method, class update current read/write speed and return it. **Example:** we reading file by part, block size is 1024. In loop we can add get_speed() method, to run every cycle.

## Usage / Rus

### Функции

**fix_block_encoding_errors(text)** - В некоторых случаях обычный **.decode()** может выдать исключение, из-за каких-то некорректных символов и т.д. Данная функция устраняет эту проблему. В случае нечитаемых символов, выдает вместо них знаки вопроса.

**fix_unicode_string(line)** - То же самое что функция выше, но делает это только для одной строки. Если сюда подать целый блок текста, то обработка займет больше времени, чем у функции выше.

**convert_size(size_bytes, prefix='B')** - Конвертирует входящее значение в более удобно читаемое. Например оно конвертирует 1000000 Байт в 976 Кбайт. Если число еще больше, то будут мегабайты и т.д.

**get_rnd_string(length=20, complexity=None)** - Генерирует случайную строку (пароль) заданной длины. В случае если установить **complexity=True**, будет генерировать более сложный пароль, который обязательно должен включать 2 буквы верхнего регистра, 3 нижнего и 2 цифры.

**generate_password** - То же самое что функция выше, отличается только название (для удобства при написании скриптов).

**check_create_dir(\*filename)** - Функционал аналогичен *os.makedirs*, но на вход мы подаем путь до создаваемого файла, и путь до него будет создан. На вход можно подавать сразу несколько значений: *check_create_dir(file1, file2)*

**replace_string_in_file(path, regex, replaced)** - Поиск и замена строки в файле. Пример: *replace_string_in_file("file.txt", r'string', r'replaced')*

**get_directory_size(path)** - Получить размер директории (папки). Выполняется с помощью модуля на C++ для ускорения работы. В случае если папка не существует, не выдает исключение, выдает нулевой размер.

**get_filename_and_extension(path)** - Получить имя и расширение файла. Используется os.path.splitext и basename от path.

**get_disk_stats()** - Читает и парсит /proc/diskstats.

**get_disk_utilization(prev_tot_ticks, tot_ticks, itv)** - Считает утилизацию диска (0-100). Ticks - это "tot_ticks" из функции выше. Itv - это время между замерами (вызовами get_disk_stats).

**get_array_hash(array)** - Получает хэш из массива (list или dict). В данный момент используется алгоритм SHA-1.

**rm(\*filename)** - Удаляет файл или директорию (рекурсивно), не выдавая каких-либо ошибок и другой информации в консоль (аналог rm -rf). На вход можно подавать сразу несколько значений: *rm(file1, dir1)*

**chown(path, username, group=None, recursive=True)** - Установить права на папку/файл. Если не указать *group*, то группа будет иметь то же значение, что и username.

**get_interface(interfaces=None)** - Получить интерфейс по умолчанию. Если аргумент *interfaces* не указан (по умолчанию), будет использован стандартный массив интерфейсов: *['enp', 'eth']*

**get_ip_addresses(interface=None)** - Получить все ip адреса интерфейса (если не указан, будет выбран стандартный интерфейс с помощью функции выше).

**get_external_ip()** - Получить внешний ip адрес.

### Классы

#### Logger
Простой логгер, может писать вывод в консоль и в файл. В начале строки лога пишет текущую дату и время. Аргумент *file* - путь до файла, в который необходимо писать лог.

* *Logger(to_console=True, file=None)*
    * *log(\*data)* - Записать лог. На вход можно подавать сразу несколько значений: logger.log('foo', 'bar')

#### DinConsole / Dynamic Console
Создает возможность вывода в консоль строки, с возможностью обновления этой строки. Таким образом можно выводить прогресс в процентах и прочее, чтобы не спамить кучу текста в консоль.

* *DinConsole()*
    * *update(text)* - Обновить текст в консоли.
    * *stay()* - Оставить текст в консоли, чтобы он не стирался. Обычно используется в конце работы класса.
    * *clear()* - Очистить консоль.

#### Speed Checker
Позволяет замерить скорость чтения/записи.

* *SpeedChecker(name, bts)*
    * get_speed() - Каждый раз вызывая этот метод, обновляется скорость передачи и возвращает текущую скорость.