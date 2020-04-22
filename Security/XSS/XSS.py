import mechanize

nameList=[]
valueList=[]
count=0

def attack(url):
    br=mechanize.Browser()
    br.set_handle_robots( False )
    br.open(url)
    for form in br.forms():
        print form
    
    while(1):
        Name_Input_Field=raw_input("Enter Name of Input Field(If you want to stop the input, enter the q) : ")    
        if(Name_Input_Field=="q" or Name_Input_Field=="Q"):
            break
        nameList.append(Name_Input_Field)
        global count
        count+=1
        
    for name in nameList:
        value=raw_input("Input a value apply to "+name+" : ")
        valueList.append(value)
    
    br.select_form(nr=0)
    for i in range(0,count):
        try:
            br.form[nameList[i]]=valueList[i]
        except Exception, e:
            if "ListControl, must set a sequence" in str(e):
                br.form[nameList[i]]=[valueList[i],]
                pass
    br.submit()
    
def main():
    url=raw_input("Input URL(XSS Available) : ")
    attack(url)

if __name__=="__main__":
    main()