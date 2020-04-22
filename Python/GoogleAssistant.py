# -*- coding: utf-8 -*-
import os

def main():
    json_file = ''
    files = os.listdir('D:\\Python\\Workspace\\Google')
    for f in files:
        if 'client_secret' in f:
            json_file = f
            break
    fp = open(json_file, 'r')
    project_id = fp.read().split('project_id')[1].split('"')[2]
    fp.close()
    os.system('C:\Python27\Scripts\googlesamples-assistant-pushtotalk.exe --device-model-id \'myModel\' --project-id ' + project_id)

if __name__ == '__main__':
    main()