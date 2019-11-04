import pygeoip, dpkt, socket, time

def makeKML(gi, ip):
    try:
        rec=gi.record_by_addr(ip)
        longitude=rec['longitude']
        latitude=rec['latitude']
        kml=(
               '<Placemark>\n'
               '<name>%s</name>\n'
               '<Point>\n'
               '<coordinates>%6f,%6f</coordinates>\n'
               '</Point>\n'
               '</Placemark>\n'
               ) %(ip,longitude,latitude)
        return kml
    except Exception, e:
        if "object has no attribute" in str(e):
            print "\n[-] No Database!"
            time.sleep(600)
            exit(0)
        else:
            print "[-] ", e
            return

def viewInfoIP(gi, IP, saveFile):
    try:
        rec=gi.record_by_addr(IP)
        country=rec['country_name']
        city=rec['city']
        latitude=rec['latitude']
        longitude=rec['longitude']
        if(str(latitude)=="37.57" and str(longitude)=="126.98"):
            fp=open(saveFile, "w")
            fp.write("No Database")
            fp.close()
            return
        fp=open(saveFile, "w")
        fp.write("IP : "+str(IP)+"\nCountry : "+str(country)+"\nCity : "+str(city)+"\nLatitude : "+str(latitude)+"\nLongitude : "+str(longitude)+"\n\n")
        fp.close()
    except Exception, e:
        if "object has no attribute" in str(e):
            print "\n[-] No Database!"
            time.sleep(600)
            exit(0)
        return

def main():    
    try:
        geoLiteCityFile=raw_input("Input GeoLiteCity.dat(http://dev.maxmind.com/geoip/legacy/geolite/) File : ")
        gi=pygeoip.GeoIP(geoLiteCityFile)
        kmlSaveFile=raw_input("Input GoogleEarth KML Save File(xxxx.kml) : ")
        saveFile=raw_input("Input Result Save File(xxxx.txt) : ")
        ip=raw_input("Input IP : ")
        viewInfoIP(gi, ip, saveFile)
        kmlHeader='<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n'
        kmlContent=makeKML(gi, ip)
        kmlFooter='</Document>\n</kml>\n'
        fp=open(kmlSaveFile, "w")
        fp.write(kmlHeader+kmlContent+kmlFooter)
        fp.close()
        print "\n[+] Open the "+saveFile+"\n[+] Open the "+kmlSaveFile+" in Google Earth!"
        time.sleep(600)
    except Exception, e:
        print "[-] ", e 
        time.sleep(600)
        exit(0)

if __name__=="__main__":
    main()
