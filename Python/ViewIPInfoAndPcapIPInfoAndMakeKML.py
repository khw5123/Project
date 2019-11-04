import pygeoip, dpkt, socket, time

def viewInfoIP(gi, IP, fp):
    try:
        rec=gi.record_by_addr(IP)
        country=rec['country_name']
        city=rec['city']
        latitude=rec['latitude']
        longitude=rec['longitude']
        if(str(latitude)=="37.57" and str(longitude)=="126.98"):
            fp.write("No Database")
            return
        fp.write("IP : "+IP+"\nCountry : "+str(country)+"\nCity : "+str(city)+"\nLatitude : "+str(latitude)+"\nLongitude : "+str(longitude)+"\n\n")
    except Exception, e:
        print "[-] ", e
        time.sleep(30)
        exit(0)

def viewInfoPcap(gi, pcap, fp):
    count=1   
    for (ts, buf) in pcap:
        try:
            eth=dpkt.ethernet.Ethernet(buf)
            ip=eth.data
            src=socket.inet_ntoa(ip.src)
            dst=socket.inet_ntoa(ip.dst)
            fp.write("[Src "+str(count)+"]\n")
            viewInfoIP(gi, src, fp)
            fp.write("[Dst "+str(count)+"]\n")
            viewInfoIP(gi,dst, fp)
            count+=1
        except Exception, e:
            print "[-] ", e 
            pass

def makeKML(gi, ip):
    rec=gi.record_by_addr(ip)
    try:
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
        print "[-] ", e
        return ""

def plotIPs(gi, pcap):
    kmlPts='' 
    for (ts,buf) in pcap:
        try:
            eth=dpkt.ethernet.Ethernet(buf)
            ip=eth.data
            src=socket.inet_ntoa(ip.src)
            srcKML=makeKML(gi, src)
            dst=socket.inet_ntoa(ip.dst)
            dstKML=makeKML(gi, dst)
            kmlPts=kmlPts+srcKML+dstKML
        except Exception, e:
            print "[-] ", e
            return ""
    return kmlPts
        
def main():    
    try:
        print "GeoLiteCity.dat : http://dev.maxmind.com/geoip/legacy/geolite/"
        geoLiteCityFile=raw_input("Input GeoLiteCity.dat File : ")
        gi=pygeoip.GeoIP(geoLiteCityFile)
        kmlSaveFile=raw_input("Input GoogleEarth KML Save File(xx.kml) : ")
        kmlfp=open(kmlSaveFile, "w")
        kmlHeader='<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://www.opengis.net/kml/2.2">\n<Document>\n'
        kmlFooter='</Document>\n</kml>\n'
        saveFile=raw_input("Input Result Save File : ")
        fp=open(saveFile, "w")
        sel=raw_input("1. View the information on the IP\n2. View the IP information of departure and destination in the pcap file\nSelect : ")
        if(sel=="1"):
            ip=raw_input("Input IP : ")
            viewInfoIP(gi, ip, fp)
            string=kmlHeader+makeKML(gi, ip)+kmlFooter
            kmlfp.write(string)
            print "[+] Open the ", saveFile, " and Open the", kmlSaveFile, " from GoogleEarth"
            fp.close()
            kmlfp.close()
        elif(sel=="2"):
            pcapFile=raw_input("Input pcap File : ")
            pcapfp=open(pcapFile)
            pcap=dpkt.pcap.Reader(pcapfp)
            viewInfoPcap(gi, pcap, fp)
            string=kmlHeader+plotIPs(gi, pcap)+kmlFooter
            kmlfp.write(string)
            print "[+] Open the ", saveFile, " and Open the", kmlSaveFile, " from GoogleEarth"
            fp.close()
            kmlfp.close()
            pcapfp.close()
        time.sleep(30)
    except Exception, e:
        print "[-] ", e 
        time.sleep(30)
        exit(0)

if __name__=="__main__":
    main()
