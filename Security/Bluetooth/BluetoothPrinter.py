#-*- coding: utf-8 -*-
import obexftp    

def imagePrint(mac, port, imageFile): # RFCOMM 프로토콜의 OBEX Object Push 서비스를 제어해 이미지를 프린터로 전송한다.
    try:
        btPrinter=obexftp.client(obexftp.BLUETOOTH)
        btPrinter.connect(mac, port) # Obexftp로 프린터에 연결
        btPrinter.put_file(imageFile) # 공격자의 컴퓨터에서 이미지파일을 프린터로 전송
        print "[+] Printed Image"
    except:    
        print "[-] Failed to print Image"

def main():
    mac=raw_input("Input Bluetooth Printer Mac Address : ")
    port=raw_input("Input OBEX Object Push Service Port : ")
    imageFile=raw_input("Input of the image file to be printed : ")
    imagePrint(mac, int(port), imageFile)
    
if __name__=="__main__":
    main()