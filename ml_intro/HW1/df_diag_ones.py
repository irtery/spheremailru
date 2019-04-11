import pandas as pd
import numpy as np

def df_diag_ones(df):
  diag_id = range(df.shape[0])
  df.values[diag_id, diag_id] = 1
  df.values[diag_id, diag_id[::-1]] = 1
  return df

if __name__ == "__main__":
  df = [
    [16,  5, 23,  4, 20],
    [24,  8, 15, 24,  9],
    [15, 11,  9,  8,  7],
    [ 5, 17,  8, 13,  1],
    [12, 24,  7, 20, 13]
  ]
  df = pd.DataFrame(df)
  df = df_diag_ones(df)
  print(df.values)