#!/usr/bin/python2.7
import dpkt
import sys
import socket

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
                        if syn_flag and ack_flag:
                            dst = inet_to_str(ip.dst)
                            if not ips.has_key(dst):
                                ips[dst] = 0
                            ips[dst] -= 3 # each syn+ack has a weight of -3
                        elif syn_flag:
                            src = inet_to_str(ip.src)
                            if not ips.has_key(src):
                                ips[src] = 0
                            ips[src] += 1 # each syn has a weight of +1
            except:
                pass # ignore exceptions

    for key in ips:
        if ips[key] > 0: # true when there are more syns that 3 * syn+acks
            print key

    sys.exit(0)

if __name__ == '__main__':
    main()
