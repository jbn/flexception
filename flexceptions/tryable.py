import sys
import inspect
from functools import partial


class Tryable:

    @classmethod
    def succeeded(cls, tryable):
        return tryable.is_success

    @classmethod
    def failed(cls, tryable):
        return not tryable.is_success

    @classmethod
    def apply(cls, f, *args, **kwargs):
        try:
            return Success(f(*args, **kwargs))
        except KeyboardInterrupt:
            raise
        except Exception:
            return Failure(f, args, kwargs, *sys.exc_info())

    @classmethod
    def fapply(cls, f):
        return partial(Tryable.apply, f)

    @property
    def is_success(self):
        return False


class Success(Tryable):

    def __init__(self, value):
        self.value = value

    def is_success(self):
        return True

    def __repr__(self):
        return "Success({})".format(self.value)


def invocation_to_str(f, args, kwargs):
    binding = inspect.signature(f).bind(*args, **kwargs)
    s = str(binding)
    arg_str = s[s.find("(") + 1:s.rfind(')')]

    return "{}({})".format(f.__name__, arg_str)


class Failure(Tryable):

    def __init__(self, f, args, kwargs, exc_type, exc_value, exc_tb):
        self.f = f
        self.args = args
        self.kwargs = kwargs
        self.exc_type = exc_type
        self.exc_value = exc_value
        # Tracebacks aren't serializable

    def __repr__(self):
        return "Failure({}, ...)".format(self.f.__name__)

    def retry(self, f=None):
        # Assert f is same sig?
        return Tryable.apply(f or self.f, *self.args, **self.kwargs)
