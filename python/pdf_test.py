from io import StringIO
import time
import PyPDF2
import pypdfium2 as pdfium

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser


def read_pdf_pdfminer(path_to_pdf: str) -> str:
    output_string = StringIO()
    with open(path_to_pdf, 'rb') as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)
    return output_string.getvalue()


def read_pdf_pypdf(path_to_pdf: str) -> str:
    s = ''
    with open(path_to_pdf, 'rb') as f:
        pdf_reader = PyPDF2.PdfFileReader(f)
        for page_num in range(pdf_reader.numPages):
            s += pdf_reader.getPage(page_num).extractText()
    return s


def read_pdf_pdfium(path_to_pdf):
    pdf = pdfium.PdfDocument(path_to_pdf)
    s = ''
    for i in range(len(pdf)):
        s += pdf.get_page(i).get_textpage().get_text()
    return s


t0 = time.time()
s = read_pdf_pdfium('../pdf/dai_ama.pdf')
t1 = time.time()
print(s)

print(t1 - t0)
