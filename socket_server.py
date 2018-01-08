
# coding:utf-8

import socket
import sys

MSGLEN = 1024


def recvail(sock, length):
    data = b''
    while len(data)<length:
        try:
            more = sock.recv(length-len(data))
            if not more:
                raise EOFError(
                    'was expecting %d bytes but only receieved %d bytes before the socket closed' % (length, len(data)))
        except socket.error, msg:
            sock.close()
            raise EOFError("Connecting Failure. Error Code : ", msg)

        data = data + more
    return data


def server(host, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 生成一个新的socket对象
    except socket.error, msg:
        print "Creating Socket Failure. Error Code : ", msg
        sys.exit()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 设置地址复用
    try:
        sock.bind((host, port))  # 绑定地址
    except socket.error, msg:
        print "Binding Failure. Error Code : ", msg
        sys.exit()

    sock.listen(1)
    print('listen.....')
    while 1:
        sc, sockname = sock.accept()
        print("we have accepted a connection from", sockname)
        while 1:
            try:
                message = sc.recv(512)
                print('info..', message)
                if not message:
                    sc.close()
                    break
                message_lines = message.split('\n')
                for mess in message_lines:
                    print "mess", mess

            except socket.error, e:
                sc.close()
            # sc.sendall(b'farewell,client')


if __name__ == "__main__":
    server('127.0.0.1', 2000)
