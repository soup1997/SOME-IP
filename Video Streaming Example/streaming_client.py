import cv2
import numpy as np
from scapy.all import *
import eth_scapy_someip as someip
from scapy.all import *
from scapy.layers.inet import UDP

header = {'service_id': None,
          'subscriber_id': None,
          'method_id': None,
          'event_id': None,
          'length': None,
          'client_id': None,
          'session_id':None,
          'protocol_ver': None,
          'interface_ver': None,
          'message_type': None,
          'return_code': None}

a = np.array([], np.uint8)
b = np.array([], np.uint8)
c = np.array([], np.uint8)
d = np.array([], np.uint8)
e = np.array([], np.uint8)
f = np.array([], np.uint8)
g = np.array([], np.uint8)  # np.uint8 important
h = np.array([], np.uint8)
i = np.array([], np.uint8)
j = np.array([], np.uint8)
k = np.array([], np.uint8)
l = np.array([], np.uint8)
m = np.array([], np.uint8)
n = np.array([], np.uint8)
o = np.array([], np.uint8)
p = np.array([], np.uint8)

def print_header_val(*data):
    for i, key in enumerate(list(header.keys())):
        header[key] = data[i].hex()
    
    for key, value in header.items():
        print('{0}: {1}'.format(key, value))
    
    print('')   
    
        
def receive(msg):
    global a, b, c, d, e, f, g, h, i, j, k, l, m, n, o, p
        
    sippacket = bytes(msg[UDP].payload)
    
    # message id
    service_id = sippacket[0:2]
    subscriber_id = sippacket[2:3]
    method_id = sippacket[3:5]
    
    event_id = sippacket[5:7]
    length = sippacket[7:8]
    
    # request id
    client_id = sippacket[8:10]
    session_id = sippacket[10:12]

    protocol_ver = sippacket[12:13]
    interface_ver = sippacket[13:14]
    message_type = sippacket[14:15]
    return_code = sippacket[15:16]
    
    img = np.array(list(raw(sippacket[16:])), dtype=np.uint8)

    
    if img[0] == 0:
        img = np.delete(img, 0)
        a = img
    elif img[0] == 1:
        img = np.delete(img, 0)
        b = img
    elif img[0] == 2:
        img = np.delete(img, 0)
        c = img
    elif img[0] == 3:
        img = np.delete(img, 0)
        d = img
    elif img[0] == 4:
        img = np.delete(img, 0)
        e = img
    elif img[0] == 5:
        img = np.delete(img, 0)
        f = img
    elif img[0] == 6:
        img = np.delete(img, 0)
        g = img
    elif img[0] == 7:
        img = np.delete(img, 0)
        h = img
    elif img[0] == 8:
        img = np.delete(img, 0)
        i = img
    elif img[0] == 9:
        img = np.delete(img, 0)
        j = img
    elif img[0] == 10:
        img = np.delete(img, 0)
        k = img
    elif img[0] == 11:
        img = np.delete(img, 0)
        l = img
    elif img[0] == 12:
        img = np.delete(img, 0)
        m = img
    elif img[0] == 13:
        img = np.delete(img, 0)
        n = img
    elif img[0] == 14:
        img = np.delete(img, 0)
        o = img
    elif img[0] == 15:
        img = np.delete(img, 0)
        p = img

    b_frame = np.concatenate((a, b, c, d, e, f, g))
    b_frame.resize((100, 100))
    
    b_frame = cv2.resize(b_frame, (480, 320), interpolation=cv2.INTER_LINEAR)
    cv2.imshow('img', b_frame)
        
    print_header_val(service_id, subscriber_id, method_id, event_id, length, client_id, session_id,
                   protocol_ver, interface_ver, message_type, return_code)
    
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        sys.exit()
    
if __name__=='__main__':
    sniff(count = 0, prn=receive, filter='udp port 138 or udp port 137') # call back function