from scapy.all import *
from scapy.contrib.automotive.someip import SOMEIP
from scapy.layers.inet import TCP, IP
from scapy.layers.l2 import Ether

logging.getLogger('scapy.runtime').setLevel(logging.ERROR)

target_ip = '192.168.0.102'
target_port = 49101
data = []


def start_tcp(target_ip, target_port):
    global sport, s_seq, d_seq  # 主要是用于TCP3此握手建立连接后继续发送数据
    # 第一次握手，发送SYN包
    # Ether(src="00:11:22:33:44:55", dst="55:44:33:22:11:00") /
    ether = Ether(src="54:05:db:8e:83:03", dst="aa:bb:cc:dd:ee:03")
    ip = IP(src="192.168.0.101", dst="192.168.0.102", flags=2)
    tcp = TCP(sport=55555, dport=49101, seq=RandInt(), ack=0, flags=0x02, window=8192)
    ans = srp(ether / ip / tcp, iface="Intel(R) Ethernet Connection (10) I219-V", verbose=False)
    print(ans[0][TCP][0])
    sport = ans[0][TCP][0][1].dport  # 源随机端口
    s_seq = ans[0][TCP][0][1].ack  # 源序列号（其实初始值已经被服务端加1）
    d_seq = ans[0][TCP][0][1].seq + 1  # 确认号，需要把服务端的序列号加1
    print(s_seq, d_seq)

    # # 第三次握手，发送ACK确认包
    # send(IP(dst=target_ip) / TCP(dport=target_port, sport=sport, ack=d_seq, seq=s_seq, flags='A'), verbose=False)
    tcp = TCP(sport=55555, dport=49101, seq=s_seq, ack=d_seq, flags=0x010)
    ans = srp(ether / ip / tcp, iface="Intel(R) Ethernet Connection (10) I219-V", verbose=False)
    # print(ans[0][IP][0][0].src)
    # sport = ans[0][TCP][0][0].dport  # 源随机端口
    # s_seq = ans[0][TCP][0][0].ack  # 源序列号（其实初始值已经被服务端加1）
    # d_seq = ans[0][TCP][0][0].seq + 1  # 确认号，需要把服务端的序列号加1
    # # print(s_seq, d_seq)
    # print(ans[0][TCP][0])


def trans_data(target_ip, target_port, data):
    # 先建立TCP连接
    start_tcp(target_ip=target_ip, target_port=target_port)
    # print sport,s_seq,d_seq
    # 发起GET请求
    ether = Ether(src="54:05:db:8e:83:03", dst="aa:bb:cc:dd:ee:03")
    ip = IP(src="192.168.0.101", dst="192.168.0.102")
    tcp = TCP(sport=55555, dport=49101, seq=s_seq, ack=d_seq, flags=0x018)

    someip = SOMEIP(srv_id=0x0100, sub_id=0x0,
                    method_id=0x3b, client_id=0x1, session_id=0x1,
                    msg_type=SOMEIP.TYPE_REQUEST, retcode=SOMEIP.RET_E_OK)
    ans = srp(ether / ip / tcp / someip, iface="Intel(R) Ethernet Connection (10) I219-V", verbose=False)
    print(ans[0][TCP][0])


if __name__ == '__main__':
    # start_tcp(target_ip, target_port)
    trans_data(target_ip, target_port, data)
