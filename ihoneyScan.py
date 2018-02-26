from modules.verify import Src
from argparse import ArgumentParser

if __name__ == '__main__':
    parser = ArgumentParser(add_help=True, description='Batch of subdomain validation tool.  --20180225')
    parser.add_argument('-f', dest="url_file", help="Set subdomain file")
    parser.add_argument('-t', dest="max_threads", nargs='?', type=int, default=50, help="Set max threads")
    parser.add_argument('-m', dest="module", nargs='?', help="Set scanning module, Choice: [verify, SingleThreadPortScan, MultiThreadPortScan,]")
    # parser.add_argument('-u', dest='url', help="Set url, example: http://localhost")
    args = parser.parse_args()
    parser.print_usage()
    print(args)

    src58 = Src(max_threads=args.max_threads, url_file=args.url_file)
    src58.dispatcher()
