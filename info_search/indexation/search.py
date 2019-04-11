#!/usr/bin/env python
# -*- coding: utf-8 -*-

import varbyte
import simple9
import mmh3
import pickle
import sys
import codecs
from query2tokens import extract_tokens

OPERATORS = ['&', '|', '!', ')', '(']

class Tree:
    def __init__(self):
        self.left = None
        self.right = None
        self.data = None

    def print_tree(self):
        print self.data
        if self.left:
            print 'left from', self.data
            self.left.print_tree()
        else:
            print self.data, 'no left'
        if self.right:
            print 'right from', self.data
            self.right.print_tree()
        else:
            print self.data, 'no right'

    def build(self, query):
        tokens = extract_tokens(query)
        self.build_from_tokens(tokens)

    def build_from_tokens(self, tokens):
        ind = self.find_least_priority_operator(tokens)
        self.data = tokens[ind]

        left_tokens = tokens[:ind]
        if left_tokens:
            self.left = Tree()
            if left_tokens[0] == '(':
                left_tokens = left_tokens[1:-1]
            if len(left_tokens) == 1:
                self.left.data = left_tokens[0]
            else:
                self.left.build_from_tokens(left_tokens)

        right_tokens = tokens[ind+1:]
        if right_tokens:
            self.right = Tree()
            if right_tokens[0] == '(':
                right_tokens = right_tokens[1:-1]
            if len(right_tokens) == 1:
                self.right.data = right_tokens[0]
            else:
                self.right.build_from_tokens(right_tokens)

    def find_least_priority_operator(self, tokens):
        priority = {}
        cur_prior = 0
        for i, token in enumerate(reversed(tokens)):
            rev_i = len(tokens) - i - 1
            if token == ')':
                cur_prior += 3
            elif token == '(':
                cur_prior -= 3
            elif token == '!':
                priority[rev_i] = cur_prior + 3
            elif token == '&':
                priority[rev_i] = cur_prior + 2
            elif token == '|':
                priority[rev_i] = cur_prior + 1
            else:
                continue
        min_prior = 10000
        min_ind = -1
        for ind, pr in sorted(priority.items(), key=lambda x: x[0], reverse=True):
            if pr < min_prior:
                min_prior = pr
                min_ind = ind
        return min_ind

if __name__ == '__main__':
    sys.stdin = codecs.getreader('utf-8')(sys.stdin)

    for query in sys.stdin:
        print
        print query
        query_tree = Tree()
        query_tree.build(query)
        query_tree.print_tree()