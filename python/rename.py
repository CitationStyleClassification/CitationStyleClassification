import os

cnt = 1
for file in os.listdir('../bib/bibliographies/english'):
    if file[0] == 'q':
        os.rename('../bib/bibliographies/english/' + file, '../bib/bibliographies/english/' + 'dblp' + str(cnt) + '.bib')
        cnt += 1