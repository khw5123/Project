import pygame, wave, contextlib, os, time

wavFileList=[]

def setPlayTime(wavFile):
    with contextlib.closing(wave.open(wavFile, "r")) as f:
        frames=f.getnframes()
        rate=f.getframerate()
        duration=frames/float(rate)
        return int(duration)

def infiniteRepeatPlay():
    count=0
    while(1):
        os.system("cls")
        print "\n"+wavFileList[count]+" Playing..."
        pygame.mixer.init()
        pygame.mixer.music.load(wavFileList[count])
        pygame.mixer.music.play()
        time.sleep(setPlayTime(wavFileList[count])+3)
        if(count==len(wavFileList)-1):
            count=0
            continue
        count+=1

def repeatPlay(count):
    for i in range(1, count+1):
        for j in range(0, len(wavFileList)):
            os.system("cls")
            print "\n"+str(i)+"st Repeat\n"+wavFileList[j]+" Playing..."
            pygame.mixer.init()
            pygame.mixer.music.load(wavFileList[j])
            pygame.mixer.music.play()
            time.sleep(setPlayTime(wavFileList[j])+3)

def main():
    try:
        print "[Online Convert Site : https://convertio.co/kr/mp3-wav]"
        while(1):
            wavFile=raw_input("\nInput WAV File(If you have finished typing 'q'): ")
            if(wavFile=="q"):
                break
            if ".wav" not in wavFile:
                print "[-] Please input only wav file!"
                continue
            try:
                print "["+wavFile+"("+str(os.path.getsize(wavFile))+"Byte)] Added!"
                wavFileList.append(wavFile)
            except Exception, e:
                print "[-] ", e
                continue
        select=raw_input("\nEnter the number of times to repeat playback(Please do infinite iteration play and enter 0) : ")
        if(select=="0"):
            infiniteRepeatPlay()
        else:
            repeatPlay(int(select))
    except Exception, e:
        print "[-] ", e
        time.sleep(600)
        exit(0)
        
if __name__=="__main__":
    main()
