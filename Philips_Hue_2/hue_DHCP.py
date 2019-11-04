import socket
import struct
import time
from phue import Bridge

b = Bridge('192.168.0.19')
b.connect()
lights = b.lights

def main() :
    raw_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))
    value = False
    mymac_address = b'\x00\xcd\x98T\xea*'
    start = time.time()
    while True :
        recv_packet = raw_socket.recvfrom(5000)

        ethernet_protocol = struct.unpack('!6s6sH', (recv_packet[0])[:14])[2]
        mac_address = struct.unpack('!6s6sH', (recv_packet[0])[:14])[1]
        if mac_address == mymac_address :
            start = time.time()
            if ethernet_protocol == 0x800 :
                ip_protocol = struct.unpack('!BBHHHBBH4s4s', recv_packet[0][14:34])[6]
                if ip_protocol == 17 :
                    udp_src_port = struct.unpack('!H', (recv_packet[0])[34:34+2])[0]
                    if udp_src_port == 68 :
                        value = True
                        setLight(value)

        end = time.time()
        checktime = end - start
        if checktime > 2 :
            if value is True :
                value = False
                setLight(value)

def setLight(value) :
    for i in range(0, 3) :
        lights[i].on = value

if __name__ == '__main__' :
    main()
