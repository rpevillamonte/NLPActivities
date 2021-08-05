
import nltk
import PyPDF2
import pandas as pd


pdfFileObject = open(r"./pdfs/ai-tecuci-WIRE.pdf", 'rb')


pdfReader = PyPDF2.PdfFileReader(pdfFileObject)

text = ''
for p in range(pdfReader.numPages):

    pageObject = pdfReader.getPage(p)

    text +=pageObject.extractText()

words = nltk.word_tokenize(text)
print(words)    

pdfFileObject.close()
