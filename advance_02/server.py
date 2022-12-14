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

from advance_02.conf import config as con


def calc_word(url: str, num_word: int, config: con):
    count_dict = defaultdict(int)
    try:
        resp = urlopen(url)
    except urllib.error.HTTPError as err:
        print(err)
        return b'{}'
    with resp:
        line = resp.readline()
        while line:
            line = line.decode(config.encoding)
            line = re.sub(r'\W+', ' ', line)
            for word in line.split(' '):
                if word:
                    count_dict[word] += 1
            line = resp.readline()

    count_dict = dict(sorted(count_dict.items(), key=lambda item: item[1], reverse=True)[:num_word])
    count_dict_encode = json.dumps(count_dict).encode(config.encoding)
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


def get_url_info(que: queue.Queue, num_word: int, config: con):
    while True:
        if not que.empty():
            cur_conn = que.get()

            if cur_conn is None:
                que.put(None)
                print('END')
                break

            with cur_conn:
                while not is_socket_closed(cur_conn):
                    url = cur_conn.recv(1024).decode(config.encoding)
                    if not url:
                        cur_conn.sendall(b'{}')
                        break
                    ans = calc_word(url, num_word, config)
                    cur_conn.sendall(ans)


def start_server(num_threads: int, num_word: int):
    que = queue.Queue()
    config = con.get_data()
    all_threads = [
        threading.Thread(
            target=get_url_info,
            args=(que, num_word, config),
        ) for _ in range(num_threads)]

    for thread in all_threads:
        thread.start()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind((config.host, config.port))
        sock.listen()
        sock.settimeout(config.timeout)
        while True:
            try:
                conn, addr = sock.accept()
                print(f'{addr=}')
                que.put(conn)
            except socket.timeout:
                que.put(None)
                break
            except KeyboardInterrupt:
                que.put(None)
                break
            except Exception as err:
                print(err)


def get_args():
    num_threads = None
    num_word = None
    for k, v in getopt.getopt(sys.argv[1:], 'w:k:')[0]:
        if k == '-w':
            try:
                num_threads = int(v)
            except ValueError:
                print('count must be number')

        if k == '-k':
            try:
                num_word = int(v)
            except ValueError:
                print('count must be number')

    return num_threads, num_word


if __name__ == "__main__":
    conf = con.get_data()
    que_conn = queue.Queue()

    count_threads, count_word = get_args()
    if count_word is not None and count_threads is not None:
        start_server(count_threads, count_word)
