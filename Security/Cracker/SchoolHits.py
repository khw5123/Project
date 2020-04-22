#-*- coding: utf-8 -*-
import urllib2, time

notice1 = 'http://www.hknu.ac.kr/web/kor/p_01_01?p_p_id=BBS_1_INSTANCE_l6Yz&p_p_lifecycle=0&_BBS_1_INSTANCE_l6Yz_struts_action=%2Fext%2Fnotice%2Fview_message&_BBS_1_INSTANCE_l6Yz_messageId=' # 한경공지
notice2 = 'http://www.hknu.ac.kr/web/kor/p_01_02?p_p_id=BBS_1_INSTANCE_N2qT&p_p_lifecycle=0&_BBS_1_INSTANCE_N2qT_struts_action=%2Fext%2Fnotice%2Fview_message&_BBS_1_INSTANCE_N2qT_messageId=' # 학사공지
notice3 = 'http://www.hknu.ac.kr/web/kor/p_01_03?p_p_id=BBS_1_INSTANCE_o79E&p_p_lifecycle=0&_BBS_1_INSTANCE_o79E_struts_action=%2Fext%2Fnotice%2Fview_message&_BBS_1_INSTANCE_o79E_messageId=' # 취업공지
count = 0

def hits(noticeType, messageId):
    try:
        global count
        url = ''
        if(noticeType == '1'):
            url = notice1 + messageId
        elif(noticeType == '2'):
            url = notice2 + messageId
        elif (noticeType == '3'):
            url = notice3 + messageId
        else:
            print '[-] Notice Type Error! Please Choose from 1, 2, 3.'
            time.sleep(600)
            exit(0)
        request = urllib2.Request(url)
        data = urllib2.urlopen(request).read()
        if((len(data) > 18500) and (len(data) < 18700)):
            print '[-] messageId Error! No such messageId.'
            time.sleep(600)
            exit(0)
        else:
            count += 1
            print '[+] Hits : '+str(count)
    except Exception, e:
        print '[-] ', e
        time.sleep(600)
        exit(0)

def main():
    try:
        noticeType = raw_input('한경공지(1), 학사공지(2), 취업공지(3) : ')
        messageId = raw_input('게시판 messageId 입력 : ')
        hitsCount = raw_input('올릴 조회수 입력 : ')
        for hit in range(0, int(hitsCount)):
            hits(noticeType, messageId)
            time.sleep(0.1)
    except Exception, e:
        print '[-] ', e
        time.sleep(600)
        exit(0)

if __name__ == '__main__':
    main()