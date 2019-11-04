import hashlib, crypt, subprocess

def showMessageDigest():
    subprocess.call("pwconv", shell=True)
    shadow=open("/etc/shadow")
    for line in shadow.readlines():
        if ':' in line:
            user=line.split(':')[0]
            md=line.split(':')[1]
            if(len(md)!=1):
                print "User : ", user, "\tMessage Digest : ", md

def crack(dictionary, messageDigest, salt, fp):
    for password in fp.readlines():
        password=password.strip('\n')
        md=crypt.crypt(password, salt)
        if(md==messageDigest):
            print "[+] ", password
            return

def main():
    dictionary=raw_input("Input Dictionary File : ")
    #showMessageDigest()
    messageDigest=raw_input("Input Message Digest : ")
    salt="$"+messageDigest.split("$")[1]+"$"+messageDigest.split("$")[2]+"$"
    fp=open(dictionary,"r")
    crack(dictionary, messageDigest, salt, fp)
    fp.close()
    
if __name__=="__main__":
    main()