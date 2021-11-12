def hello():
    return 'HELLO'

def world():
    return 'WORLD'

urlpatterns = {
    '/hello/': hello,  # 機能をオブジェクトとして呼び出すので機能の後に()は書かない
    '/world/': world,
}

def application(environ, start_response):
    path = environ['PATH_INFO']
    the_function = urlpatterns.get(path)
    if the_function:
        data = the_function()
    else:
        data = 'No path match'

    data = str(data).encode()

    start_response(f"200 OK", [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(data)))
    ])

    return iter([data])
