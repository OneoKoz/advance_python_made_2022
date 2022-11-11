import os
import queue
import socket
import sys
import threading

from conf import config as cc

conf = cc.get_data()
que_req = queue.Queue()
COUNT_THREADS = 18
PATH2URLS = './conf/urls.txt'


def send_request(que: queue.Queue):
    while not que.empty():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.connect((conf.host, conf.port))
            except ConnectionRefusedError:
                print('problem with server')
                break

            try:
                url = que.get()
            except queue.Empty as err:
                print(err)

            if url is None:
                que.put(url)
                print('END CLIENT THREAD')
                break

            sock.sendall(str.encode(url))
            data = sock.recv(1024).decode(conf.encoding)
            print(f'{url=} {data=}')


def start_client():
    all_threads = [
        threading.Thread(
            target=send_request,
            args=(que_req,),
        ) for _ in range(COUNT_THREADS)]

    with open(PATH2URLS, 'r', encoding=conf.encoding) as file:
        all_urls = file.readlines()

    for url in all_urls:
        que_req.put(url.strip())
    que_req.put(None)

    for thread in all_threads:
        thread.start()


if __name__ == "__main__":

    if len(sys.argv) > 2:
        try:
            COUNT_THREADS = int(sys.argv[1])
        except ValueError:
            print('count must be int')

        if not os.path.exists(sys.argv[2]):
            print('file is not exists')
        else:
            PATH2URLS = sys.argv[2]

        start_client()
    else:
        print('not enough argument')
