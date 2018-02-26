import socket
import datetime
import threading
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")

# 多线程
threadlist = []
portlist = [21, 22, 23, 53, 80, 111, 139, 161, 389, 443, 445, 512, 513, 514,
            873, 1025, 1433, 1521, 3128, 3306, 3311, 3312, 3389, 5432, 5900,
            5984, 6082, 6379, 7001, 7002, 8000, 8080, 8081, 8090, 9000, 9090,
            8888, 9200, 9300, 10000, 11211, 27017, 27018, 50000, 50030, 50070]


def connScan(tgtip, port):
    start = datetime.datetime.now()
    # logging.info('[ ] Scanner Port {}'.format(port))
    try:
        sk = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sk.settimeout(10)
        sk.connect((tgtip, port))
        sk.send(u'helloPython\r\n'.encode())
        banner = sk.recv(1024)
        if banner:
            logging.info(
                '[+] {} Port {} Open, banner:{}'.format(tgtip, port, banner))
    except Exception as e:
        pass
        end = datetime.datetime.now()
        delta = (end - start).total_seconds()
        if delta >= 9:
            logging.info(
                "[+] {} Port {} request timeout, please check by hand".format(
                    tgtip, port))

        # logging.info('[-] Port {} Close, {}({})'.format(port, type(e).__name__, e))
    finally:
        sk.close()


def dispatcher(ip):
    for port in portlist:
        t = threading.Thread(target=connScan, args=(ip, port))
        threadlist.append(t)

    for thread in threadlist:
        thread.start()


if __name__ == '__main__':
    scanip = '207.148.23.27'
    dispatcher(scanip)
    # with open('url1.txt') as f:
    #     while True:
    #         scanip = f.readline()
    #         if scanip:
    #             dispatcher(scanip.strip())
    #             # print(scanip.strip())
    #         else:
    #             break
    # print(len(threadlist))
    # for thread in threadlist:
    #     thread.start()

# with open('url.txt') as f:
#     while True:
#         line = f.readline()
#         if line:
#             print(line.strip())
#         else:
#             break
