def foo(x, y):
    return x + y


##################

def test_foo1():
    assert foo(2, 4) == 6


def test_foo2():
    assert foo(2, 1) == 3
