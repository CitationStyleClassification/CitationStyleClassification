#!/bin/bash

filename=$1".tex"

latex $filename > ../problems/warnings_1.txt
bibtex $1 > ../problems/warnings_2.txt
latex $filename > ../problems/warnings_3.txt
latex $filename > ../problems/warnings_4.txt
pdflatex $filename > ../problems/warnings_5.txt

# echo "PDF file have been generated successfully!"
# example: ./bibgen.sh generate