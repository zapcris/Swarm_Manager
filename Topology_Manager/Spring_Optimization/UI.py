from tkinter import *
from tkinter.filedialog import askopenfile
from openpyxl import load_workbook


def open_file():

    file = askopenfile(mode ='r', filetypes =[('Excel Files', '*.xlsx *.xlsm *.sxc *.ods *.csv *.tsv')]) # To open the file that you want.
    #' mode='r' ' is to tell the filedialog to read the file
    # 'filetypes=[()]' is to filter the files shown as only Excel files

    wb = load_workbook(filename = file.name) # Load into openpyxl
    wb2 = wb.active

    #Whatever you want to do with the WorkSheet