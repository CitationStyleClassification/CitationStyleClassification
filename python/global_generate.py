import os
import subprocess

dir1 = '/home/artyom/Документы/стили_ТЕХ/Physiology_Review'
dir2 = '/home/artyom/Документы/стили_ТЕХ'

for file in os.listdir(dir1):
    os.system('cp %(dir1)s/%(file)s %(dir2)s/' % {'dir1': dir1, 'file': file, 'dir2': dir2})

for file in os.listdir(dir2):
    if 'IEEE' in file:
        print(file)