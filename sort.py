import os
import sys
import shutil
from datetime import datetime


def get_dir_name():
    work_dir = ''
    args = sys.argv
    if len(args) == 1:
        work_dir = input('Enter path to directory: ')
    else:
        work_dir = args[1]
    while True:
        if not os.path.exists(work_dir):
            if work_dir:
                print(f'{work_dir} is not exist')
            work_dir = input('Enter path to directory: ')
        else:
            if os.path.isdir(work_dir):
                break
            else:
                print(f'{work_dir} is not a directory')
                work_dir = ''
    return work_dir


def read_dir(namedir):
    return os.listdir(namedir)


def is_free_dir(namedir):
    global name_folder
    lists_free_dir = (
        os.path.join(name_folder, 'Images'),
        os.path.join(name_folder, 'Video'),
        os.path.join(name_folder, 'Documents'),
        os.path.join(name_folder, 'Audio'),
        os.path.join(name_folder, 'Archives'),
        os.path.join(name_folder, 'PSD')

    )
    return namedir in lists_free_dir


def check_clear_dir(namedir):
    lists = os.listdir(namedir)
    if not lists and not is_free_dir(namedir):
        os.rmdir(namedir)
    else:
        for el in lists:
            path_el = os.path.join(namedir, el)
            if os.path.isdir(path_el):
                check_clear_dir(path_el)


def check_file_type(file):
    file_name_arr = file.split('.')
    file_ext = ''
    if len(file_name_arr) > 1:
        file_ext = file_name_arr[-1]
    if not file_ext:
        return None
    else:
        if file_ext in ('jpeg', 'png', 'jpg', 'svg'):
            return 'Images'
        elif file_ext in ('avi', 'mp4', 'mov', 'mkv'):
            return 'Video'
        elif file_ext in ('doc', 'docx', 'txt', 'pdf', 'xls', 'xlsx', 'pptx'):
            return 'Documents'
        elif file_ext in ('mp3', 'ogg', 'mov', 'amr'):
            return 'Audio'
        elif file_ext in ('zip', 'gz', 'tar'):
            return 'Archives'
        elif file_ext in ('psd', 'psb'):
            return 'PSD'
        else:
            return None


def normalize(file, is_copy=False):
    alph = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'y',
            'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h',
            'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch', 'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya', 'і': 'i',  'є': 'e', 'ї': 'i', 'А': 'A',
            'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E', 'Ж': 'Zh', 'З': 'Z', 'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L',
            'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'H', 'Ц': 'Ts', 'Ч': 'Ch',
            'Ш': 'Sh', 'Щ': 'Sch', 'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya', 'І': 'I',  'Є': 'E',  'Ї': 'I'}

    lists = file.split('.')
    name_file = '.'.join(lists[0:-1])
    new_name = ''
    for el in name_file:
        if el in alph:
            new_name += alph[el]
        elif (ord('A') <= ord(el) <= ord('Z')) or (ord('a') <= ord(el) <= ord('z')) or el.isdigit():
            new_name += el
        else:
            new_name += '_'
    if is_copy:
        new_name += f'_(copy_{datetime.now().microsecond})'

    return new_name + '.' + lists[-1]


def rename_file(folder_to, folder_from, file):
    global name_folder
    path_to = os.path.join(name_folder, folder_to)
    if not os.path.exists(path_to):
        os.makedirs(path_to)
    if folder_to != 'Archives':
        try:
            os.rename(os.path.join(folder_from, file),
                      os.path.join(path_to, normalize(file)))
        except FileExistsError:
            print(
                f'File {file} is already exist.')
            while True:
                os.rename(os.path.join(folder_from, file),
                          os.path.join(path_to, normalize(file, True)))
                continue

    else:
        f = normalize(file).split('.')
        try:
            shutil.unpack_archive(os.path.join(
                folder_from, file), os.path.join(path_to, f[0]), f[1])
        except shutil.ReadError:
            print(f"Archive {os.path.join(folder_from, file)} can't be unpack")
        else:
            os.remove(os.path.join(folder_from, file))


def sorting_dir(namedir):
    lists = read_dir(namedir)
    for el in lists:
        path_file = os.path.join(namedir, el)
        if is_free_dir(path_file):
            continue
        if os.path.isdir(path_file):
            sorting_dir(path_file)
        else:
            folder = check_file_type(el)
            if folder:
                rename_file(folder, namedir, el)


if __name__ == '__main__':

    name_folder = get_dir_name()
    sorting_dir(name_folder)
    check_clear_dir(name_folder)
