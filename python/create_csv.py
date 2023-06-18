import os
import re
import pypdfium2 as pdfium
from pypdfium2._helpers.misc import PdfiumError
import pandas as pd


def remove_page_number(s):
    indexes = []
    for i in range(len(s)):
        if s[i] == '[':
            indexes.append(i)
    for idx in indexes:
        if idx == 0 or not onlyDigits(s[idx - 1]):
            continue
        for j in range(1, idx):
            if onlyDigits(s[idx - j: idx]) and not onlyDigits(s[idx - j - 1: idx]):
                return s[:idx - j], s[idx:]
    return s, ""


def read_pdf_pdfium(path_to_pdf):
    try:
        pdf = pdfium.PdfDocument(path_to_pdf)
        s = ''
        for i in range(len(pdf)):
            s += pdf.get_page(i).get_textpage().get_text()
        return s
    except PdfiumError as e:
        print("Ошибка чтения PDF-файла")
        pdf_errors.write("Pdfium Error in file" + path_to_pdf + '\n')
        return ""

def square_brackets(s):
    return s.count('[')


def round_brackets(s):
    return s.count('(')


def slashes(s):
    return s.count('/')


def inverse_slashes(s):
    return s.count("\\")


def quotes(s):
    return s.count('”')


def dots(s):
    return s.count('.')


def commas(s):
    return s.count(',')


def semicolons(s):
    return s.count(';')


def colons(s):
    return s.count(':')


def ands(s):
    return s.count('and')


def ampersands(s):
    return s.count('&')


def page_ref(s):
    if 'p.' in s:
        return 1
    elif 'P.' in s:
        return 2
    elif 'pp.' in s:
        return 3
    elif 'стр.' in s:
        return 4
    elif 'С.' in s or 'с.' in s:
        return 5
    else:
        return 0


def tirets(s):
    return s.count('—')


def years(s):
    cnt = 0
    for i in range(50, 99):
        if str(i) in s:
            cnt += 1
    for i in range(1950, 2022):
        if str(i) in s:
            cnt += 1
    return cnt


def capital_letters(s):
    words = s.split()
    if not words:
        return 0
    capitals = 0
    for word in words:
        if word[0] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' or word[0] in 'АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ':
            capitals += 1
    return capitals / len(words)


def onlyDigits(s):
    for ch in s:
        if ch not in '1234567890':
            return False
    return True


def onlyLetters(s):
    for ch in s:
        if ch.lower() not in 'abcdefghijklmnopqrstuvwxyzабвгдеёжзийклмнопрстуфхцчшщъыьэюя':
            return False
    return True


def begin_ref(s):
    begin = s[s.find('[') + 1: s.find(']')]
    '''
    [1] - #1
    [Ackley85]  - #2
    [Ackley(1985)] - #3
    [Yae] - #4
    [Ackley, 1985] - #5
    [Ackley 1985] - #6
    [A Connectionist Algorithm for Genetic SearchAckley1985] - #7
    [] - #8 (style namunsrt)
    [Ackley 85] - #9
    [Ackl 85] - #10
    [Ackley1985], [Alba, Aldana, and TroyaAlba et al.1993] - #11
    [Abelson:1985:SIC] - #12 (style abstract)
    '''
    if not begin:
        return 8
    elif begin.count(':') == 2:
        return 12
    elif onlyDigits(begin):
        return 1
    elif onlyLetters(begin) or re.fullmatch(r'[a-zA-Z.]+\d?', begin):  # onlyLetters(begin):
        return 4
    elif '(' in begin:
        return 3
    elif re.fullmatch(r'[a-zA-Z]{4} \d\d[a-zA-Z]*', begin):
        return 10
    elif re.fullmatch(r'[a-zA-Z.& ]+, \d{4}[a-zA-Z]?', begin):
        return 5
    elif re.fullmatch(r'[a-zA-Z. ]+\s\d{4}', begin):
        return 6
    elif re.fullmatch(r'[a-zA-Z,. ]+\d{4}[a-zA-Z]?', begin):
        return 11
    elif re.fullmatch(r'[a-zA-Z]+\d\d[a-zA-Z]*', begin):
        return 2
    elif re.fullmatch(r'[a-zA-Z]+ \d\d[a-zA-Z]*', begin):
        return 9
    else:
        return 7


def key(s):
    return int('Key:' in s)


def abstract(s):
    return int('Abstract:' in s)


