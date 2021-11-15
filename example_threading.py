from time import sleep, time
from threading import Thread, current_thread


# def foo():
#     sleep(2)
# start = time()
# foo()
# print(f'step1: {time() - start}')
# foo()
# print(f'step2: {time() - start}')
# foo()
# print(f'step3: {time() - start}')
# print(f'{time() - start}')


########################################
# thread の基本的な使い方。
# def foo():
#     sleep(2)
# start = time()
# th1 = Thread(target=foo)
# th2 = Thread(target=foo)
# th1.start()  # thread をスタートさせる
# th2.start()
# th1.join()  # thread をメインに結合させる。全てのthread処理が終わってからmain処理を完了させるため。
# th2.join()
# print(f'{time() - start}')


########################################
# threadをたくさん作るとき。例：forを使って同じものを10個。
# def foo():
#     sleep(2)
# start = time()
# thread = []
# for _ in range(10):
#     th = Thread(target=foo)
#     th.start()
#     thread.append(th)
#
# for thread_ in thread:
#     thread_.join()
#
# print(f'{time() - start}')


########################################
# threadの実際の使い方
# import requests
# from concurrent.futures import ThreadPoolExecutor
#
# def print_content_length(url):
#     print(
#         len(requests.get(url).content)
#     )
#
# urls = [
#     'https://google.com/',
#     'https://lms.ithillel.ua',
#     'https://ja.wikipedia.org/wiki/%E3%82%A6%E3%82%A3%E3%82%AD',
#     'https://habr.com/ru/all/',
# ] * 10
#
# start = time()
# # for url in urls:
# #     print_content_length(url)
#
# # thread = []
# # for url in urls:
# #     th = Thread(target=print_content_length, args=[url])  # argsの他にkwargsを使ってもいい。
# #     th.start()
# #     thread.append(th)
# #
# # for thread_ in thread:
# #     thread_.join()
#
# with ThreadPoolExecutor(max_workers=10) as executor:  # workerの数を調整。最低の数で最高のパフォーマンスを出せるように。
#     for url in urls:
#         future = executor.submit(print_content_length, url)
#
# print(f'{time() - start}')


########################################
# # from threading import Thread
# from multiprocessing import Process
#
# the_num = 100_000_000
#
# start = time()
#
# def countdown(num):
#     while num:
#         num -= 1
#
# th1 = Process(target=countdown, args=[the_num / 2])
# th2 = Process(target=countdown, args=[the_num / 2])
# th1.start()
# th2.start()
# th1.join()
# th2.join()
#
# print(f'{time() - start}')

'''
GIL - Global Interpreter Lock
タスクが一つのときはスレッドは一つだけ。二つの時は二つ。

CPU bound - Process 新たなカーネルを作り処理。重い計算をさせるような処理。より多くのリソースと時間を要する。
I/O bound - Thread 一つのカーネル内に複数のスレッドを作り処理。何かしらの処理を待っているようなタスク。より軽い処理。

例：
write/read Database ->> I/O bound, Threadオペレーション。計算する必要がないから。リクエストし処理を待つだけだから。
write to file ->> I/O bound, Threadオペレーション。計算する必要がないから。
prime number ->> CPU bound, 
parse wiki - Thread
'''

########################################
# print(current_thread())
# def foo():
#     print(current_thread())
#     sleep(5)
#
# start = time()
# thread = []
# for _ in range(10):
#     th = Thread(target=foo)
#     th.start()
#     thread.append(th)
#
# for thread_ in thread:
#     thread_.join()
#
# print(f'{time() - start}')


########################################
from multiprocessing import Process, current_process

the_num = 100_000_000

start = time()

print(current_process())
def countdown(num):
    print(current_process())
    while num:
        num -= 1

th1 = Process(target=countdown, args=[the_num / 2])
th2 = Process(target=countdown, args=[the_num / 2])
th1.start()
th2.start()
th1.join()
th2.join()

print(f'{time() - start}')
