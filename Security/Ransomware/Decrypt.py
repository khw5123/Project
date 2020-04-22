#-*- coding: utf-8 -*-
import Crypto, hashlib, time
import Crypto.Random
from Crypto.Cipher import AES

key="myKeyValue" # 암호화에 사용된 키 값으로 복호화에도 필요함
InitializationVector="1234567890123456" # 암호화에 사용된 초기화 벡터로 복호화에도 필요함
FileName="" # 복호화 할 파일명

def gen_sha256_hashed_key_salt(key): # SHA(256) 해시 함수
    salt1=hashlib.sha256(key).digest() # 설정한 Key를 해싱해 솔트 값 생성
    return hashlib.sha256(salt1+key).digest() # 생성한 솔트 값과 설정한 Key를 합해 해싱

def AES256Decrypt(key, iv, cipher): # 복호화 함수
    decryptor=AES.new(gen_sha256_hashed_key_salt(key), AES.MODE_CBC, IV=iv) # SHA(256) 해시 함수로 메세지 다이제스트 생성, 블록 암호화 방식 중 하나인 CBC(Cipher Block Chaining) 사용 
    plain=decryptor.decrypt(cipher) # 복호화 후 평문 얻음
    plain=plain[0:-ord(plain[-1])]
    return plain # 평문 반환

def main():
    fp=open(FileName, "rb") # 파일을 열어서 암호문(암호화된 바이너리)을 얻음
    FileBinary=fp.read()
    fp.close()
    decrypted=AES256Decrypt(key, InitializationVector, FileBinary) # 키 값과 초기화 벡터를 이용해 바이너리를 복호화
    #decrypted=AES256Decrypt(key, encrypted['iv'], encrypted['cipher'])
    fp=open(FileName, "wb") # 파일을 열어서 평문(복호화된 바이너리=원본 프로그램의 바이너리)을 덮음
    fp.write(decrypted)
    fp.close()
    
if __name__=="__main__":
    main()
