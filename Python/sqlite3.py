# -*- coding: utf-8 -*-
import sqlite3

def query(conn, cur, sql):
    try:
        cur.execute(sql)
        if 'select' in sql.lower()[0:6]:
            for description in cur.description:
                print(description[0] + '\t', end='')
            print('')
            while True:
                data = cur.fetchone()
                if data == None:
                    break
                for i in range(0, len(data)):
                    print(data[i], end='\t')
                print('')
        else:
            conn.commit()
    except Exception as e:
        print('\n[-]', e)

def main():
    databaseFile = input('Input Database File : ')
    conn = sqlite3.connect(databaseFile)
    cur = conn.cursor()
    while True:
        print('\n[Select]\n1. Query\n2. Exit')
        sel= input('Select : ')
        if sel == '1':
            sql = input('Input Query : ')
            query(conn, cur, sql)
        elif sel == '2':
            break
        else:
            print('Input Error')
    conn.close()

if __name__ == '__main__':
    main()