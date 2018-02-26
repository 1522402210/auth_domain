# -*- coding: utf8 -*-
import requests
import logging
from re import search
from socket import gethostbyname
from concurrent import futures

logging.basicConfig(level=logging.INFO, format="%(message)s")


class Src:
    def __init__(self, max_threads=10, max_timeout=5, url_file='url.txt'):
        self.max_threads = max_threads  # 最大线程数
        self.max_timeout = max_timeout  # 最大请求超时时间
        self.url_file = url_file  # 同级目录下存放爆破出来的域名的文件名

        self.executor = futures.ThreadPoolExecutor(max_workers=max_threads)

        self.headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
            # 'Referer': 'http://www.58.com/',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            # 'Cookie': '这里写你的Cookie',
            'Connection': 'close'
        }

    def auth(self, url):
        try:
            r = requests.get(url=url, headers=self.headers, timeout=self.max_timeout)
            content = r.content.decode()

            ip_list = [gethostbyname(str(url.strip()))]

            if content:
                header_list = []  # ['nginx/1.10.3', 'PHP/5.6.20']

                header_server = r.headers.get('Server')
                header_XPoweredBy = r.headers.get('X-Powered-By')

                if header_XPoweredBy is not None: header_list.append(header_XPoweredBy)
                if header_server is not None: header_list.append(header_server)

                if not r.history:
                    status_lst = []
                    title_list = []

                    url_title = search(r'<title>(.*)</title>', content)

                    if url_title:
                        url_title = url_title.group(1).strip().strip('\r').strip('\n')[:30]
                        title_list.append(url_title)
                        status_lst.append(r.status_code)

                    # [   ] http://cs.crm.58.com   [200]   ['ASP.NET', 'Tengine']   ['58同城CRM微信客服系统']
                    logging.info("[   ] {}  {}   {}   {}   {}".format(ip_list, url, status_lst, header_list, title_list))
                else:
                    status_lst = []  # [301, 200, 302, 200]
                    title_list = []

                    url_title = ""
                    for code in r.history:
                        url_title = search(r'<title>(.*)</title>', content)
                        if url_title:
                            url_title = url_title.group(1).strip().strip('\r').strip('\n')[:30]

                        status_lst.append(code.status_code)
                    status_lst.append(r.status_code)
                    title_list.append(url_title)

                    logging.info("[***] {}  {}   {}   {}   {}".format(ip_list, url, status_lst, header_list, title_list))
        except:
            pass

    def dispatcher(self):
        try:
            with open(self.url_file) as f:
                while True:
                    line = f.readline()
                    if line:
                        url = "http://" + str(line.strip())  # 去掉每行末尾的\r\n
                        self.executor.submit(self.auth, url)
                    else:
                        break
        except Exception:
            pass

# def main():
#     parser = ArgumentParser(add_help=True, description='Batch of subdomain validation tool.  --20180225')
#     parser.add_argument('-f', dest="url_file", help="Set subdomain file")
#     parser.add_argument('-t', dest="max_threads", nargs='?', type=int, default=50, help="Set max threads")
#     parser.add_argument('-m', dest="max_timeout", nargs='?', type=int, default=3, help="Set max timeout")
#     parser.add_argument('-u', dest='url', help="Set url, example: http://localhost")
#     args = parser.parse_args()
#     parser.print_usage()
#     print(args)
#
#     src58 = Src(max_threads=args.max_threads, max_timeout=args.max_timeout, url_file=args.url_file)
#     src58.dispatcher()


# src58 = Src(max_threads=100, max_timeout=3, url_file='url.txt')
# src58.dispatcher()


# if __name__ == '__main__':
#     main()
