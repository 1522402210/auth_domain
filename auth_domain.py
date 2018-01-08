import requests
import threading
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")

headers = {
    'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36",
    'Referer': 'http://www.58.com/',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    # 'Cookie': '这里写你的Cookie',
    'Connection': 'close'
}


def handler(url):
    try:
        r = requests.get(url=url, headers=headers, timeout=5)
        content = r.content
        if content:
            logging.info(
                "{} => {} => {}".format(url, r.status_code,
                                        r.headers['Server']))
    except:
        # logging.info("{} - Connect Timeout！".format(url))
        pass
    finally:
        pass


if __name__ == '__main__':
    try:
        with open('url.txt') as f:
            while True:
                line = f.readline()
                if line:
                    url = "http://" + line.strip()
                    threading.Thread(target=handler, args=(url,)).start()
                else:
                    break
    except:
        pass
    finally:
        logging.info('所有线程已启动，请等待域名验证完成!')
