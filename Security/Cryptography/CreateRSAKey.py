import Crypto.PublicKey.RSA, time

def main():
    try:
        keyLength=raw_input("Input Key Length( ex) 1024 or 2048 or 4096... ) : ")
        saveFile=raw_input("Input Save File : ")
        print "Wait...\n"
        newKey=Crypto.PublicKey.RSA.generate(int(keyLength), e=65537)
        publicKey=newKey.publickey().exportKey("PEM")
        print publicKey
        privateKey=newKey.exportKey("PEM") 
        print privateKey
        fp=open(saveFile, "w")
        fp.write(str(publicKey)+"\n"+str(privateKey))
        fp.close()
        print "\n[+] End!"
        time.sleep(600000) 
    except Exception, e:
        print "[-] ", e 
        exit(0)

if __name__=="__main__":
    main()
