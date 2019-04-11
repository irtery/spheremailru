import time
import functools

def stopwatch(func):
    @functools.wraps(func)
    def wrapper(*args, **argv):
        print('`{}` started'.format(func.__name__))
        startTime = time.time()
        result = func(*args, **argv)
        finishTime = time.time()
        print('`{}` finished in {}s'.format(func.__name__, round(finishTime - startTime, 2)))
        return result
    return wrapper


@stopwatch
def func():
    time.sleep(1.25)
