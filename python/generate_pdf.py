import os


def copy_file(dir1, dir2, file):
    os.system('cp %(dir1)s/%(file)s %(dir2)s/' % {'dir1': dir1, 'file': file, 'dir2': dir2})


def remove_file(dir, file):
    os.system('rm %(dir)s/%(file)s' % {'dir': dir, 'file': file})


def move_file(dir1, dir2, file):
    os.system('mv %(dir1)s/%(file)s %(dir2)s/' % {'dir1': dir1, 'file': file, 'dir2': dir2})


def bibgen(timeout=3):
    os.system('timeout %(timeout)i ../bash/bibgen.sh generate' % {'timeout': timeout})


path_en_bib = '../bib/bibliographies/english'
path_en_bst = '../bst/BibTEX_styles/english_styles'
path_ru_bib = '../bib/bibliographies/russian'
path_ru_bst = '../bst/BibTEX_styles/russian_styles'
path_de_bib = '../bib/bibliographies/deutsch'
path_de_bst = '../bst/BibTEX_styles/deutsch_styles'
current_dir = '.'
unprocessed_files = open('../problems/unprocessed_files.txt', 'w')
generated_pdf = sorted(os.listdir('../pdf'))

for bib in sorted(os.listdir(path_en_bib)):
    copy_file(path_en_bib, current_dir, bib)
    bib_name = bib[:bib.rfind('.')]

    for bst in sorted(os.listdir(path_en_bst)):
        if 'gost' not in bst:
            continue
        copy_file(path_en_bst, current_dir, bst)
        bst_name = bst[:bst.rfind('.')]

        if bib_name + '_' + bst_name + '.pdf' in generated_pdf:
            remove_file(current_dir, bst)
            continue

        template_file = open('generation_template.txt')
        generation_template = template_file.read()

        generation_template += "\\bibliographystyle{%(bst_name)s}\n" % {'bst_name': bst_name}
        generation_template += "\\bibliography{%(bib_name)s}\n" % {'bib_name': bib_name}
        generation_template += '\\end{document}\n'

        generation_file = open('generate.tex', 'w')
        generation_file.write(generation_template)

        template_file.close()
        generation_file.close()

        print(bib_name, bst_name)

        bibgen(timeout=60)

        will_remove_files = []
        for file in os.listdir(current_dir):
            if ('.py' in file) or ('.txt' in file) or ('.bib' in file) or ('.pdf' in file):
                continue
            else:
                will_remove_files.append(file)
        for file in will_remove_files:
            remove_file(current_dir, file)

        if 'generate.pdf' not in os.listdir(current_dir):
            unprocessed_files.write(bib_name + ' ' + bst_name + '\n')
        else:
            new_pdf_name = '%(bib_name)s_%(bst_name)s.pdf' % {'bib_name': bib_name, 'bst_name': bst_name}
            os.rename('generate.pdf', new_pdf_name)
            move_file(current_dir, '../pdf', new_pdf_name)

    remove_file(current_dir, bib)

unprocessed_files.close()
print("PDF files successfully generated!")
