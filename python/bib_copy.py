import os

def copy_file(dir1, dir2, file):
    os.system('cp %(dir1)s/%(file)s %(dir2)s/' % {'dir1': dir1, 'file': file, 'dir2': dir2})

dir1 = '../bib/bibliographies/english'
dir2 = '.'
#copy_file(dir1, dir2, 'dblp2.bib')

cnt = 0
for bib in os.listdir(dir1):
    copy_file(dir1, dir2, bib)
    print(bib[:bib.rfind('.')])
    cnt += 1
    if cnt == 5:
        break
