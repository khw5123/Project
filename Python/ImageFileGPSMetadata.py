import time
from PIL import Image
from PIL.ExifTags import TAGS

def findGPSMetadata(imgFileName):
    try:
        exifData={}
        imgFile=Image.open(imgFileName)
        info=imgFile._getexif()
        if info:
            for (tag, value) in info.items():
                decoded=TAGS.get(tag, tag)
                exifData[decoded]=value
            exifGPS=exifData["GPSInfo"]
            if exifGPS:
                print "\n[+] GPS Metadata : "+str(exifGPS)
    except Exception, e:
        print "[-] ", e
        pass

def main():
    try:
        imgFile=raw_input("Input Image File : ")
        findGPSMetadata(imgFile)
        print "\nEnd!"
        time.sleep(600)
    except Exception, e:
        print "[-] ", e
        time.sleep(600)
        exit(0)

if __name__=="__main__":
    main()
