from scapy.all import *
from scapy.layers.inet import UDP

# 헤더 정의
header = {'service_id': None,
          'subscriber_id': None,
          'method_id': None,
          'event_id': None,
          'length': None,
          'client_id': None,
          'session_id': None,
          'protocol_ver': None,
          'interface_ver': None,
          'message_type': None,
          'return_code': None}


def print_header_val(*data):
    # data를 byte타입에서 hex타입으로 변경
    for i, key in enumerate(list(header.keys())):
        header[key] = data[i].hex()

    # 모든 데이터 출력
    for key, value in header.items():
        print('{0}: {1}'.format(key, value))

    print('')



def receive(msg):
    # sip_packet: payload에 담긴 값을 받아옴
    sip_packet = bytes(msg[UDP].payload)

    # message id
    service_id = sip_packet[0:2]
    subscriber_id = sip_packet[2:3]
    method_id = sip_packet[3:5]

    event_id = sip_packet[5:7]
    length = sip_packet[7:8]

    # request id
    client_id = sip_packet[8:10]
    session_id = sip_packet[10:12]

    protocol_ver = sip_packet[12:13]
    interface_ver = sip_packet[13:14]
    message_type = sip_packet[14:15]
    return_code = sip_packet[15:16]
    actual_data = sip_packet[16:].decode()

    print(actual_data) # 실제 데이터 출력
    
    # 헤더 값 출력
    print_header_val(service_id, subscriber_id, method_id, event_id, length, client_id, session_id,
                     protocol_ver, interface_ver, message_type, return_code)


if __name__ == '__main__':
    # udp port:138에서 데이터를 받아와 receive함수 실행
    sniff(count=0, prn=receive, filter='udp port 138')  # call back function
