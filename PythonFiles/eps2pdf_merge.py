# Imports:
from glob import *
# Loading the pyPdf Library
import PyPDF2 as pdf
import os

# Creating a routine that appends files to the output file
def append_pdf(input, output):
        [output.addPage(input.getPage(page_num)) for page_num in range(input.numPages)]

## Code starts here:
# 1) Export eps to pdf files:

fileList = glob('*.eps')
folderName = 'Merged-pdf'

try:
    os.mkdir(folderName)
except:
    pass

idx = 1
for f in fileList:
    print('File #{}/{}: {}'.format(idx, len(fileList), f))
    cmd =  'epstopdf {}'.format(f)
    os.system(cmd)
    idx = idx + 1

# 2) merge all pdf into one file ans save in a single folder:

    # Creating an object where pdf pages are appended to
output = pdf.PdfFileWriter()

pdfList = glob('*.pdf')
# Appending two pdf-pages from two different files
for f in pdfList:
    append_pdf(pdf.PdfFileReader(open(f, "rb")), output)

# Writing all the collected pages to a file
output.write(open("{}/teset.pdf".format(folderName), "wb"))