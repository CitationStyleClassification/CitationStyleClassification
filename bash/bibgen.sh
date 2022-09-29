#!/bin/bash

filename=$1".tex"

latex $filename > warnings_1.txt
bibtex $1 > warnings_2.txt
latex $filename > warnings_3.txt
latex $filename > warnings_4.txt
pdflatex $filename > warnings_5.txt

echo "PDF file have been generated successfully!"
