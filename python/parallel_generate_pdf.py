import pandas as pd
import PyPDF2 as pdf
import subprocess
import asyncio
import time
from multiprocessing import Process
from threading import Thread
from math import ceil
import os


def copy_file(dir1, dir2, file):
    os.system('cp %(dir1)s/%(file)s %(dir2)s/' % {'dir1': dir1, 'file': file, 'dir2': dir2})


def remove_file(dir, file):
    os.system('rm %(dir)s/%(file)s' % {'dir': dir, 'file': file})


def move_file(dir1, dir2, file):
    os.system('mv %(dir1)s/%(file)s %(dir2)s/' % {'dir1': dir1, 'file': file, 'dir2': dir2})


def bibgen():
    os.system('timeout 3 ../bash/bibgen.sh generate')


def generate_pdf(bib_file, bst_array, bst_path, template, thread_number):
    bib_name = bib_file[:bib_file.rfind('.')]
    for bst_file in bst_array:
        print("I'm in thread" + str(thread_number))
        copy_file(bst_path, current_dir, bst_file)
        bst_name = bst_file[:bst_file.rfind('.')]
        template += "\\bibliographystyle{%(bst_name)s}\n" % {'bst_name': bst_name}
        template += "\\bibliography{%(bib_name)s}\n" % {'bib_name': bib_name}
        template += '\\end{document}\n'

        generation_file = open('generate' + str(thread_number) + '.tex', 'w')
        generation_file.write(template)
        generation_file.close()

        print(bib_name, bst_name)

        bibgen()

        if ('generate' + str(thread_number) + '.pdf') not in os.listdir(current_dir):
            unprocessed_files.write(bib_name + ' ' + bst_name + '\n')
        else:
            new_pdf_name = '%(bib_name)s_%(bst_name)s.pdf' % {'bib_name': bib_name, 'bst_name': bst_name}
            os.rename('generate.pdf', new_pdf_name)
            move_file(current_dir, '../pdf', new_pdf_name)


def remove_trash_files():
    will_remove_files = []
    for file in os.listdir(current_dir):
        if ('.py' in file) or ('.txt' in file) or ('.bib' in file) or ('.pdf' in file):
            continue
        else:
            will_remove_files.append(file)
    for file in will_remove_files:
        remove_file(current_dir, file)


path_en_bib = '../bib/bibliographies/english'
path_en_bst = '../bst/BibTEX_styles/english_styles'
path_rus_bib = '../bib/bibliographies/russian'
path_rus_bst = '../bst/BibTEX_styles/russian_styles'
path_de_bib = '../bib/bibliographies/deutsch'
path_de_bst = '../bst/BibTEX_styles/deutsch_styles'
current_dir = '.'
unprocessed_files = open('../problems/unprocessed_files.txt', 'w')
template_file = open('generation_template.txt')
generation_template = template_file.read()
template_file.close()

bib_list = sorted(os.listdir(path_en_bib))
bst_list = sorted(os.listdir(path_en_bst))
part_size = ceil(len(bst_list) / 8)

for bib in bib_list:
    copy_file(path_en_bib, current_dir, bib)

    thread1 = Process(generate_pdf(bib, bst_list[:part_size], path_en_bst, generation_template, 1))
    thread2 = Process(generate_pdf(bib, bst_list[part_size:2 * part_size], path_en_bst, generation_template, 2))
    thread3 = Process(generate_pdf(bib, bst_list[2 * part_size:3 * part_size], path_en_bst, generation_template, 3))
    thread4 = Process(generate_pdf(bib, bst_list[3 * part_size:4 * part_size], path_en_bst, generation_template, 4))
    thread5 = Process(generate_pdf(bib, bst_list[4 * part_size:5 * part_size], path_en_bst, generation_template, 5))
    thread6 = Process(generate_pdf(bib, bst_list[5 * part_size:6 * part_size], path_en_bst, generation_template, 6))
    thread7 = Process(generate_pdf(bib, bst_list[6 * part_size:7 * part_size], path_en_bst, generation_template, 7))
    thread8 = Process(generate_pdf(bib, bst_list[7 * part_size:], path_en_bst, generation_template, 8))

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()
    thread5.start()
    thread6.start()
    thread7.start()
    thread8.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()
    thread5.join()
    thread6.join()
    thread7.join()
    thread8.join()

    remove_trash_files()
    remove_file(current_dir, bib)

unprocessed_files.close()
print("PDF-файлы успешно сгенерированы!")
