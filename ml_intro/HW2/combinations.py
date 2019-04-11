import math
import random
import string

def C(n, k):
  return math.factorial(n)// (math.factorial(k) * math.factorial(n-k))

n = 6
k = 4

a = []

for i in range(1, k + 1):
    a.append(i)

p = k - 1
while p >= 0:
    print("p:", p)
    print(a)
    if a[k - 1] == n:
        p = p - 1
    else:
        p = k - 1
    print("new p:", p)
    if p >= 0:
        for i in reversed(range(p, k)):
            a[i] = a[p] + i - p + 1

#subsequences = {}
#sequence = ''.join(random.choices(string.ascii_lowercase, k=n))
#print(sequence)

# for I in range(1, C(n, k) + 1):
#   b = [0]
#   s = 0
#   t = 1
#   while t <= k:
#     j = b[t-1] + 1
#     while j < n - k + t and s + C(n - j, k - t) < I:
#       s = s + C(n - j, k - t)
#       j += 1
#     b.append(j)
#     t += 1
#   print(I, b[1:])
#   subsequence = ''
#   for i in b[1:]:
#     subsequence += sequence[i - 1]
#   if subsequence in subsequences:
#     subsequences[subsequence] += 1
#   else:
#     subsequences[subsequence] = 0

# print(sequence)
# for subsequence, meet_count in subsequences.items():
#   print(subsequence, meet_count)

