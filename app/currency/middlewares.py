import time

from currency.models import ResponseLog


class ResponseTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response  # 以上は初期設定なので基本的に編集しない。

    def __call__(self, request):
        start = time.time()  # views.py に行く前
        response = self.get_response(request)  # views.py の実行
        end = time.time()  # views.py を実行した後

        ResponseLog.objects.create(
            status_code=response.status_code,
            path=request.path,
            response_time=(end - start) * 1_000,
            request_method=request.method,
        )
        return response


# class GclidMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         if 'gclid' in request.GET:
#             print(f'Gclid in request params. Path: {request.path}')
#
#         return self.get_response(request)
