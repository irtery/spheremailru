import numpy as np

def zeros_insert(k, n):
  k = np.array(k, dtype=float)
  i = 1
  while i < k.size:
    pos_arr = [i for j in range(n)]
    k = np.insert(k, pos_arr, np.zeros(n))
    i += n + 1
  return k