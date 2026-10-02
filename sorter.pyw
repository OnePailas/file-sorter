import os
import json
import shutil
import time
import pathlib


if os.path.isdir(r'C:\OP_Sorter'):
    if os.path.isdir(r'C:\OP_Sorter\logs'):
        pass

    else:
        os.mkdir(r'C:\OP_Sorter\logs')

else:
    os.mkdir(r'C:\OP_Sorter')
    os.mkdir(r'C:\OP_Sorter\logs')


##### Ведение логов #####
# Проверяется наличие файла "logs.txt". Если файл существует, то его имя заменяется на новое

# [2026-01-01 00:00:00] [INFO ]
# [2026-01-01 00:00:00] [WARN ]
# [2026-01-01 00:00:00] [ERROR]

if os.path.exists(r'C:\OP_Sorter\logs\logs.txt'):
    os.chdir(r'C:\OP_Sorter\logs')
    os.rename('logs.txt', f'{time.strftime('%Y-%m-%d %H-%M-%S')}-logs.txt')
    logs_file = open('logs.txt', 'w')

else:
    os.chdir(r'C:\OP_Sorter\logs')
    logs_file = open('logs.txt', 'w')


# По умолчанию не существует директорий, которые нужно сортировать
exported_directories = []
# По умолчанию не существует путей файлов, которых надо игнорировать
exported_files_ignore = []
# По умолчанию минимальное количество файлов для старта сортировки составляет 13 файлов
imported_minimal_amount = [13]

# Если существует конфиг, то импортируем директории оттуда
if os.path.exists(r'C:\OP_Sorter\config.json'):

    # Открываем конфиг и читаем его
    export_data = open(r'C:\OP_Sorter\config.json', 'r')
    data = json.load(export_data)

    # Импортируем директории для сортировки, пути игнорируемых файлов, минимальное количество файлов для начала сортировки
    exported_directories = list(set(data['directories']))
    exported_files_ignore = list(set(data['ignores']))
    imported_minimal_amount = list(set(data['amount']))[0]

    export_data.close()

else:
    quit


if len(exported_directories) > 0:
    pass

else:
    logs_file.write(f'[{time.strftime('%Y-%m-%d %H:%M:%S')}] [ERROR] Directories were not provided.')
    quit


# Функция для расположения ярлыков в алфавитном порядке (только для рабочего стола, иначе ярлыки будут перемещены в локальную папку сортировщика)
def sort_member_files(directory_sorting):

    if directory_sorting.lower() == str(pathlib.Path.home()).lower() + r'\desktop':

        # Запускаем сортировку ярлыков на рабочем столе, если список для них ненулевой 
        if len(system_files) > 0:

            # Запускается указатель по списку ярлыков
            for x in system_files:

                shutil.move(directory_sorting + rf'\{x}', directory_sorting + r'\Sorter\just_folders')
                
            # Обязательно создаем задержку, чтобы ярлыки не затерялись (если не давать задержку, то почему-то ярлыки просто теряются и все, никакой сортировки не происходит)
            time.sleep(2)

            for x in sorted(system_files):

                shutil.move(directory_sorting + rf'\Sorter\just_folders\{x}', directory_sorting)

        else:

            # Пишем в логи, что список Н был пуст
            logs_file.write(f'[{time.strftime('%Y-%m-%d %H:%M:%S')}] [INFO ] The "system_files" list was empty.' + '\n')
            pass

    else:

        # Запускаем сортировку ярлыков, если список для них ненулевой 
        if len(system_files) > 0:

            # Запускается указатель по списку ярлыков
            for x in system_files:

                # Если получается, то перемещаем файл в папку, предназначенную для него
                try:
                    # Пишем в логи, что был перемещен Н файл
                    logs_file.write(rf'[{time.strftime('%Y-%m-%d %H:%M:%S')}] [INFO ] File {file} moved to {directory_sorting}\Sorter\system_files.' + '\n')
                    shutil.move(directory_sorting + rf'\{x}', directory_sorting + rf'\Sorter\system_files')

                except:
                    # Пишем в логи, что не удалось переместить Н файл
                    logs_file.write(f'[{time.strftime('%Y-%m-%d %H:%M:%S')}] [WARN ] Failed to move the file {x}.' + '\n')
                    pass

    # Пишем в логи, что директория была успешно отсортирована
    logs_file.write(f'[{time.strftime('%Y-%m-%d %H:%M:%S')}] [INFO ] Sorter sorted {directory_sorting}.')

    # Завершаем сортировку
    return True


