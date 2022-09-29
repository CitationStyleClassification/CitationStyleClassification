import os


def file_size_MB(my_file):
    return os.stat(my_file).st_size / (1024 * 1024)


# файлы для объединения
english_bib_1 = open('/home/artyom/Документы/библиографии/english_1.bib', 'w')
english_bib_2 = open('/home/artyom/Документы/библиографии/english_2.bib', 'w')
russian_bib = open('/home/artyom/Документы/библиографии/russian.bib', 'w')
deutsch_bib = open('/home/artyom/Документы/библиографии/deutsch.bib', 'w')
problems = open('problems.txt', 'w')  # лог ошибок

english_path = '/home/artyom/Документы/библиографии/английский язык'
russian_path = '/home/artyom/Документы/библиографии/русский язык'
deutsch_path = '/home/artyom/Документы/библиографии/немецкий язык'

for file in os.listdir(english_path):
    with open(english_path + '/' + file) as f:
        try:
            if file_size_MB('/home/artyom/Документы/библиографии/english_1.bib') < 45:
                english_bib_1.write(f.read() + '\n')
            else:
                english_bib_2.write(f.read() + '\n')
        except Exception as e:
            problems.write(english_path + '/' + file + '\n')
            # problems.writelines(str(e) + '\n')

for file in os.listdir(russian_path):
    with open(russian_path + '/' + file) as f:
        try:
            russian_bib.write(f.read() + '\n')
        except Exception as e:
            problems.write(russian_path + '/' + file + '\n')
            # problems.writelines(str(e) + '\n')

for file in os.listdir(deutsch_path):
    with open(deutsch_path + '/' + file) as f:
        try:
            deutsch_bib.write(f.read() + '\n')
        except Exception as e:
            problems.write(deutsch_path + '/' + file + '\n')
            # problems.writelines(str(e) + '\n')

english_bib_1.close()
english_bib_2.close()
russian_bib.close()
deutsch_bib.close()
problems.close()
