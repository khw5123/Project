# -*- coding: utf-8 -*-
import time
from pyPdf import PdfFileReader

def showMetadata(pdfFile, saveFile):
    try: 
        pdf=PdfFileReader(file(pdfFile,'rb'))
        docInfo=pdf.getDocumentInfo()
        for metaItem in docInfo:
            print "[+] ", metaItem+" : "+docInfo[metaItem]
            try:
                fp=open(saveFile, "a")
                fp.write(metaItem+" : "+docInfo[metaItem]+"\n")
                fp.close()
            except:
                fp=open(saveFile, "a")
                fp.write(metaItem.encode('utf-8')+" : "+docInfo[metaItem].encode('utf-8')+"\n")
                fp.close()
                pass
    except Exception, e:
        print "[-]", e 
        time.sleep(600)
        exit(0)
        
def main():
    try:
        pdfFile=raw_input("Input PDF File : ")
        saveFile=raw_input("Input Svae File : ")
        showMetadata(pdfFile, saveFile)
        print "[+] Open the ", saveFile
        time.sleep(600)
    except Exception, e:
        print "[-]", e 
        time.sleep(600)
        exit(0)

if __name__ == '__main__':
    main()
