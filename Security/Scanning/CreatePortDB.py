import shelve, socket, time

fileName="portDB.raj"

def create():
    shelf=shelve.open(fileName, writeback=True)
    shelf['desc']={}
    shelf.close()
    print "Dictionary is created"

def update():
    print "Updating..."
    shelf=shelve.open(fileName, writeback=True)
    data=(shelf['desc'])
    port=0
    while(port != 65535):
        port+=1
        try:
            protocol=socket.getservbyport(port)
            data[port]=protocol
        except:
            pass
    shelf.close()
    print "Dictionary is updated"

def list():
    print ""
    shelf=shelve.open(fileName, writeback=True)
    data=(shelf['desc'])
    for key, value in data.items():
        print key, ":", value
    print ""
    
def main():
    create()
    update()
    list()
    print "Confirm this Directory"
    time.sleep(20)
    
if __name__=="__main__":
    main()