def annotation(s):
    return int('Annotation:' in s)


def sine(s):
    s = s.lower()
    if ('[s. n.]' in s) or ('[s. l.]' in s) or ('[s.n.]' in s) or ('[s.l.]' in s):
        return 2
    elif ('(s. n.)' in s) or ('(s. l.)' in s) or ('(s.n.)' in s) or ('(s.l.)' in s):
        return 3
    elif ('s. n.' in s) or ('s. l.' in s) or ('s.n.' in s) or ('s.l.' in s):
        return 1
    else:
        return 0


def et_al(s):
    if '[et al.]' in s:
        return 2
    elif '(et al.)' in s:
        return 3
    elif 'et al.' in s:
        return 1
    else:
        return 0


def etc(s):
    return int('etc.' in s)


pdf_path = '../pdf'
pdf_errors = open('../problems/pdf_errors.txt', 'w+')

processed_files = open('../problems/processed_pdf_files.txt', 'r')
processed_pdf = [line.split()[0] for line in processed_files]
processed_files.close()

processed_files = open('../problems/processed_pdf_files.txt', 'a')

file_number = 1

list_of_records = []

for pdf_file in os.listdir(pdf_path):
    print(pdf_file, file_number)
    file_number += 1
    bib_records = []
    buffer = ""
    try:
        pdf_document = read_pdf_pdfium(pdf_path + '/' + pdf_file)
        if pdf_document == "":
            continue
        temp_file = open('temp_file.txt', 'w')
        temp_file.write(pdf_document)
        temp_file.close()

        temp_file = open('temp_file.txt', 'r')
        for line in temp_file:
            if onlyDigits(line):  # тогда это строка с номером страницы ???
                continue
            if line[0] == '[':
                ref = line[line.find('[') + 1: line.find(']')]
                if buffer != "":
                    if 'ugost' not in pdf_file:
                        temp_buffer = remove_page_number(buffer)
                        if temp_buffer[1]:
                            bib_records.append(temp_buffer[0])
                            bib_records.append(temp_buffer[1])
                        else:
                            bib_records.append(buffer)
                        buffer = ""
                    else:
                        if onlyDigits(ref) and ref != "Text":
                            temp_buffer = remove_page_number(buffer)
                            if temp_buffer[1]:
                                bib_records.append(temp_buffer[0])
                                bib_records.append(temp_buffer[1])
                            else:
                                bib_records.append(buffer)
                            buffer = ""
            buffer += line
        if buffer != "":
            bib_records.append(buffer)

        processed_files.write(f"{pdf_file} SUCCESS\n")
        temp_file.close()
        os.remove('temp_file.txt')
    except FileExistsError:
        pdf_errors.write(f"File {pdf_file} is not exist\n")
        processed_files.write(f"{pdf_file} ERROR\n")
    except FileNotFoundError:
        pdf_errors.write(f"File {pdf_file} did not find\n")
        processed_files.write(f"{pdf_file} ERROR\n")

    for record in bib_records:
        list_of_records.append([
            square_brackets(record),
            round_brackets(record),
            slashes(record),
            inverse_slashes(record),
            quotes(record),
            dots(record),
            commas(record),
            semicolons(record),
            colons(record),
            abstract(record),
            ands(record),
            ampersands(record),
            page_ref(record),
            begin_ref(record),
            tirets(record),
            key(record),
            annotation(record),
            capital_letters(record),
            years(record),
            sine(record),
            et_al(record),
            etc(record),
            pdf_file[pdf_file.rfind('_') + 1: pdf_file.rfind('.')]
        ])

    if file_number % 100 == 0:
        list_of_records = filter(lambda rec: rec[0] != 0, list_of_records)
        data_frame = pd.DataFrame(
            list_of_records,
            columns=[
                'square_brackets',
                'round_brackets',
                'slashes',
                'inverse_slashes',
                'quotes',
                'dots',
                'commas',
                'semicolons',
                'colons',
                'abstract',
                'ands',
                'ampersands',
                'page_ref',
                'begin_ref',
                'tirets',
                'key',
                'annotation',
                'capital_letters',
                'years',
                'sine',
                'et_al',
                'etc',
                'style_name'
            ]
        )

        data_frame.to_csv(f'../csv/bib_data_{file_number // 100}.csv', index=False)
        list_of_records = []

processed_files.close()
pdf_errors.close()
