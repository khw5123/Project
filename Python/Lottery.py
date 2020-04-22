from random import randint 

def lottery():
    com=[]
    i=0
    while(i<7):
        com.append(randint(1,45))
        for j in range(0,i):
            if(com[i]==com[j]):
                com.pop()
                i-=1
        i+=1
    sel=[]
    i=0
    print "\n[Enter the number seven(1~45)]"
    while(i<6):
        count=i+1
        num=raw_input("Input Number["+str(count)+"] : ")
        sel.append(int(num))    
        if(sel[i]>45 or sel[i]<1):
            print "[-] Input out of range, Enter another number in the range"
            sel.pop()
            i-=1
        for j in range(0,i):
            if(sel[j]==sel[i]):
                print "[-] Duplicate input, Enter another number"
                sel.pop()
                i-=1
                break
        i+=1
    sameCount=0
    for i in range(0,6): 
        for j in range(0,6): 
            if(com[i]==sel[j]):
                sameCount+=1
    bonusCount=0
    for i in range(0,6):
        if(com[6]==sel[i]):
            bonusCount+=1
    print "\nChoose your numbers : ",sel
    print "Winning numbers(Last number is bonus number) : ",com
    if(sameCount==6):
        if(bonusCount==0):
            print "[+] Your ranking : [1]"
    elif(sameCount==5): 
            if(bonusCount==1):
                print "[+] Your ranking : [2]"
            elif(bonusCount==0):
                print "[+] Your ranking : [3]"
    elif(sameCount==4): 
        print "[+] Your ranking : [4]"
    elif(sameCount==3):
        print "[+] Your ranking : [5]"
    else: 
        print "[+] Your ranking : Washout"

def lotteryAuto():
    count=raw_input("\nEnter the number : ")
    for a in range(0,int(count)):
        sel=[]
        i=0
        while(i<6):
            sel.append(randint(1,45))
            for j in range(0,i):
                if(sel[i]==sel[j]):
                    sel.pop()
                    i-=1
            i+=1
        print sel
    print ""
     
def frequencyCheck():
    frq=raw_input("\nThe frequency input(The higher it is accurate) : ")
    confirm=[]
    for i in range(0,45):
        confirm.append(0)
    for k in range(0,int(frq)): 
        i=0
        com=[]
        while(i<7):
            com.append(randint(1,45))
            for j in range(0,i):
                if(com[i]==com[j]):
                    com.pop()
                    i-=1
            i+=1
        for a in range(1,46):
            for b in range(0,7):
                if(com[b]==a):
                    confirm[a-1]+=1
    for i in range(0,45):
        count=i+1
        print "["+str(count)+"] : "+str(confirm[i])

def main():
    while(1):
        sel=raw_input("\n[Options]\n1. Simulation\n2. Auto\n3. Frequency Check\n4. Quit\nChoice : ")
        if(sel=="1"):
            lottery()
        elif(sel=="2"):
            lotteryAuto()
        elif(sel=="3"):
            frequencyCheck()
        elif(sel=="4"):
            break
        else:
            print"Only from 1, 2, 3, 4 input"
   
if __name__=="__main__":
    main()