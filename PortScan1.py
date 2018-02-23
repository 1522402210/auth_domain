import socket
import datetime

# 单线程
portlist = [21, 22, 23, 53, 80, 111, 139, 161, 389, 443, 445, 512, 513, 514,
            873,
            1025, 1433, 1521, 3128, 3306, 3311, 3312, 3389, 5432, 5900, 5984,
            6082, 6379, 7001, 7002, 8080, 8090, 9090, 8888, 9200, 9300, 10000,
            11211, 27017, 27018, 50000, 50030, 50070]


def connScan(tgtip, port):
    start = datetime.datetime.now()
    print('[ ] Scanner Port {}'.format(port))
    try:
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.settimeout(10)
        sk.connect((tgtip, port))
        sk.send(u'helloPython\r\n'.encode())
        banner = sk.recv(1024)
        if banner:
            print('[+] Port {} Open, banner:{}'.format(port, banner))
    except Exception as e:
        end = datetime.datetime.now()
        delta = (end - start).total_seconds()
        if delta >= 9:
            print("[+] Port {} request timeout, please check by hand".format(
                port))
        pass
        # print('[-] Port {} Close, {}({})'.format(port, type(e).__name__, e))
    finally:
        sk.close()


def portScan(ip):
    for port in portlist:
        connScan(ip, port)


if __name__ == '__main__':
    scanip = '207.148.23.27'
    portScan(scanip)
