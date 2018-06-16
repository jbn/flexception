from flexceptions.tryable import Tryable


def f(x, gamma=-0.5):
    return x**gamma


def test_success():
    res = Tryable.apply(f, 4)

    assert res.is_success
    assert res.value == 0.5
    assert repr(res) == "Success(0.5)"
    assert Tryable.succeeded(res)
    assert not Tryable.failed(res)


def test_failure():
    res = Tryable.apply(f, 0)

    assert not res.is_success
    assert not hasattr(res, 'value')
    assert repr(res) == "Failure(f, ...)"
    assert not Tryable.succeeded(res)
    assert Tryable.failed(res)

    def g(x):
        return x + 1

    assert res.retry(lambda x: x + 1).value == 1
