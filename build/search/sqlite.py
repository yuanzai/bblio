from models import Document
from os import listdir
from os.path import isfile
import re
import csv
import sys

def populateTable(path):
    Document.objects.all().delete()
    for f in listdir(path):
        if isfile(f):
            print ""
        else:
            try:
                d = Document()
                thisFile = open(path + f, 'r')
                #d.document_text = re.escape(thisFile.read())
                readText = re.sub(r'[^\w\_s\n!"#$%&/\'()*+,./:;=?@\^_`{|}~-]', ' ', thisFile.read())
                #d.document_text = readText
                d.document_text = re.sub('\n', '</br>', readText)
                d.file_name = f
                d.save()
            except:
                pass    

def populateSites(path):
    Document.objects.all().delete()
    csvList = listdir(path)
    
    for l in csvList:
        if l[0:4]=='site':
            with open(path + l, 'rb') as csvfile:
                csv.field_size_limit(sys.maxsize)
                csvreader = csv.reader(csvfile, delimiter=',', quotechar='"')
                for row in csvreader:
                    try:
                        d = Document()
                        if len(row[0]) < 10:
                            continue
                        d.document_text = row[0]
                        d.urlAddress = row[1]
                        if row[1][0:3] == 'www':
                            d.urlAddress = row[1][4:]
                        d.title = row[2]
                        d.save()
                    except:
                        pass 
                    