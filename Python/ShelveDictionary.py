import shelve, time

def create(fileName):
    try:
        shelf=shelve.open(fileName, writeback=True)
        shelf['desc']={}
        shelf.close()
        print "\nDictionary is created"
    except Exception, e:
        print "\n[-] ", e
        pass

def update(fileName):
    try:
        shelf=shelve.open(fileName, writeback=True)
        data=(shelf['desc'])
        key=raw_input("Enter the Key : ")
        data[key]=raw_input("Enter the  Value : ")
        shelf.close()
        print "\nDictionary is updated"
    except Exception, e:
        print "\n[-] ", e
        pass
    
def delete(fileName):
    try:
        shelf=shelve.open(fileName, writeback=True)
        data=(shelf['desc'])
        key=raw_input("Enter the Key : ")
        del data[key]
        shelf.close()
        print "\nEntry is deleted"
    except Exception, e:
        print "\n[-] ", e
        pass
    
def show(fileName):
    try:
        print ""
        shelf=shelve.open(fileName, writeback=True)
        data=(shelf['desc'])
        for key, value in data.items():
            print key, ":", value
    except Exception, e:
        print "\n[-] ", e
        pass
    
def main():
    try:
        while(True):
            print "\nUsage : C - Create\n\tU - Update\n\tS - Show\n\tD - Delete\n\tE - Exit"
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
                print "\n[-] Wrong Input\n"
    except Exception, e:
        print "[-] ", e
        time.sleep(600)
        exit(0)

if __name__=="__main__":
    main()