# Функция для сортировки основных файлов
def sort_owner_files(directory_sorting):

    # Запускается указатель по списку, где хранятся другие списки файлов
    for index_folder, x in enumerate(list_folders_for_Sorted_files):
        
        # Если Н-ый список имеет файлы, то пускаем его в сортировку
        if len(x) > 0:

            # Запускается указатель по Н-ому списку
            for file in x:

                # Если получается, то перемещаем файл в папку, предназначенную для него
                try:
                    # Пишем в логи, что был перемещен Н файл
                    logs_file.write(rf'[{time.strftime('%Y-%m-%d %H:%M:%S')}] [INFO ] File {file} moved to {directory_sorting}\Sorter\{folders_name_for_create[index_folder]}.' + '\n')
                    shutil.move(directory_sorting + rf'\{file}', directory_sorting + rf'\Sorter\{folders_name_for_create[index_folder]}')

                except:
                    # Пишем в логи, что не удалось переместить Н файл
                    logs_file.write(f'[{time.strftime('%Y-%m-%d %H:%M:%S')}] [WARN ] Failed to move the file {file}.' + '\n')
                    pass

        else:

            # Пишем в логи, что список Н был пуст
            logs_file.write(f'[{time.strftime('%Y-%m-%d %H:%M:%S')}] [INFO ] The "{folders_name_for_create[index_folder]}" list was empty.' + '\n')
            pass

    sort_member_files(directory_sorting)


# Функция для проверки наличии папок под различные расширения
def check_member_folders(directory_sorting):

    # Список папок для сортируемых файлов
    listdir_folders_sorted_files = os.listdir(directory_sorting + r'\Sorter')

    # Запускается указатель, который проверяет наличие каждой папки из требуемого списка
    for x in folders_name_for_create:

        # Если папка присутствует, то ее пропускаем и проверяем следующюю
        if x in listdir_folders_sorted_files:
            pass

        else:
            os.mkdir(directory_sorting + rf'\Sorter\{x}')

            # Пишем в логи, что была создана Н папки
            logs_file.write(f'[{time.strftime('%Y-%m-%d %H:%M:%S')}] [INFO] The "{x}" folder was created.' + '\n')

    sort_owner_files(directory_sorting)


# Главная функция. Проверяет на наличие локальных папок для сортировщика
def check_owner_folders(directory_sorting):

    # Проверяет, существует ли основаная локальная папка "Sorter" для файлов в указанном пути
    if os.path.isdir(directory_sorting + r'\Sorter'):
        pass

    else:
        os.mkdir(directory_sorting + r'\Sorter')

    check_member_folders(directory_sorting)



