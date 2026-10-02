import json
import os
import pathlib

# По умолчанию не существует директорий, которые нужно сортировать
data_directories = []
# По умолчанию не существует путей файлов, которых надо игнорировать
data_ignores = []
# По умолчанию минимальное количество файлов для старта сортировки составляет 13 файлов
data_minimal_amount = [13]

# Если существует конфиг, то импортируем директории оттуда
if os.path.exists(r'c:\OP_Sorter\config.json'):

    # Открываем конфиг и читаем его
    config_was_opened = open(r'c:\OP_Sorter\config.json', 'r')
    config_was_loaded = json.load(config_was_opened)

    # Импортируем директории для сортировки, пути игнорируемых файлов, минимальное количество файлов для начала сортировки
    data_directories = config_was_loaded['directories']
    data_ignores = config_was_loaded['ignores']
    data_minimal_amount = config_was_loaded['amount']

    config_was_opened.close()

# Проверяем на наличие папки "OP_Sorter" для конфига
if os.path.isdir(r'C:\OP_Sorter'):
    pass

else:
    os.mkdir(r'C:\OP_Sorter')

# Функция для добавления директорий под сортировку, путей файлов, которые не нужно сортировать
def accept_data(key):
    # Очищаем терминал
    os.system('cls')

    # Обрабатваем директории под сортировку
    if key == 'directories':
        print('Which directories do you want to sort? Write only the paths')

        # Начинаем обработку. Если уже были указаные какие-то директории, то их тоже включаем в обработку
        if len(data_directories) > 0:

            # Запускаем указатель по списку директорий. Выводим каждый и нумеруем
            for number, directory in enumerate(data_directories):
                print(f'{number}. {directory}')
        
        else:
            number = -1

        # Начинаем опрос директорий
        while True:
            input_data = input(f'{number + 1}. ')

            try:
                # Если путь существует, и он не был до этого указан ни в списке для директорий, ни в списке для игноров
                if os.path.isdir(input_data) and str(pathlib.Path(input_data)).lower() not in data_directories and str(pathlib.Path(input_data)).lower() not in data_ignores:
                    # То добавляем его в список для директорий. Сохраняем и выводим его в список
                    data_directories.append(str(pathlib.Path(input_data)).lower())
                    config()
                    accept_data('directories')
                    break

                # Если же путь существует, и он был уже указан в списке директорий
                elif os.path.isdir(input_data) and str(pathlib.Path(input_data)).lower() in data_directories:
                    # То просто сохраняем настройки и просим ввести другую директорию
                    config()
                    accept_data('directories')
                    break

                # В ином случае мы просто сохраняем настройки и отправляемся в главное меню
                else:
                    config()
                    owner_menu()
                    break

            except:
                config()
                owner_menu()
                break

    # Обрабатваем пути файлов, которые нужно игнорировать при сортировке
    elif key == 'ignores':
        print('Which files do you not want to sort? Write only the paths')
        
        # Начинаем обработку. Если уже были указаные какие-то пути, то их тоже включаем в обработку
        if len(data_ignores) > 0:

            # Запускаем указатель по списку путей. Выводим каждый и нумеруем
            for number, ignore in enumerate(data_ignores):
                print(f'{number}. {ignore}')

        else:
            number = -1

        # Начинаем опрос путей
        while True:
            input_data = input(f'{number + 1}. ')

            try:
                # Если путь существует, и он не был до этого указан ни в списке для директорий, ни в списке для игноров
                if os.path.exists(input_data) and str(pathlib.Path(input_data)).lower() not in data_ignores and str(pathlib.Path(input_data)).lower() not in data_directories:
                    # То добавляем его в список для путей. Сохраняем и выводим его в список
                    data_ignores.append(str(pathlib.Path(input_data)).lower())
                    config()
                    accept_data('ignores')
                    break

                # Если же путь существует, и он был уже указан в списке путей
                elif os.path.exists(input_data) and str(pathlib.Path(input_data)).lower() in data_ignores:
                    # То просто сохраняем настройки и просим ввести другую директорию
                    config()
                    accept_data('ignores')
                    break

                # В ином случае мы просто сохраняем настройки и отправляемся в главное меню
                else:
                    config()
                    owner_menu()
                    break

            except:
                config()
                owner_menu()
                break


