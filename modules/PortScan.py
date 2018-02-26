# coding=utf-8
from queue import Queue
from threading import Thread
from telnetlib import Telnet

portlist = [21, 22, 23, 53, 80, 111, 139, 161, 389, 443, 445, 512, 513, 514,
            873, 1025, 1433, 1521, 3128, 3306, 3311, 3312, 3389, 5432, 5900,
            5984, 6082, 6379, 7001, 7002, 8000, 8080, 8081, 8090, 9000, 9090,
            8888, 9200, 9300, 10000, 11211, 27017, 27018, 50000, 50030, 50070]


class PortScan(Thread):
    TIMEOUT = 5

    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def auth(self, url):
        host = url.split(':')[0]
        port = url.split(':')[-1]

        try:
            tn = Telnet(host=host, port=port, timeout=self.TIMEOUT)
            # 越高,得到的调试输出就越多(sys.stdout)。
            tn.set_debuglevel(3)
            print('[*] ' + url + ' -- ok')

            with open('ok.txt', 'a') as f:
                try:
                    f.write(str(url) + '\n')
                except:
                    pass
        except Exception as e:
            # print('[ ] ' + url + ' -- ' + str(e))
            pass
        finally:
            tn.close()

    def run(self):  # 非空
        while not self.queue.empty():
            url = self.queue.get()
            try:
                self.auth(url)
            except:
                continue


def dispatcher(url_file=None, ip=None, max_thread=100):
    iplist = []  # ['207.148.23.27', '47.95.232.119']
    if url_file is not None and ip is None:
        with open(str(url_file)) as f:
            while True:
                line = str(f.readline()).strip()
                if line:
                    iplist.append(line)
                else:
                    break
    elif ip is not None and url_file is None:
        iplist.append(ip)
    else:
        pass

    with open('ok.txt', 'w'):
        pass

    q = Queue()  # 队列大小92，每一个PortScan实例取走一个
    for ip in iplist:
        for port in portlist:
            url = str(ip) + ':' + str(port)
            q.put(url)

    print(q.__dict__['queue'])
    print('-' * 64)
    print(u'队列大小：' + str(q.qsize()))

    threadl = [PortScan(q) for _ in range(max_thread)]
    for t in threadl:
        t.start()

    for t in threadl:
        t.join()

# if __name__ == '__main__':
#     dispatcher('ip.txt')
