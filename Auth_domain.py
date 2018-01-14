import requests
import logging
import threading
from concurrent import futures
import datetime

max_threads = 50  # 最大并发线程数
logging.basicConfig(level=logging.INFO, format="%(message)s")
executor = futures.ThreadPoolExecutor(max_workers=max_threads)
threadpool_container = []  # 线程池容器

headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
    'Referer': 'http://www.58.com/',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    # 'Cookie': '这里写你的Cookie',
    'Connection': 'close'
}


def handler(url):
    try:
        max_timeout = 5  # 最大请求超时时间
        r = requests.get(url=url, headers=headers, timeout=max_timeout)
        content = r.content
        if content:
            if not r.history:
                logging.info(
                    "[ ] {} -> {} -> {}".format(url, r.status_code,
                                                r.headers['Server']))
            else:
                lst = []
                for code in r.history:
                    lst.append(code.status_code)
                lst.append(r.status_code)
                logging.info(
                    "[+] {} -> {} -> {}".format(url, lst,
                                                r.headers['Server']))
    except:
        pass
    finally:
        pass


def shutdown():
    try:
        while True:
            flag = True

            for t in threadpool_container:
                flag = flag and t.done()  # 调用是否成功取消或运行完成

            if flag:
                executor.shutdown()  # 清理池

                break
    except:
        pass


def run():
    try:
        with open('url.txt') as f:
            while True:
                line = f.readline()
                if line:
                    url = "http://" + line.strip()
                    t = executor.submit(handler, url)
                    threadpool_container.append(t)
                    # threading.Thread(target=handler, args=(url,)).start()
                else:
                    break
    except Exception as e:
        print(e)
        pass
    finally:
        logging.info('[+] 所有线程已启动，请等待域名验证完成!')
        shutdown()


if __name__ == '__main__':
    start = datetime.datetime.now()
    run()
    end = datetime.datetime.now()
    delta = (end - start).total_seconds()
    logging.info("[*] 所有线程已结束！总耗时{}秒".format(delta))
