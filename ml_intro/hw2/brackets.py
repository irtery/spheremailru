import sys

def brackets(n):
  yield from gen_next_sequence(n)

def gen_next_sequence(n, open_count=0, close_count=0, result_str=""):
    if open_count + close_count == 2 * n:
      yield result_str
    if open_count < n:
      yield from gen_next_sequence(n, open_count + 1, close_count, result_str + '(')
    if open_count > close_count:
      yield from gen_next_sequence(n, open_count, close_count + 1, result_str + ')')

if __name__ == '__main__':
  n = int(input())
  for i in brackets(n):
    print(i)