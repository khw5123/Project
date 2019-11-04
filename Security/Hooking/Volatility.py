#-*- coding: utf-8 -*-
import sys, time
import volatility
import volatility.conf as conf
import volatility.registry as registry
import volatility.commands as commands
import volatility.addrspace as addrspace
from volatility.plugins.registry.registryapi import RegistryApi
from volatility.plugins.registry.lsadump import HashDump

try:
    sys.path.append("C:\\Python27\\Lib\\site-packages\\volatility") # volatility 경로
    memory_file=raw_input("Input Memory Image File( ex) .vmem ) :  ") # 분석할 메모리 이미지
    registry.PluginImporter()
    config=conf.ConfObject()
    config.parse_options()
    config.PROFILE=raw_input("Input Profile( ex) WinXPSP2x86) : ") # https://github.com/volatilityfoundation/volatility
    config.LOCATION=memory_file
    registry.register_global_options(config, commands.Command)
    registry.register_global_options(config, addrspace.BaseAddressSpace)
    registry=RegistryApi(config) 
    registry.populate_offsets() # populate_offsets 함수는 hivelist 명령을 실행하는 작업을 수행한다.
    sam_offset=None
    sys_offset=None
    for offset in registry.all_offsets: # 발견된 하이브를 모두 확인
        if registry.all_offsets[offset].endswith("\\SAM"): # SAM 하이브를 찾는다.
            sam_offset=offset
            print "[+] SAM : 0x%08x" % offset
        if registry.all_offsets[offset].endswith("\\system"): # SYSTEM 하이브를 찾는다.
            sys_offset=offset
            print "[+] System : 0x%08x" % offset
        if sam_offset is not None and sys_offset is not None: # 두 하이브를 찾았을 경우
            config.sys_offset=sys_offset # config 객체에 오프셋 저장 
            config.sam_offset=sam_offset
            hashdump=HashDump(config) # HashDump 객체 생성
            for hash in hashdump.calculate(): # 결과 출력
                print hash
            break
    if sam_offset is None or sys_offset is None:
        print "[-] Failed to find the system or SAM offsets."
    time.sleep(30)
except Exception, e:
    print "[-] ", e 
    time.sleep(30)
    exit(0)