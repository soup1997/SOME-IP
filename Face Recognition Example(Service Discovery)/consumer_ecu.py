from scapy.all import *
from scapy.layers.inet import UDP, IP
from scapy.layers.l2 import Ether
import eth_scapy_sd as sd

class service_discovery:
    def __init__(self):
        self.sdp = sd.SD()
        
        self.srv_id = 0x1111
        self.n_opt_1 = 1
        self.inst_id = 0xffff
        self.major_ver = 0x03
        self.cnt = 0x0
        self.ttl = 0x05
        self.eventgroup_id = 0x04
        
        self.sd_entry_array = {'service_id': None,
                  'instance_id': None,
                  'major_ver':None,
                  'TTL': None,
                  'Reserved': None,
                  'IDR_FLAG, Reserved2': None,
                  'EventGroup_ID': None,
                  }
        
        self.sd_options_array = {'Length': None,
                    'Type': None,
                    'Reserved': None,
                    'IPV4_Address': None,
                    'Reserved2': None,
                    'L4_Proto': None,
                    'Port_Number': None
                    }
        self.set_array()
  
  
    def set_array(self):
        entry_array = [sd.SDEntry_EventGroup(srv_id=self.srv_id, n_opt_1=self.n_opt_1,
                               inst_id=self.inst_id, major_ver=self.major_ver,
                               eventgroup_id = self.eventgroup_id, cnt=self.cnt,
                               ttl=self.ttl)]
        self.sdp.setEntryArray(entry_array)
        self.sdp.entry_array[0].type = None
        
        option_array = [sd.SDOption_IP4_EndPoint(addr='192.168.0.13', l4_proto=0x11, port=0xd903)]
        self.sdp.setOptionArray(option_array)


    def print_val(self, *data, array_type):
        for i, key in enumerate(list(array_type.keys())):
            array_type[key] = data[i].hex()
        
        for key, value in array_type.items():
            print('{0}: {1}'.format(key, value))


    def receive(self, msg):
        sippacket = bytes(msg[UDP].payload)
        
        # SD Entry Array
        self.sdp.entry_array[0].type = int.from_bytes(sippacket[24:25], byteorder='little')
        
        service_id = sippacket[28:30]
        instance_id = sippacket[30:32]
        major_ver = sippacket[32:33]
        ttl = sippacket[33:36]
        reserved = sippacket[36:37]
        reserved2 = sippacket[37:38]
        eventgroup_id = sippacket[38:40]
        
        self.print_val(service_id, instance_id, major_ver, ttl, reserved, reserved2,
                  eventgroup_id, array_type=self.sd_entry_array)
        
        # SD Options Array
        length = sippacket[44:46]
        sd_type = sippacket[46:47]
        reserved = sippacket[47:48]
        ipv4_addr = sippacket[48:52]
        reserved2 = sippacket[52:53]
        l4_proto = sippacket[53:54]
        port_num = sippacket[54:56]
        
        self.print_val(length, sd_type, reserved, ipv4_addr, reserved2,
                  l4_proto, port_num, array_type=self.sd_options_array)
        
        try:
            data = sippacket[56:].decode()
            print(data)
        
        except UnicodeDecodeError:
            pass
        
        finally:
            self.comm()
        
    def comm(self):
        s = Ether() / IP(src = '192.168.0.7', dst='192.168.0.13') / UDP(sport=5355, dport=138) / self.sdp.getSomeip(True)
        
        if self.sdp.entry_array[0].type is None: # find service
            s['SD'].entry_array[0].type = sd.SDEntry_Service.TYPE_SRV_FINDSERVICE
            print("Sending Find Service")
            sendp(s, count=1)
        
        elif self.sdp.entry_array[0].type == sd.SDEntry_Service.TYPE_SRV_OFFERSERVICE:
            s['SD'].entry_array[0].type = sd.SDEntry_Service.TYPE_EVTGRP_SUBSCRIBE
            print("Receiving Offer Service")
            print("Sending Subscribe EventGroup")
            sendp(s, count=1)
        
        elif self.sdp.entry_array[0].type == sd.SDEntry_Service.TYPE_EVTGRP_SUBSCRIBE_ACK:
            print("Receiving Subscribe EventGroup ACK")
            
if __name__ == '__main__':
    someip_sd = service_discovery()
    someip_sd.comm()
    sniff(count=0, prn=someip_sd.receive, filter='udp port 138')
