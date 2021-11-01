# import time
#
# CACHE = None
#
# def slow_func():
#     global CACHE
#
#     if CACHE is None:  # 初めてのコール。キャッシュは空っぽ。
#         print('CACHE DOES NOT EXISTS.')
#         result = "y"
#         time.sleep(3)
#         CACHE = result  # キャッシュに結果"y"を書き込む！
#         return result
#     else:  # 既にcacheが存在する場合は
#         print('CACHE EXISTS.')
#         return CACHE
#
# start = time.time()
# print(slow_func())  # 機能自体をプリントにかける
# print(slow_func())
# print(slow_func())
# end = time.time()
# print(f'took time: {end - start}')
########################################


# import time
#
# CACHE = {}
#
# def slow_func(sleep_time: int):  # イントを書かなくても結果は同じだった。
#     print(CACHE)
#
#     if sleep_time in CACHE:
#         return CACHE[sleep_time]
#     else:
#         time.sleep(sleep_time)  # 最初2秒まつ。次は3秒まつ。
#         result = sleep_time ** 2
#         CACHE[sleep_time] = result  # キャッシュに結果を書き込む
#         print(CACHE)
#         return result
#
# start = time.time()
# print(slow_func(2))  # 「4」を2秒で
# print(slow_func(3))  # 「9」を3秒で
# print(slow_func(2))  # 「4」を0秒で
# end = time.time()
# print(f'took time: {end - start}')
########################################


# import time
#
# CACHE = {}
#
# def factorial(n):
#     global CACHE
#     print(CACHE)  # 最初は空っぽ。
#
#     if n in CACHE:  # 最初は空っぽだからスキップ。
#         return CACHE[n]
#     else:
#         result = 1
#         for num in range(n, 1, -1):
#             time.sleep(1)
#             result *= num
#
#         CACHE[n] = result
#         return result
#
# start = time.time()
# print(factorial(5))
# print(factorial(5))
# print(factorial(5))
# end = time.time()
# print(f'took time: {end - start}')
########################################


# import time
#
# CACHE = {}
#
# def add(x, y):
#     global CACHE
#     print(CACHE)
#
#     key = f'add::{x}::{y}'  # キャッシュのkeyはユニークなものを作ること。長くなってもいい。
#     print(CACHE)
#
#     if key in CACHE:  # 最初は空っぽだからスキップ。
#         return CACHE[key]
#     else:
#         result = x + y
#         CACHE[key] = result
#         return result
#
# def diff(x, y):
#     global CACHE
#     print(CACHE)
#
#     key = f'diff::{x}::{y}'  # キャッシュのkeyはユニークなものを作ること。長くなってもいい。
#     print(CACHE)
#
#     if key in CACHE:  # 最初は空っぽだからスキップ。
#         return CACHE[key]
#     else:
#         result = x - y
#         CACHE[key] = result
#         return result
#
#
# start = time.time()
# print('Add', add(22, 2))
# print('Diff', diff(22, 2))
# print(CACHE)
# # print(add(2, 4))
# end = time.time()
# print(f'took time: {end - start}')
########################################
import time


class User:
    def __init__(self, name):
        self.name = name
        self._slow_method_cache = None

    def slow_method(self):
        if self._slow_method_cache is not None:
            return self._slow_method_cache
        else:
            time.sleep(1)
            result = self.name
            self._slow_method_cache = result
            return result

human1 = User('Yoshio')
human1.slow_method()
human1.slow_method()
human1.slow_method()
human1.slow_method()
human1.slow_method()
human2 = User('Yoshiko')
human2.slow_method()
