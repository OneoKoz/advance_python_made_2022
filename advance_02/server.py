import getopt
import json
import queue
import re
import socket
import sys
import threading
import urllib
from collections import defaultdict
from urllib.request import urlopen

from conf import config as con

conf = con.get_data()
que_conn = queue.Queue()
COUNT_WORD = 7
COUNT_THREADS = 7


def calc_word(url: str):
    count_dict = defaultdict(int)
    try:
        resp = urlopen(url)
    except urllib.error.HTTPError as err:
        print(err)
        return b''
    with resp:
        for line in resp.readlines():
            line = line.decode(conf.encoding)
            line = re.sub(r'\W+', ' ', line)
            for word in line.split(' '):
                if word:
                    count_dict[word] += 1

    count_dict = dict(sorted(count_dict.items(), key=lambda item: item[1], reverse=True)[:COUNT_WORD])
    count_dict_encode = json.dumps(count_dict).encode(conf.encoding)
    return count_dict_encode


def is_socket_closed(sock: socket.socket) -> bool:
    try:
        data = sock.recv(16, socket.MSG_DONTWAIT | socket.MSG_PEEK)
        if len(data) == 0:
            return True
    except BlockingIOError:
        return False
    except ConnectionResetError:
        return True
    except Exception as err:
        print(err)
        return False
    return False


def get_url_info(que: queue.Queue):
    while True:
        if not que.empty():
            cur_conn = que.get()

            if cur_conn is None:
                que.put(None)
                print('END')
                break

            with cur_conn:
                while not is_socket_closed(cur_conn):
                    url = cur_conn.recv(1024).decode(conf.encoding)
                    if not url:
                        break
                    ans = calc_word(url)
                    cur_conn.sendall(ans)


def start_server():
    all_threads = [
        threading.Thread(
            target=get_url_info,
            args=(que_conn,),
        ) for _ in range(COUNT_THREADS)]

    for thread in all_threads:
        thread.start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((conf.host, conf.port))
        sock.listen(10)
        sock.settimeout(conf.timeout)
        while True:
            try:
                conn, addr = sock.accept()
                print(f'{addr=}')
                que_conn.put(conn)
            except socket.timeout:
                que_conn.put(None)
                break
            except KeyboardInterrupt:
                que_conn.put(None)
                break


if __name__ == "__main__":
    for k, v in getopt.getopt(sys.argv[1:], 'w:k:')[0]:
        if k == '-w':
            try:
                COUNT_THREADS = int(v)
            except ValueError:
                print('count must be number')

        if k == '-k':
            try:
                COUNT_WORD = int(v)
            except ValueError:
                print('count must be number')
    start_server()
