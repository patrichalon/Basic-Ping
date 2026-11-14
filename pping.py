__author__ = "Alon Patrich"
__copywrite__ = "Patrich LTD by Alon Patrich"

import socket
import sys # for launch arguments and ip 
import threading
import struct
import time
import os

"""
this is a standard code for the ping command on windows
"""

#vars: 
packet_size = 32 # in bytes. can change based on flag -n
number_of_packets  = 4 # can change based on flag -p

def ping(dest_ip : str , count : int):
    """
    send pack purpose is to send 4 to the target. 
    """
    icmp_type = 8
    icmp_code = 0
    checksum = 0
    packet_id = os.getpid() & 0xFFFF
    sequence = 1
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    sock.settimeout(2.5)
    packet_id = os.getpid() & 0xFFFF
    #instilize a socket that uses imcp as protocol (level bellow tcp and udp)

    print(f"Pinging {dest_ip}:")

    for seq in range(1, count + 1):
        # 1. Build packet with current timestamp
        send_time = time.time()
        payload = struct.pack("!d", send_time) + b"ping_test"
        temp_header = struct.pack("!BBHHH", 8, 0, 0, packet_id, seq)
        checksum = calculate_checksum(temp_header + payload)
        packet = struct.pack("!BBHHH", 8, 0, checksum, packet_id, seq) + payload

        # 2. Send packet
        sock.sendto(packet, (dest_ip, 0))
        try:
                while True:
                    raw_data, addr = sock.recvfrom(1024)
                    recv_time = time.time()

                    # Extract TTL from the 9th byte of the 20-byte IP header
                    ttl = raw_data[8]

                    # Extract the 8-byte ICMP header starting at byte 20
                    icmp_type, code, _, recv_id, recv_seq = struct.unpack(
                        "!BBHHH", raw_data[20:28]
                    )

                    # Ignore ICMP packets meant for other programs
                    if icmp_type == 0 and recv_id == packet_id and recv_seq == seq:
                        rtt = (recv_time - send_time) * 1000
                        print(
                            f"Reply from {addr[0]}: bytes={len(raw_data)-20} time={rtt:.2f}ms TTL={ttl}"
                        )
                        break

        except socket.timeout:
                print("Request timed out.")

        time.sleep(1)  # Wait 1 second before the next ping



def calculate_checksum(data: bytes) -> int:
    # 1. If the length is odd, pad with one zero byte
    if len(data) % 2 != 0:
        data += b"\x00"

    total = 0
    # 2. Sum all 16-bit (2-byte) chunks in network byte order (big-endian)
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + data[i + 1]
        total += word

    # 3. Fold any overflow bits beyond 16 bits back into the lower 16 bits
    while total >> 16:
        total = (total & 0xFFFF) + (total >> 16)

    # 4. Take the one's complement (flip all bits) and mask to 16 bits
    checksum = ~total & 0xFFFF
    return checksum

def help():
    print("Usage: pping.py <flags> <destination>")
    print("     *flags isn't mandatory but destination is.")


if __name__ == "__main__":
    args = sys.argv
    if(len(args) < 2):
        print("Not enough arguments given to the program")
        help() #print help message and return
        sys.exit(1)
    
        
    #in the sys argv after run the argv[0] is pping.py and then the next are actual program args
    ping(sys.argv[-1], 4)
    #the last argument is expected to be the destination.


    
