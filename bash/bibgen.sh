#!/bin/bash

filename=$1".tex"

yes "" | latex $filename > /dev/null
yes "" | bibtex $1 > /dev/null
yes "" | latex $filename > /dev/null
yes "" | latex $filename > /dev/null
yes "" | pdflatex $filename > /dev/null
