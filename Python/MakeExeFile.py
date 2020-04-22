#-*- coding: utf-8 -*-
import subprocess, time
'''
#-*- coding: utf-8 -*-
from distutils.core import setup
import py2exe   #윈도우 실행파일로 변환하는 모듈(python홈 디렉터리에 백도어클라이언트.py와 이 파일을 컴파일한 파일을 같이 넣고 cmd에서 python.exe -u ChangeWindowEXE.py py2exe 입력후 새로 생성된 dist디렉터리안의 변환된exe파일 확인)

options={
         "bundle_files" : 1, #번들링 여부 결정 : 파이썬 인터프리터까지 번들링(1), 기본 번들링(2), 번들링 안함(3)
         "compressed" : 1, #라이브러리 아카이브를 압축할건지 결정 : 압축(1), 압축안함(2)
         "optimize" : 2, #코드를 최적화할건지 결정 : 최적화안함(0), 일반적 최적화(1), 추가 최적화(2) 
         "dll_excludes": ["w9xpopen.exe"] #제거할 파일 목록
}
setup(
      console=["Shell_code.py"], #콘솔 exe로 변환할 코드목록(리스트)
      options={"py2exe" : options}, #컴파일에 필요한 옵션 지정
      zipfile=None #실행에 필요한 모듈을 zip파일로 묶되, None은 실행파일로만 묶음
)
'''
def main():
    exeFile=raw_input("Input python.exe File Location : ")
    pyFile=raw_input("Input py File Location : ")
    try:
        string='from distutils.core import setup\n'
        string+='import py2exe\n\n'
        string+='options={"bundle_files" : 1, "compressed" : 1, "optimize" : 2, "dll_excludes": ["w9xpopen.exe"]}\n'
        string+='setup(console=["'+pyFile+'"], options={"py2exe" : options}, zipfile=None)'
        directory=""
        for i in range(len(exeFile.split("\\"))-1):
            directory+=exeFile.split("\\")[i]+"\\"
        makeExeFile=directory+"makeExeFile.py"
        fp=open(makeExeFile, "w")
        fp.write(string)
        fp.close()
        subprocess.call(exeFile+" -u "+makeExeFile+" py2exe", shell=True)
        print "\n[+] Open the [CurrentDirectory]\dist"
        time.sleep(30)
    except Exception, e:
        print "[-] ", e 
        time.sleep(30)
        exit(0)     
            
if __name__=="__main__":
    main()