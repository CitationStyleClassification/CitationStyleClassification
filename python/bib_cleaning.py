import os

# english_path = '/home/artyom/Документы/библиографии/английский язык'
# russian_path = '/home/artyom/Документы/библиографии/русский язык'
# deutsch_path = '/home/artyom/Документы/библиографии/немецкий язык'

for file in os.listdir('econ'):
    f = open('econ' + '/' + file, 'r')
    lines = []
    for line in f:
        lines.append(line)
    f.close()
    f = open('econ' + '/' + file, 'w')
    for line in lines:
        if '%' not in line:
            f.write(line)
    f.close()

