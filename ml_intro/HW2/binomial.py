import sys

def binomial(n):
    for k in range(n + 1):
        if k == 0 or k == n:
            c = 1
        else:
            c = c * (n - k +1) // k
        yield c

if __name__ == '__main__':
    array = map(int, input().strip().split(" "))
    for n in array:
        print(*binomial(n))