# Функция для удаления директорий под сортировку, путей файлов, которые не нужно сортировать
def remove_data(key):
    # Очищаем терминал
    os.system('cls')

    # Обрабатваем директории под сортировку
    if key == 'directories':
        print('Which directories do you want to remove out of the sort? Write only number')
        
        # Запускаем указатель по списку директорий. Выводим каждый и нумеруем
        for number, directory in enumerate(data_directories):
            print(f'{number}. {directory}')

        # Начинаем опрос директорий
        while True:
            input_number = input()

            try:
                # Если номер директории больше 0 и меньше количества всех директорий, а также если список директорий не равен нулю
                if 0 <= int(input_number) < len(data_directories) and len(data_directories) > 1:
                    # То удаляем директорию под указаным номером. Сохраняем настройки и выводим его в список
                    data_directories.pop(int(input_number))
                    config()
                    remove_data('directories')
                    break

                # Если же номер директории больше 0 и меньше количества всех директорий, а также список директорий равен 1
                elif 0 <= int(input_number) < len(data_directories) and len(data_directories) == 1:
                    # То просто удаляем директорю, сохраняем настройки и возвращаемся в главное меню
                    data_directories.pop(int(input_number))
                    config()
                    owner_menu()
                    break

                # В ином случае сохраняем настройки и просим ввести корректный номер директории
                else:
                    config()
                    remove_data('directories')
                    break

            except:
                config()
                owner_menu()
                break

    # Обрабатваем пути под сортировку
    elif key == 'ignores':
        print('Which files do you want to remove out of ignore? Write only number')
        
        # Запускаем указатель по списку путей. Выводим каждый и нумеруем
        for number, ignore in enumerate(data_ignores):
            print(f'{number}. {ignore}')

        # Начинаем опрос директорий
        while True:
            input_number = input()

            try:
                # Если номер пути больше 0 и меньше количества всех путей, а также если список путей не равен нулю
                if 0 <= int(input_number) < len(data_ignores) and len(data_ignores) > 1:
                    # То удаляем путь под указаным номером. Сохраняем настройки и выводим его в список
                    data_ignores.pop(int(input_number))
                    config()
                    remove_data('ignores')
                    break

                # Если же номер пути больше 0 и меньше количества всех путей, а также список путей равен 1
                elif 0 <= int(input_number) < len(data_ignores) and len(data_ignores) == 1:
                    # То просто удаляем путь, сохраняем настройки и возвращаемся в главное меню
                    data_ignores.pop(int(input_number))
                    config()
                    owner_menu()
                    break

                # В ином случае сохраняем настройки и просим ввести корректный номер директории
                else:
                    config()
                    remove_data('ignores')
                    break

            except:
                config()
                owner_menu()
                break


# Функция для указания минимального количества файлов для начала сортировки
def change_amount():
    # Очищаем терминал
    os.system('cls')

    print('Which minimal amount of files do you want to sort? Write only number')
    # Начинаем опрос числа
    while True:
        input_number = input()

        try:
            # Если число больше -1 и оно является единственным для сортировщика
            if int(input_number) >= 0 and len(data_minimal_amount) == 1:
                # То заменяем прошлый минимум на актуальный. Сохраняем настройки и выходим в главное меню
                data_minimal_amount.pop(0)
                data_minimal_amount.append(int(input_number))
                config()
                owner_menu()
                break

            # Если число меньше 0, просим указать число снова
            elif int(input_number) < 0:
                config()
                change_amount()
                break

        except:
            config()
            owner_menu()
            break


# Функция для сохранения настроек
def config():
    # Проверяем наличие конфига
    if os.path.exists(r'C:\OP_Sorter\config.json'):
        # Если конфиг существует, то начинчинаем процесс сохранения
        opening_config = open(r'C:\OP_Sorter\config.json', 'w')

        # Создаем структуру информации, которую нужно передать для дампа JSON
        json_data_dump = {
            "directories" : data_directories,
            "ignores" : data_ignores,
            "amount" : data_minimal_amount
        }

        # Указываем JSON что нужно сохранить, где и в каком виде
        json.dump(json_data_dump, opening_config, ensure_ascii = False)

        opening_config.close()


    # Если конфига не существует
    else:
        # То переходим в директорию, предназначенную для него 
        os.chdir(r'C:\OP_Sorter')
        # Создаем конфиг
        opening_config = open('config.json', 'w') 

        # Создаем структуру информации, которую нужно передать для дампа JSON
        json_data_dump = {
            "directories" : data_directories,
            "ignores" : data_ignores,
            "amount" : data_minimal_amount
        }

        # Указываем JSON что нужно сохранить, где и в каком виде
        json.dump(json_data_dump, opening_config, ensure_ascii = False)

        opening_config.close()



# Функция для вывода главного меню
def owner_menu():
    # Очищаем терминал
    os.system('cls')

    print('Sorter files 1.0.0')
    print('-----------------------------------------------------------------')

    print('1. Add new directories for sorter')
    print('2. Add new ignore files')
    print()
    print('3. Remove direcories out of the sort')
    print('4. Remove ignore files')
    print()
    print(f'5. Amount files for work sorter     {data_minimal_amount}')
    print()
    print('0. Exit')

    print('-----------------------------------------------------------------')

    # Запрашиваем у пользователя нужный ему пункт
    choice = input('Choose option (0-4): ')
    
    # Добавить новые директории под сортировку
    if choice == '1':
        accept_data('directories')

    # Добавить пути файлов, которые нужно игнорировать при сортировке
    elif choice == '2':
        accept_data('ignores')

    # Удалить директории из под сортировки
    elif choice == '3' and len(data_directories) > 0:
        remove_data('directories')

    # Удалить пути файлов, которые нужно игнорировать при сортировке
    elif choice == '4' and len(data_ignores) > 0:
        remove_data('ignores')

    # Указать новое минимальное количество файлов для старта сортировки
    elif choice == '5':
        change_amount()

    # Сохранить настройки и завершить сеанс
    elif choice == '0':
        config()
        os.system('cls')
        quit

    # Иначе снова вызвать главное меню
    else:
        owner_menu()


owner_menu()