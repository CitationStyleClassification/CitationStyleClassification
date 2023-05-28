import os
import sys
import csv

max_field_size = csv.field_size_limit(sys.maxsize)

command = f'csvstack -z {max_field_size * 10} '

csv_files_count = len(os.listdir('../csv'))

for i in range(1, csv_files_count + 1):
    command += f' ../csv/raw_bib_data_{i}.csv'

command += ' > ../csv/raw_bib_data.csv'

print(command)

os.system(command)

print("SUCCESS")