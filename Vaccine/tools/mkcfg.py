#-*- coding: utf-8 -*-
import os
import glob
import hashlib

def main():
    file_scan_list = [] # 리스트에 존재하는 모든 폴더안에 있는 파일에 대해 update.cfg 내용을 설정
    while True:
        dirName = raw_input('Input Folder(q : quit, enter : default) : ')
        if(dirName.lower() == 'q' or dirName.lower() == 'quit'):
            break
        elif(dirName.lower() == ''):
            file_scan_list.append('.')
            break
        else:
            if os.path.isdir(dirName) == True:
                file_scan_list.append(dirName)
            else:
                print "Not Appended!"
    while len(file_scan_list) != 0:
        real_name = file_scan_list.pop(0)
        if os.path.isdir(real_name) == True:
            flist = glob.glob(real_name + '/*')
            file_scan_list += flist
        else:
            fp = open(real_name, 'rb')
            data = fp.read()
            fp.close()
            s = hashlib.sha1()
            s.update(data)
            hash = s.hexdigest()
            real_name = real_name.split('engine')
            file_name = 'engine'+ real_name[1].replace('.\\', '')
            str = hash + ' ' + file_name
            fp = open('update.cfg', 'at')
            fp.write(str + '\n')
            fp.close()
            print str
    
if __name__ == "__main__":
    main()
