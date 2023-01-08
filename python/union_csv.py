import os
import sys
import csv

max_field_size = csv.field_size_limit(sys.maxsize)

command = f'csvstack -z {max_field_size * 10}'

csv_files_count = len(os.listdir('../csv'))

for i in range(1, 199):
    command += f' ../csv/bib_data_{i}.csv'

command += ' > ../csv/bib_data_union_v2.csv'

print(command)

os.system(command)