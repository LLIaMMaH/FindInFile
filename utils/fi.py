import os
from dataclasses import dataclass
from datetime import datetime


@dataclass
class FindInformation:
    all_files: int = 0
    all_find_line: int = 0
    search_string: str = ''
    report_name: str = datetime.now().strftime('%Y-%m-%d_%H%M%S.txt')
    directory: str = os.getcwd()
    file_type: str = '*.*'
    exclude_type: str = ''
    write_to_file: bool = True
    escape_path: bool = False
    markdown_line: bool = False
    markdown_language: str = ''
    print_count_string_in_file: bool = True

    @staticmethod
    def get_all_files(more: bool = True) -> str:
        result = ''
        if more:
            result = 'Всего файлов найдено: '
        return result + str(fs.all_files)

    @staticmethod
    def get_search_string(more: bool = True) -> str:
        result = ''
        if more:
            result = 'Поиск текста: '
        return result + fs.search_string

    @staticmethod
    def get_report_name(more: bool = True) -> str:
        result = ''
        if more:
            result = 'Имя файла: '
        return result + fs.report_name

    @staticmethod
    def get_directory(more: bool = True) -> str:
        result = ''
        if more:
            result = 'Начальная папка: '
        return result + fs.directory

    @staticmethod
    def get_file_type(more: bool = True) -> str:
        result = ''
        if more:
            result = 'Тип файлов: '
        return result + fs.file_type

    @staticmethod
    def get_exclude_type(more: bool = True) -> str:
        result = ''
        if more:
            result = 'Исключить типы файлов: '
        return result + fs.exclude_type
