#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import numpy as np

def levenshtein(a, b):
    """Return the Levenshtein edit distance between two strings *a* and *b*."""
    if a == b:
        return 0
    if len(a) < len(b):
        a, b = b, a
    if not a:
        return len(b)
    previous_row = range(len(b) + 1)
    for i, column1 in enumerate(a):
        current_row = [i + 1]
        for j, column2 in enumerate(b):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (column1 != column2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    return previous_row[-1] 

# def levenshtein(seq1, seq2):  
#     size_x = len(seq1) + 1
#     size_y = len(seq2) + 1
#     matrix = np.zeros ((size_x, size_y))
#     for x in xrange(size_x):
#         matrix [x, 0] = x
#     for y in xrange(size_y):
#         matrix [0, y] = y

#     for x in xrange(1, size_x):
#         for y in xrange(1, size_y):
#             if seq1[x-1] == seq2[y-1]:
#                 matrix [x,y] = min(
#                     matrix[x-1, y],
#                     matrix[x-1, y-1],
#                     matrix[x, y-1]
#                 )
#             else:
#                 matrix [x,y] = min(
#                     matrix[x-1,y] + 1,
#                     matrix[x-1,y-1] + 1,
#                     matrix[x,y-1] + 1
#                 )
#     # print (matrix)
#     return (matrix[size_x - 1, size_y - 1])

if __name__ == '__main__':
    filepath = 'lenta_words.txt'
    words_dict = {}
    with open(filepath) as fp:  
       content = fp.readlines()

    content = [x.strip() for x in content]
    for line in content:
        words_dict.setdefault(line, 0)
        words_dict[line] += 1
    words = words_dict.keys()
    print len(words)

    filein = 'in'

    with open(filein) as fp:  
       content = fp.readlines()

    check_words = ['пути', 'путин', 'роботу', 'работу', 'сирии', 'сирийца']
    for word in check_words:
        print word, words_dict[word]

    for typo_word in content:
        typo_word = typo_word.strip()
        min_dist = 1000
        cor_word = words[0]
        for word in words:
            # print word
            if abs(len(typo_word) - len(word)) > 3:
                continue
            dist = levenshtein(typo_word, word)
            if dist < min_dist:
                if words_dict[word] < 20:
                    continue
                print word, dist
                min_dist = dist
                cor_word = word
                continue
            if dist == min_dist:
                if words_dict[word] > words_dict[cor_word]:
                    print word, dist
                    min_dist = dist
                    cor_word = word
        print typo_word, '->', cor_word
        