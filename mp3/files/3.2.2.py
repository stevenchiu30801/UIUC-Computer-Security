#!/usr/bin/python2.7
import dpkt
import sys
import socket

class packetCounter:
    syn = 0
    synack = 0

def inet_to_str(inet):
    try:
        return socket.inet_ntop(socket.AF_INET, inet)
    except ValueError:
        return socket.inet_ntop(socket.AF_INET6, inet)

def main():
    if (len(sys.argv) < 2):
        print "error: need argument"
        sys.exit(1)

    filename = sys.argv[1]
    ips = {} # empty dict

    with open(filename) as f:
        pcap = dpkt.pcap.Reader(f)
        for _, buf in pcap:
            try:
                eth = dpkt.ethernet.Ethernet(buf)
                if isinstance(eth.data, dpkt.ip.IP): # is IP?
                    ip = eth.data
                    if ip.p == dpkt.ip.IP_PROTO_TCP: # is TCP?
                        tcp = ip.data
                        syn_flag = ( tcp.flags & dpkt.tcp.TH_SYN ) != 0
                        ack_flag = ( tcp.flags & dpkt.tcp.TH_ACK ) != 0
                        if syn_flag and ack_flag: # add dst to dict and synack++
                            dst = inet_to_str(ip.dst)
                            if not ips.has_key(dst):
                                ips[dst] = packetCounter()
                            ips[dst].synack += 1
                        elif syn_flag: # add src to dict and syn++
                            src = inet_to_str(ip.src)
                            if not ips.has_key(src):
                                ips[src] = packetCounter()
                            ips[src].syn += 1
            except:
                pass # ignore exceptions

    for key in ips:
        if ips[key].synack * 3 < ips[key].syn:
            print key

    sys.exit(0)

if __name__ == '__main__':
    main()
