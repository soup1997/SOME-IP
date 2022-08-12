from scapy.all import *
from scapy.layers.inet import UDP

sd_entry_array = {'service_id': None,
                  'instance_id': None,
                  'major_ver':None,
                  'TTL': None,
                  'Reserved': None,
                  'IDR_FLAG, Reserved2': None,
                  'EventGroup_ID': None,
                  }

sd_options_array = {'Length': None,
                    'Type': None,
                    'Reserved': None,
                    'IPV4_Address': None,
                    'Reserved': None,
                    'L4_Proto': None,
                    'Port_Number': None
                    }

def print_val(*data, array_type):
    for i, key in enumerate(list(array_type.keys())):
        array_type[key] = data[i].hex()
    
    for key, value in array_type.items():
        print('{0}: {1}'.format(key, value))
    
    print('')


def receive(msg):
    sippacket = bytes(msg[UDP].payload)
    
    # SD Entry Array
    service_id = sippacket[28:30]
    instance_id = sippacket[30:32]
    major_ver = sippacket[32:33]
    ttl = sippacket[33:36]
    reserved = sippacket[36:37]
    reserved2 = sippacket[37:38]
    eventgroup_id = sippacket[38:40]
    
    print_val(service_id, instance_id, major_ver, ttl, reserved, reserved2,
              eventgroup_id, array_type=sd_entry_array)
    
    # SD Options Array
    length = sippacket[45:47]
    sd_type = sippacket[47:48]
    reserved = sippacket[48:49]
    ipv4_addr = sippacket[49:53]
    reserved2 = sippacket[53:54]
    l4_proto = sippacket[54:55]
    port_num = sippacket[55:56]
    
    print_val(length, sd_type, reserved, ipv4_addr, reserved2,
              l4_proto, port_num, array_type=sd_options_array)
    
    data = sippacket[56:].decode()
    print(data)
    
if __name__=='__main__':
    sniff(count=0, prn=receive, filter='udp port 138')