import asyncio
import os
import sys

import aiohttp


async def fetch_url(url, session):
    async with session.get(url) as resp:
        data = await resp.read()
        return len(data)


async def read_file_urls(path: str):
    que = asyncio.Queue()
    with open(path, 'r', encoding='utf-8') as file:
        line = file.readline()
        while line:
            await que.put(line.strip())
            line = file.readline()
    return que


async def worker(queue, session, num):
    while True:
        url = await queue.get()
        try:
            res = await fetch_url(url, session)
            print(f"worker_{num}", res)
        finally:
            queue.task_done()


async def fetch_batch_urls(queue: asyncio.Queue, num_worker: int):
    async with aiohttp.ClientSession() as session:
        tasks = [
            asyncio.create_task(worker(queue, session, i))
            for i in range(num_worker)
        ]
        await queue.join()
        for task in tasks:
            task.cancel()


async def start_client(num_workers: int, path2url: str):
    if any(check_data(num_workers, path2url)) is None:
        return

    urls_queue = await read_file_urls(path2url)
    await fetch_batch_urls(urls_queue, num_workers)


def check_data(workers, path):
    try:
        workers = int(workers)
        if workers < 1:
            print('workers must be positive int')
            workers = 1
    except ValueError:
        workers = None
        print('count must be int')

    if not os.path.exists(path):
        path = None
        print('file is not exists')

    return workers, path


def get_args():
    if len(sys.argv) < 3:
        print('not enough argument')
        return None, None

    return check_data(*sys.argv[1:3])


if __name__ == "__main__":
    count_workers, path2urls = get_args()
    if count_workers is not None and path2urls is not None:
        asyncio.run(start_client(num_workers=count_workers, path2url=path2urls))
