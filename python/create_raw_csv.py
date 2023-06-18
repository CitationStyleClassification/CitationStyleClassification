import os
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
            s += pdf.get_page(i).get_textpage().get_text_range()
        return s
    except PdfiumError as e:
        print("PDF reading error")
        pdf_errors.write("Pdfium Error in file" + path_to_pdf + '\n')
        return ""


def onlyDigits(s):
    for ch in s:
        if ch not in '1234567890':
            return False
    return True


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
            if onlyDigits(line) or 'Список литературы' in line:
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
        pdf_errors.write(f"File {pdf_file} does not exist\n")
        processed_files.write(f"{pdf_file} ERROR\n")
    except FileNotFoundError:
        pdf_errors.write(f"File {pdf_file} did not find\n")
        processed_files.write(f"{pdf_file} ERROR\n")
    for record in bib_records:
        list_of_records.append([
            record,
            pdf_file[pdf_file.rfind('_') + 1: pdf_file.rfind('.')]
        ])

    if file_number % 100 == 0:
        list_of_records = filter(lambda rec: rec[0] != 0, list_of_records)
        data_frame = pd.DataFrame(
            list_of_records,
            columns=[
                'record',
                'style_name'
            ]
        )

        data_frame.to_csv(f'../csv/raw_bib_data_{file_number // 100}.csv', index=False)
        list_of_records = []

processed_files.close()
pdf_errors.close()
