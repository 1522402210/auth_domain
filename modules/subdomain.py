# -*- coding: utf8 -*-
import requests
import logging
from re import search
from socket import gethostbyname
from concurrent import futures

logging.basicConfig(level=logging.WARNING, format="%(message)s")


class Src:
    def __init__(self, max_threads=1, max_timeout=5, url_file='url.txt'):
        self.max_threads = max_threads  # 最大线程数
        self.max_timeout = max_timeout  # 最大请求超时时间

        self.headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
            # 'Referer': 'http://www.58.com/',
            # 'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            # 'Cookie': '这里写你的Cookie',
            'Connection': 'close'
        }

    def auth(self, url):
        try:
            r = requests.get(url=url, headers=self.headers, timeout=self.max_timeout)
            content = r.content.decode()

            if 'http://' in url:
                url = url.split('http://')[1]
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
                    logging.warning("[   ] {}  {}   {}   {}   {}".format(ip_list, url, status_lst, header_list, title_list))
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

                    logging.warning("[***] {}  {}   {}   {}   {}".format(ip_list, url, status_lst, header_list, title_list))
        except:
            pass


def dispatcher(max_threads=None, url_file=None, domain=None):
    executor = futures.ThreadPoolExecutor(max_workers=max_threads)
    src58 = Src(max_threads=max_threads)

    if url_file is not None and domain is None:
        try:
            with open(url_file) as f:
                while True:
                    line = f.readline()
                    if line:
                        url = "http://" + str(line.strip())  # 去掉每行末尾的\r\n
                        executor.submit(src58.auth, url)
                    else:
                        break
        except Exception:
            pass
    elif domain is not None and url_file is None:
        url = "http://" + str(domain.strip())
        executor.submit(src58.auth, url)
