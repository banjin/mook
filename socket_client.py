# coding:utf-8

import socket
import sys
MSGLEN = 1024


class Client(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def connect(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.host, self.port))
        sock.send('hi there, server')


class MyClient(object):
    '''demonstration class only
      - coded for clarity, not efficiency
    '''

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def mysend(self, msg):
        totalsent = 0
        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def myreceive(self):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - bytes_recd, 2048))
            if chunk == '':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        return ''.join(chunks)


def client(host, port):
    import time
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    print('Client has been assigned')
    i = 0
    all_data = []
    a = '{"ip":"10.10.10.105","scan_start_time":1513940970,"scan_end_time":1514259654,"provider_id":"bmh","vuln_name":"MySQL弱口令","scan_type":"漏洞专扫","level":"高危","risk_url":"10.10.10.105:3306/?user=root\u0026password=1qaz2wsx","custom_name":"10.10.10.105","desc":"存在mysql弱口令，攻击者能够轻松窃取数据","harm_content":"黑客可以轻易破解密码，从而控制mysql服务","solution":"增强口令强度","threat_type":"其他","port":"3306"}\n'
    for i in range(20000):
        all_data.append(a)
    data_str = ''.join(all_data)
    start_time = time.time()

    #while i<100:
    #    time.sleep(0.00005)
        #msg = sys.stdin.readline()
        #print "msg....", msg
    #    sock.sendall('{"ip":"10.10.10.105","scan_start_time":1513940970,"scan_end_time":1514259654,"provider_id":"bmh","vuln_name":"MySQL弱口令","scan_type":"漏洞专扫","level":"高危","risk_url":"10.10.10.105:3306/?user=root\u0026password=1qaz2wsx","custom_name":"10.10.10.105","desc":"存在mysql弱口令，攻击者能够轻松窃取数据","harm_content":"黑客可以轻易破解密码，从而控制mysql服务","solution":"增强口令强度","threat_type":"其他","port":"3306"}\n')
    #    i+=1
    sock.sendall(data_str)
        #print i
        #print("send")
        # reply = sock.recv(10)
        # print('reply..', reply)
    # with open('rule.json') as f:
    #     for line in f.readlines():
    #         print "line",line
    #         sock.sendall(line)
    end_time = time.time()
    print "cost:", end_time - start_time

if __name__ == "__main__":

    client('40.125.161.143', 6666)
