import pandas as pd
import numpy as np

def peak_finder(s):
  result = np.array([], dtype=int)
  for i in range(1, s.size - 1):
    if (s[i] > s[i-1]) & (s[i] > s[i+1]):
      result = np.append(result, i)
  return result

if __name__ == "__main__":
  s = pd.Series([1, 5, 1, 1, 5, 1])
  r = peak_finder(s)
  print(r)