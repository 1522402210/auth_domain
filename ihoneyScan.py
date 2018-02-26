from modules import subdomain
from modules import PortScan
import ipaddress
from argparse import ArgumentParser
from base64 import b64decode

if __name__ == '__main__':
    logo_code = 'IF8gICBfICAgICAgICAgICAgICAgICAgICAgICAgICAgIF9fX18gICAgICAgICAgICAgICAgICAKKF8pIHwgfF9fICAgX19fICBfIF9fICAgX19fIF8gICBfLyBfX198ICBfX18gX18gXyBfIF9fICAKfCB8IHwgJ18gXCAvIF8gXHwgJ18gXCAvIF8gXCB8IHwgXF9fXyBcIC8gX18vIF9gIHwgJ18gXCAKfCB8IHwgfCB8IHwgKF8pIHwgfCB8IHwgIF9fLyB8X3wgfF9fXykgfCAoX3wgKF98IHwgfCB8IHwKfF98IHxffCB8X3xcX19fL3xffCB8X3xcX19ffFxfXywgfF9fX18vIFxfX19cX18sX3xffCB8X3wKICAgICAgICAgICAgICAgICAgICAgICAgICAgIHxfX18vICAgICAgICAgICAgICAgICAgICAgICAK'

    example = '''
        $ python3.5 ihoneyScan.py -m verify -f url.txt
        $ python3.5 ihoneyScan.py -m verify -t 100 -f url.txt
        $ python3.5 ihoneyScan.py -m portscan -f ip.txt -t 100
        $ python3.5 ihoneyScan.py -m portscan --ip 207.148.23.27
    '''

    print(b64decode(logo_code).decode())
    print('-' * 64)
    parser = ArgumentParser(add_help=True, description='Batch of subdomain validation tool.')
    parser.add_argument('-f', dest="url_file", help="Set subdomain file")
    parser.add_argument('-t', dest="max_threads", nargs='?', type=int, default=1, help="Set max threads")
    parser.add_argument('-m', dest="module", nargs='?', help="Set module, Choice: [subdomain, portscan]")
    parser.add_argument('--ip', dest='ip', nargs='?', type=str, help="Example: 207.148.23.27")
    parser.add_argument('-d', dest='domain', nargs='?', type=str, help="Example: www.ihoneysec.top", default=None)

    args = parser.parse_args()

    if args.module == 'subdomain':
        print('[+] Subdomain module start ')
        subdomain.dispatcher(max_threads=args.max_threads, url_file=args.url_file, domain=args.domain)
    elif args.module == 'portscan':
        print('[+] portscan module start ')
        if args.ip is not None and args.url_file is None:
            try:
                ipaddress.ip_address(args.ip)
            except Exception as e:
                print(e)
            scan = PortScan.dispatcher(ip=args.ip, max_thread=args.max_threads)
        elif args.url_file is not None and args.ip is None:
            PortScan.dispatcher(url_file=args.url_file, max_thread=args.max_threads)
    else:
        print('模块不支持，请反馈给作者')
