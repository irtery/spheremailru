import functools

def once(func):
    already_called = False
    result = False
    @functools.wraps(func)
    def wrapper(*args):
        nonlocal already_called
        nonlocal result
        if not already_called:
            result = func(*args)
            already_called = True
        return result
    return wrapper

@once
def bonjour():
    print("Bonjour le monde!")

if __name__ == "__main__":
    bonjour()
    bonjour()
    bonjour()