# Запускается указатель по списку директорий, подлежащих сортировке
for point in exported_directories:

    # Получение списка файлов
    list_files = os.listdir(point)

    ignoring = ['Sorter', 'desktop.ini', 'sorter_settings.py', 'sorter.py', 'sorter.pyw']

    for x in ignoring:
        if x in list_files:
            list_files.remove(x)

    # Исключение файлов, которые не подлежат сортировки
    # Обработка игнорируемых файлов начинается, если они указаны пользователем
    if len(exported_files_ignore) > 0:

        # Для начала мы берем путь игнорируемого файла
        for x in exported_files_ignore:

            # Берем название файла из списка всех файлов
            for w in list_files:

                # А после делаем из сортируемой директории и названии файла целый путь и сравниваем его с путем игнорируемого файла
                if (point + rf'\{w}').lower() == x.lower():
                    # Если путь, созданный нами, сравним с путем игнорируемого файла, то файл исключается из списка сортировки
                    # И путь игнорируемого файла заменяется на следующий путь для продолжения проверки 
                    list_files.remove(w)
                    break

                # Если путь, созданый нами, не сравним с путем игнорируемого файла, то файл остается в списке сортировки
                else:
                    # И передается следующий объект для сравнения
                    pass


    # Набор списков для сортировки
    table_files = []            # список таблиц             .xlsx .xls .xlsm .ods .fods .csv
    text_files = []             # список текстовых файлов   .txt .docx .doc .odt .rtf .pdf
    presentation_files = []     # список презентаций        .pptx .ppt .odp
    photo_files = []            # список фотографий         .png .jpg .jpeg .gif .svg .ico .webp
    archive_files = []          # список архивов            .zip .rar .7z .gz .tar
    audio_video_files = []      # список звуков             .mp3 .wav .mp4 .mkv .mov .avi
    code_files = []             # список кодовых файлов     .py .pyw .json .js .htm .html
    residue_files = []          # список остатка файлов
    system_files = []           # список системных файлы    .exe .lnk .url
    just_folders = []           # просто папки


    # Запускается указатель по списку всех файлов для их сортировки по расширениям
    for x in list_files:

        # Извлекается расширение файла
        file = os.path.splitext(x)[1]

        # Рассматривается расширение и записывается в подходящий список 
        match file.lower():
            case '.xlsx' | '.xls' | '.xlsm' | '.ods' | '.fods' | '.csv':
                table_files.append(x)

            case '.txt' | '.docx' | '.doc' | '.odt' | '.rtf' | '.pdf':
                text_files.append(x)

            case '.pptx' | '.ppt' | '.odp':
                presentation_files.append(x)

            case '.exe' | '.lnk' | '.url':
                system_files.append(x)

            case '.png' | '.jpg' | '.jpeg' | '.gif' | '.svg' | '.ico' | '.webp':
                photo_files.append(x)

            case '.zip' | '.rar' | '.7z' | '.gz' | '.tar':
                archive_files.append(x)

            case '.mp3' | '.wav' | '.mp4' | '.mkv' | '.mov' | '.avi':
                audio_video_files.append(x)

            case '.py' | '.pyw' | '.json' | '.js' | '.htm' | '.html':
                code_files.append(x)

            case '':
                just_folders.append(x)

            case _:
                residue_files.append(x)


    # Список всех отсортированных файлов по спискам для перемещения по папкам
    list_folders_for_Sorted_files = [table_files, text_files, presentation_files, photo_files, archive_files, audio_video_files, code_files, residue_files, just_folders]

    # Список названий списков для перемещения файлов в папку по названию списка
    folders_name_for_create = ['table_files', 'text_files', 'presentation_files', 'photo_files', 'archive_files', 'audio_video_files', 'code_files', 'residue_files', 'just_folders', 'system_files']

    # Подсчитываем общее количество файлов, чтобы определить, набран ли минимум для старта сортировки
    flag_for_start = len(table_files) + len(text_files) + len(presentation_files) + len(photo_files) + len(archive_files) + len(audio_video_files) + len(code_files) + len(residue_files) + len(just_folders)

    # Если же сортируется рабочий стол, то там в общее количество файлов ярлыки не учитываем
    if point == str(pathlib.Path.home()) + r'\desktop':
        pass

    else:
        flag_for_start += len(system_files)

    # Если количество файлов больше или равно указанного минимума, то сортировка начинается (по умолчанию минимум состаялет 13 файлов)
    if flag_for_start >= imported_minimal_amount:

        logs_file.write(f'[{time.strftime('%Y-%m-%d %H:%M:%S')}] [INFO ] Sorter began sorting {point}.' + '\n')

        # Запускается последовательность функций для сортировки файлов
        check_owner_folders(point)

    else:
        logs_file.write(f'[{time.strftime('%Y-%m-%d %H:%M:%S')}] [INFO] File count was below the minimum')
        pass

# Прекращаем вести логи
logs_file.close()