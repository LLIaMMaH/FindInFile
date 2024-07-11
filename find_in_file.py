import os
import re
from pathlib import Path
from typing import List, Union

from utils.fi import FindInformation


def get_start_directory(home: str = None) -> Union[bool, str]:
    """
    Если директория не указана, то берём текущую.
    Если указанная директория не найдена, то берём текущую.

    :param home: str - Проверка директории
    """
    if home is None:
        return os.getcwd()
    if os.path.isdir(home):
        return home
    else:
        print('Указанная вами папка не найдена.')
        return False


def get_directory_list(home: str, exclude_directories: list = []) -> list:
    directories = set()
    for root, dirs, _ in os.walk(home):
        # Исключаем директории, которые не нужно обрабатывать
        dirs[:] = [d for d in dirs if not any(os.path.join(root, d).endswith(exdir) for exdir in exclude_directories)]
        for directory in dirs:
            directories.add(os.path.join(root, directory))
    return list(directories)


def printing(text: str, write_to_file: bool, file_handler):
    if write_to_file and file_handler:
        file_handler.write(text + '\n')
    else:
        print(text)


def find_in_files(fs: FindInformation, directories: List[str], file_type: list = [], exclude_type: list = []):
    line_counter = 0
    files_count = 0
    all_files_count = 0
    results = []
    processed_files = set()  # Множество для хранения уникальных файлов

    for directory in directories:
        for root, _, filenames in os.walk(directory):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                if file_path in processed_files:
                    continue
                if any(file_path.lower().endswith(ext) for ext in exclude_type):
                    continue
                if not file_type or any(file_path.lower().endswith(ft) for ft in file_type):
                    processed_files.add(file_path)
                    try:
                        all_files_count += 1
                        with open(file_path, 'r', encoding='utf-8') as cur_file:
                            local_count = 0
                            find_file = 0
                            open_md_tag = True
                            for line in cur_file:
                                local_count += 1
                                match = re.search(fs.search_string, line, re.IGNORECASE)
                                if match:
                                    if fs.markdown_line and open_md_tag:
                                        open_md_tag = False
                                        results.append('```' + fs.markdown_language)
                                    fnd_srt = f'{local_count}\t' + line.strip()
                                    results.append(fnd_srt)
                                    find_file += 1
                            if find_file > 0:
                                if fs.markdown_line and not open_md_tag:
                                    results.append('```')
                                files_count += 1
                                inf_str = f'{Path(file_path).name} - {local_count} строки\n' if fs.print_count_string_in_file else f'{Path(file_path).name}\n'
                                if fs.escape_path:
                                    inf_str = inf_str.replace('\\', '\\\\')
                                results.append(inf_str)
                                line_counter += local_count
                    except PermissionError:
                        print(f"Ошибка при обработке файла {file_path}: Permission denied")
                    except Exception as e:
                        print(f"Ошибка при обработке файла {file_path}: {e}")
                        continue

    if fs.write_to_file:
        with open(fs.report_name, 'w', encoding='utf-8') as file_handler:
            for line in results:
                printing(line, fs.write_to_file, file_handler)
            printing('=====================================', fs.write_to_file, file_handler)
            printing(f'Всего файлов - {files_count}', fs.write_to_file, file_handler)
            printing(f'Всего строк - {line_counter}', fs.write_to_file, file_handler)
            printing(f'Всего файлов обработано - {all_files_count}', fs.write_to_file, file_handler)
    else:
        for line in results:
            printing(line, fs.write_to_file, None)
        printing('=====================================', fs.write_to_file, None)
        printing(f'Всего файлов - {files_count}', fs.write_to_file, None)
        printing(f'Всего строк - {line_counter}', fs.write_to_file, None)
        printing(f'Всего файлов обработано - {all_files_count}', fs.write_to_file, None)


# Настройка параметров
fs = FindInformation(
    # report_name='result.txt',
    write_to_file=True,
    search_string='что будем искать',
    markdown_line=True,
    markdown_language='php',
    print_count_string_in_file=True,
    escape_path=True
)

# Выясним начальную директорию
# ask_the_way = input('Укажите пожалуйста папку, с которой нужно начинать поиск: ')
ask_the_way = 'D:/work/projects/xxx/public_html/'
if ask_the_way == '':
    ask_the_way = None
start_directory = get_start_directory(ask_the_way)
if not start_directory:
    print("Начальная директория не найдена. Завершаем работу скрипта.")
    exit(1)

# Выясним, какие директории исключать при поиске
exclude_directories = ['venv', '__pycache__']

# Подготовим список директорий
directories = get_directory_list(start_directory, exclude_directories)
directories.append(start_directory)  # Добавляем начальную директорию в список директорий для обхода

# В каких файлах смотрим, а какие исключаем
# file_type = ['.php','.inc']
file_type = []
exclude_type = ['.txt', '.gif', '.png', '.jpg', '.ico', '.zip', '.eot', '.ttf', '.woff', '.woff2']

# Запуск поиска по файлам
find_in_files(fs, directories, file_type, exclude_type)

