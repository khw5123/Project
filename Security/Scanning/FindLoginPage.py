import httplib, shelve

def find(url, shelveFile, sss):
    shelf=shelve.open(shelveFile ,writeback=True)
    data=(shelf['desc'])
    for key, value in data.items():
        if(key==sss):
            u=url+value
            http_r=httplib.HTTPConnection(url)
            http_r.request("GET", value)
            reply=http_r.getresponse()
            if(reply.status==200):
                print "[+] http://", u

def main():
    url=raw_input("Input URL : ")
    shelveFile=raw_input("Input raj File Name(shelve DB) : ")
    sss=raw_input("Input Server Side Script( ex) php, asp, jsp ) : ")
    url=url.replace("http://","")
    url=url.replace("/","")
    find(url, shelveFile, sss)

if __name__=="__main__":
    main()
'''
import shelve

def create(fileName):
    shelf=shelve.open(fileName, writeback=True)
    shelf['desc']={}
    shelf.close()
    print "Dictionary is created\n"

def update(fileName):
    shelf=shelve.open(fileName, writeback=True)
    data=(shelf['desc'])
    key=raw_input("Enter the Key : ")
    data[key]=raw_input("Enter the  Value : ")
    shelf.close()
    print "Dictionary is updated\n"
    
def delete(fileName):
    shelf=shelve.open(fileName, writeback=True)
    data=(shelf['desc'])
    key=raw_input("Enter the Key : ")
    del data[key]
    shelf.close()
    print "Entry is deleted\n"

def show(fileName):
    print ""
    shelf=shelve.open(fileName, writeback=True)
    data=(shelf['desc'])
    for key, value in data.items():
        print key, ":", value
    print ""
    
def main():
    while(True):
        print "Usage : C - Create\n\t    U - Update\n\t    S - Show\n\t    D - Delete\n\t    E - Exit\n"
        sel=raw_input("Select :  ")  
        if(sel=='C' or sel=='c'):
            fileName=raw_input("Input Create File Name(No Input extension) : ")
            fileName+=".raj"
            create(fileName)
        elif(sel=='U' or sel=='u'):
            fileName=raw_input("Input File Name(No Input extension) : ")
            fileName+=".raj"
            update(fileName)
        elif(sel=='S' or sel=='s'):
            fileName=raw_input("Input File Name(No Input extension) : ")
            fileName+=".raj"
            show(fileName)
        elif(sel=='D' or sel=='d'):
            fileName=raw_input("Input File Name(No Input extension) : ")
            fileName+=".raj"
            delete(fileName)
        elif(sel=='E' or sel=='e'):
            exit()
        else:
            print "Wrong Input\n"

if __name__=="__main__":
    main()
'''