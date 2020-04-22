#-*- coding: utf-8 -*-
import win32com.client, time, random
'''
import Crypto.PublicKey.RSA, Crypto.Cipher.PKCS1_OAEP, zlib
public_key="MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA2EJeS17k/I69dbGlUGFgqTFmXfDbl74sNq9rj0reWqw41Eym8/9UO/lM428DWXIn1HMZ4IQb/AW8BqPBjwc5gcqKwdd1MK5PHBa7Qd8Y/rEtVsW48Ah02PQ6ecSCorvqy3JMyMwIBzJTUIjBo+p+MdLW2GHxGCJHQY7x78FyVaBAU4v+gmUEmNMyIrYeYtYMJFHAz3H8wEjhuH8O+puE1Xm+3Yngd4EHVuRqWdFPktj+srv3Sf+lsOmQ+3s85h3xLOw5l6qMTzhmeLJNbLnjSZ/5BF9vO3il9BlBzYctRl1TyYH6V6G7fWCb4QrvAOl0ERH55sxQEnnNBUWwNyq+iwIDAQAB"
def encrypt_string(plaintext):
    chunk_size=256
    print "Compressing: %d bytes" % len(plaintext)
    plaintext=zlib.compress(plaintext)
    print "Encrypting %d bytes" % len(plaintext)
    rsakey=Crypto.PublicKey.RSA.importKey(public_key)
    rsakey=Crypto.Cipher.PKCS1_OAEP.new(rsakey)
    encrypted=""
    offset=0
    while(offset < len(plaintext)):
        chunk=plaintext[offset:offset+256]
        if(len(chunk)%chunk_size != 0):
            chunk+=" " *(chunk_size - len(chunk))
        encrypted+=rsakey.encrypt(chunk)
        offset+=chunk_size
    encrypted=encrypted.encode("base64")
    print "Base64 encoded crypto: %d" % len(encrypted)
    return encrypted
'''
def wait_for_browser(browser):
    while(browser.ReadyState!=4 and browser.ReadyState!="complete"):    
        time.sleep(0.1)

def random_sleep():
    time.sleep(random.randint(0,1))

def login_to_tumblr(ie):
    full_doc=ie.Document.all
    for i in full_doc:
        # print str(i.id)
        if(i.id=="signup_email"):
            i.setAttribute("value", username)
        elif(i.id=="signup_password"):
            i.setAttribute("value", password)
    random_sleep()
    try:
        if(ie.Document.forms[0].id=="signup_form"):
            ie.Document.forms[0].submit()
        else:
            ie.Document.forms[1].submit()
    except IndexError, e:
        pass
    random_sleep()
    wait_for_browser(ie)

def post_to_tumblr(ie, title, post):
    full_doc=ie.Document.all
    for i in full_doc:
        #print str(i.id)
        if(i.id=="new_post"):
            i.setAttribute("value",title)
            title_box=i
            i.focus()
        elif(i.id=="new_post"):
            i.setAttribute("innerHTML", post)
            print "[+] Set Text Area"
            i.focus()
        elif(i.id=="new_post_buttons"):
            print "[+] Found Post Button"
            post_form=i
            i.focus()
    random_sleep()    
    title_box.focus()
    random_sleep()
    post_form.children[0].click()
    wait_for_browser(ie)
    random_sleep()

def main(): 
    try:
        username=raw_input("Input Tumblr Account : ")
        password=raw_input("Input Tumblr Password : ")
        file=raw_input("Input the name of the file to post : ")
        fp=open(file, "r")
        content=fp.read()
        fp.close()
        ie=win32com.client.Dispatch("InternetExplorer.Application")
        ie.Visible=0 # 0일 경우 프로세스를 은닉하고, 1 일 경우 프로세스를 보이게 한다.
        ie.Navigate("http://www.tumblr.com/login")
        wait_for_browser(ie)
        login_to_tumblr(ie) # 로그인
        print "[+] Successed Login"
        ie.Navigate("https://www.tumblr.com/new/text")
        wait_for_browser(ie)
        post_to_tumblr(ie, file, content) # 포스팅
        print "[+] Successed Post"
        ie.Quit()
        print "[+] Open The Your Tumblr"
        time.sleep(30)
    except Exception, e:
        print "[-] ", e 
        time.sleep(30)
        exit(0)
        
if __name__=="__main__":
    main()