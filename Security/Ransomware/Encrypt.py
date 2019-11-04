#-*- coding: utf-8 -*-
import Crypto, hashlib, time
import Crypto.Random
from Crypto.Cipher import AES

key="myKeyValue" # 암호화에 사용될 키 값
InitializationVector="1234567890123456" # 초기화 벡터로 CBC(Cipher Block Chaining) Mode로 암호화 하므로 초기화 벡터는 16Byte가 되야함
FileName="" # 암호화 할 파일명

def gen_sha256_hashed_key_salt(key): # SHA(256) 해시 함수
    salt1=hashlib.sha256(key).digest() # 설정한 Key를 해싱해 솔트 값 생성
    return hashlib.sha256(salt1+key).digest() # 생성한 솔트 값과 설정한 Key를 합해 해싱

def AES256Encrypt(key, plain): # AES 암호화 방식으로 256Byte Key를 사용하여 암호화 하는 함수
    length=AES.block_size-(len(plain)%AES.block_size) # 각 블록을 16Byte 로 맞춰줘야 하므로 마지막 블록이 16Byte 가 아닐 경우 부족한 바이트 수를 구해서
    plain+=chr(length)*length # 부족한 바이트 수만큼 더해서 마지막 블록을 16Byte 로 맞춤
    iv=InitializationVector # 초기화 벡터 설정
    encryptor=AES.new(gen_sha256_hashed_key_salt(key), AES.MODE_CBC, IV=iv) # SHA(256) 해시 함수로 메세지 다이제스트 생성, 블록 암호화 방식 중 하나인 CBC(Cipher Block Chaining) 사용 
    return {'cipher': encryptor.encrypt(plain), 'iv': iv} # 암호화 후 값 반환

def main():
    fp=open(FileName, "rb") # 파일을 열여서 평문(원본 프로그램의 바이너리)을 얻음
    FileBinary=fp.read()
    fp.close()
    encrypted=AES256Encrypt(key, FileBinary) # 키 값을 이용해 바이너리를 암호화
    fp=open(FileName, "wb") # 파일을 열어서 암호문(암호화된 바이너리)을 덮음
    fp.write(encrypted['cipher'])
    fp.close()
    
if __name__=="__main__":
    main()
