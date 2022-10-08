#!/bin/bash

filename=$1".tex"

latex $filename > /dev/null
bibtex $1 > /dev/null
latex $filename > /dev/null
latex $filename > /dev/null
pdflatex $filename > /dev/null
