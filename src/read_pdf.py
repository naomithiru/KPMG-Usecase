
# Import libraries
from PIL import Image
import pytesseract
import sys
from pdf2image import convert_from_path
import os

#https://www.youtube.com/watch?v=6DjFscX4I_c&ab_channel=Murtaza%27sWorkshop-RoboticsandAI

PDF_file = r'F:\\belearner\\KPMG-Usecase\\assets\\10201-2017-014921.pdf'
#https://stackoverflow.com/questions/50951955/pytesseract-tesseractnotfound-error-tesseract-is-not-installed-or-its-not-i
pytesseract.pytesseract.tesseract_cmd = r'T:\\Users\\Fra\\AppData\\Local\\Programs\\Tesseract-OCR\\tesseract.exe'

# Path of the pdf

'''
Part #1 : Converting PDF to images
'''

# Store all the pages of the PDF in a variable
pages = convert_from_path(PDF_file, 500)