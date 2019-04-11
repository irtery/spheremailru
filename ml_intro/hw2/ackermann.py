def compute_ackermann(m, n):
  ackermann.counter += 1
  if m == 0:
    return n + 1
  if m > 0 and n == 0:
    return compute_ackermann(m - 1, 1)
  return compute_ackermann(m - 1,  compute_ackermann(m, n - 1))

def ackermann(m, n):
  ackermann.counter = 0
  return compute_ackermann(m, n)

if __name__ == '__main__':
  print(ackermann(2, 27), ackermann.counter)
  print(ackermann(4, 0), ackermann.counter)
  print(ackermann(3, 5), ackermann.counter)