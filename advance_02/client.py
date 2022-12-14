import os
import queue
import socket
import sys
import threading

from advance_02.conf import config as cc


def read_file_urls(path: str, que: queue.Queue, config: cc):
    with open(path, 'r', encoding=config.encoding) as file:
        line = file.readline()
        while line:
            que.put(line.strip())
            line = file.readline()
    que.put(None)


def send_request(que: queue.Queue, config: cc):
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect((config.host, config.port))
            except ConnectionRefusedError:
                print('problem with server')
                break

            try:
                url = que.get()
            except queue.Empty as err:
                print(err)
                break

            if url is None:
                que.put(url)
                print('END CLIENT THREAD')
                break

            try:
                sock.sendall(str.encode(url))
                data = sock.recv(1024).decode(config.encoding)
                print(f'{url=} {data=}')
            except Exception as err:
                print(err)


def start_client(path2file: str, num_threads: int = 5):
    cur_que = queue.Queue()
    config = cc.get_data()

    if not os.path.exists(path2file):
        print('file not exist')
        return

    if num_threads < 1:
        print('num_thread must be positive int')

    all_threads = [
        threading.Thread(
            target=send_request,
            args=(cur_que, config),
        ) for _ in range(num_threads)]

    thread4read = threading.Thread(target=read_file_urls, args=(path2file, cur_que, config))
    thread4read.start()
    for thread in all_threads:
        thread.start()


def get_args():
    if len(sys.argv) < 3:
        print('not enough argument')
        return None, None

    try:
        num_thr = int(sys.argv[1])
    except ValueError:
        num_thr = None
        print('count must be int')

    if not os.path.exists(sys.argv[2]):
        path_2_urls = None
        print('file is not exists')
    else:
        path_2_urls = sys.argv[2]
    return num_thr, path_2_urls


if __name__ == "__main__":
    conf = cc.get_data()
    que_req = queue.Queue()

    count_threads, path2urls = get_args()
    if count_threads is not None and path2urls is not None:
        start_client(num_threads=count_threads, path2file=path2urls)
