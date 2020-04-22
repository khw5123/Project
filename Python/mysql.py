#-*- coding: utf-8 -*-
import pymysql

addressDB="" # DB 서버IP
portDB= # DB 접속 포트
accountDB="" # DB 접속 계정
passwordDB="" # DB 접속 패스워드
nameDB="" # DB 이름
listDB=[ ["mysql", ["user", "password"]], ["",["", "","",...]] ] # DB - Tables 매칭 리스트

def main():
    conn=pymysql.connect(host=addressDB, port=portDB, user=accountDB, password=passwordDB, db=nameDB, charset="utf8") # MySQL Connection 연결
    curs=conn.cursor() # Connection 으로부터 Cursor 생성
    
    # 데이터베이스 목록 조회
'''
    curs.execute("show databases")
    rows=curs.fetchall() # 데이터 Fetch (모든 데이터를 한번에 가져올 때 사용), fetchone() 은 한번 호출에 하나의 Row를 가져옴, fetchmany(n) 은 한번에 n개 만큼의 데이터를 가져올 때 사용 
    for index in range(0, len(rows)):
        print rows[index]
'''
    # 데이터베이스 생성
'''
    createDBName=""
    curs.execute("create database %s" % createDBName)
'''
    # 데이터베이스 삭제
'''
    dropDBName=""
    curs.execute("drop database %s" % dropDBName)
'''
    # 테이블 목록 조회
'''
    dbName=""
    curs.execute("use %s" % dbName)
    curs.execute("show tables")
    rows=curs.fetchall()
    for index in range(0, len(rows)):
        print rows[index]
'''
    # 테이블 생성
'''
    dbName=""
    curs.execute("use %s" % dbName)
    createTableName=""
    createColumnName1=""
    createColumnName2=""
    createDataType1="varchar(20)"
    createDataType2="int(15)"
    createSQL="create table %s (%s %s, %s %s)" % (createTableName, createColumnName1, createDataType1, createColumnName2, createDataType2) 
    curs.execute(createSQL)
'''
    # 테이블 삭제
'''
    dbName=""
    curs.execute("use %s" % dbName)
    dropTableName=""
    curs.execute("drop table %s" % dropTableName)
'''
    # 테이블명 변경
'''
    dbName=""
    curs.execute("use %s" % dbName)
    oldTableName=""
    newTableName=""
    curs.execute("rename table %s to %s" % (oldTableName, newTableName))
'''
    # 테이블 내 칼럼 정보 확인
'''
    dbName=""
    curs.execute("use %s" % dbName)
    tableName=""
    curs.execute("describe %s" % tableName)
    rows=curs.fetchall()
    print "[Field    Type    Null    Key    Default    Extra]"
    for index in range(0, len(rows)):
        print rows[index]
'''
    # 테이블 내 칼럼 추가
'''
    dbName=""
    curs.execute("use %s" % dbName)
    tableName=""
    createColumnName=""
    createDataType="int(5)"
    alterSQL="alter table %s add %s %s" % (tableName, createColumnName, createDataType)
    curs.execute(alterSQL)
'''
    # 테이블 내 칼럼 삭제
'''
    dbName=""
    curs.execute("use %s" % dbName)
    tableName=""
    dropColumnName=""
    alterSQL="alter table %s drop %s" % (tableName, dropColumnName)
    curs.execute(alterSQL)
'''
    # 테이블 내 칼럼 자료형 수정
'''
    dbName=""
    curs.execute("use %s" % dbName)
    tableName=""
    columnName=""
    modifyDataType="varchar(25)"
    alterSQL="alter table %s modify %s %s" % (tableName, columnName, modifyDataType)
    curs.execute(alterSQL)
'''
    # SELECT
'''
    dbName=""
    curs.execute("use %s" % dbName)
    tableName=""
    selectSQL="select * from %s" % tableName
    curs.execute(selectSQL)
    rows=curs.fetchall() 
    print rows
'''
    # INSERT
'''
    dbName=""
    curs.execute("use %s" % dbName)
    tableName=""
    column1=""
    column2=
    record1=""
    record2=
    insertSQL="insert into %s (%s, %d) values ('%s', '%d')" % (tableName, tableName, column1, column2, record1, record2)
    curs.execute(insertSQL)
    conn.commit()
'''
    # UPDATE
'''
    dbName=""
    curs.execute("use %s" % dbName)
    tableName=""
    columnName=""
    newRecord=""
    originRecord=""
    updateSQL="update %s set %s='%s' where %s='%s'" % (tableName, columnName, newRecord, columnName, originRecord)
    curs.execute(updateSQL)
    conn.commit()
'''
    # DELETE
'''
    dbName=""
    curs.execute("use %s" % dbName)
    tableName=""
    deleteColumnName=""
    deleteRecord=
    deleteSQL="delete from %s where %s=%d" % (tableName, deleteColumnName, deleteRecord)
    curs.execute(deleteSQL)
    conn.commit()
'''
    conn.close() # 연결 해제
    
if __name__=="__main__":
    main()
