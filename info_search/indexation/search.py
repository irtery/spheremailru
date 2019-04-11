#!/usr/bin/env python
# -*- coding: utf-8 -*-

import varbyte
import simple9
import mmh3
import pickle
import sys
import codecs
from query2tokens import extract_tokens

class Tree:
    def __init__(self):
        self.left = None
        self.right = None
        self.data = None

        self.current_doc_id = -1
        self.last_doc_id = -1

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

    def evaluate(self):
        # print self.data
        if self.right:
            self.right.last_doc_id = self.last_doc_id
        if self.left:
            self.left.last_doc_id = self.last_doc_id

        if self.data == '&':
            self.evaluate_and()
        elif self.data == '|':
            self.evaluate_or()
        elif self.data == '!':
            self.evaluate_not()
        else:
            self.evaluate_term()

        if self.right:
            self.right.current_doc_id = self.current_doc_id
        if self.left:
            self.left.current_doc_id = self.current_doc_id

        return self.current_doc_id

    def evaluate_term(self):
        # print 'in evaluate_term'
        hterm = mmh3.hash(self.data.encode('utf-8'), signed=False)
        if hterm in index_dict.keys():
            compr_docids = index_dict[hterm]
            # print self.data, encode_method
            doc_ids = []
            if encode_method == 'varbyte':
                doc_ids = varbyte.decode(compr_docids)
            else:
                doc_ids = simple9.decode(compr_docids)
            # print 'cur_doc', self.current_doc_id
            self.get_next(doc_ids)
            # print 'cur_doc after get_next', self.current_doc_id
        else:
            print 'key not found'
            self.current_doc_id = omega_id
        # print 'next term doc_id', self.current_doc_id

    def get_next(self, doc_ids):
        orig_doc_ids = []
        orig_doc_id = -1
        for i, doc_id in enumerate(doc_ids):
            if i == 0:
                orig_doc_id = doc_id
                orig_doc_ids.append(doc_id)
            else:
                orig_doc_id = doc_id + orig_doc_ids[i-1]
                orig_doc_ids.append(orig_doc_id)
            if orig_doc_id > self.last_doc_id:
                # print orig_doc_ids, len(orig_doc_ids)
                self.current_doc_id = orig_doc_id
                return
        self.current_doc_id = omega_id

    def evaluate_and(self):
        # print self.data
        left_doc_id = self.left.evaluate()
        right_doc_id = self.right.evaluate()

        while left_doc_id != right_doc_id:
            while left_doc_id > right_doc_id:
                self.right.last_doc_id = right_doc_id
                right_doc_id = self.right.evaluate()
                if right_doc_id == omega_id:
                    break
            while right_doc_id > left_doc_id:
                self.left.last_doc_id = left_doc_id
                left_doc_id = self.left.evaluate()
                if left_doc_id == omega_id:
                    break
            if left_doc_id == omega_id or right_doc_id == omega_id:
                break

        if left_doc_id == right_doc_id:
            self.current_doc_id = left_doc_id
        else:
            self.current_doc_id = omega_id

        # print 'next and doc_id', self.current_doc_id

        self.right.last_doc_id = self.last_doc_id
        self.left.last_doc_id = self.last_doc_id

    def evaluate_or(self):
        left_doc_id = self.left.evaluate()
        right_doc_id = self.right.evaluate()

        # print 'left:', left_doc_id, 'right:', right_doc_id
        if left_doc_id < right_doc_id:
            self.current_doc_id = left_doc_id
        else:
            self.current_doc_id = right_doc_id
        # print 'next or doc_id:', self.current_doc_id

    def evaluate_not(self):
        # print 'in evaluate_not'
        doc_id = self.right.evaluate()
        # print 'border', doc_id
        if self.current_doc_id == omega_id:
            return

        if self.current_doc_id < doc_id - 1:
            # print 'norm', self.current_doc_id
            self.current_doc_id = self.current_doc_id + 1
            # print 'next not term doc id', self.current_doc_id
            return
        else:
            # print 'ne norm', self.current_doc_id
            self.right.last_doc_id = doc_id
            tmp = self.current_doc_id
            self.current_doc_id = doc_id
            # print 'incr right border', self.right.last_doc_id
            self.evaluate_not()
            self.right.last_doc_id = self.last_doc_id


if __name__ == '__main__':
    sys.stdin = codecs.getreader('utf-8')(sys.stdin)

    with open('index', 'rb') as f:
        index = pickle.load(f)

    with open('urls', 'rb') as f:
        urls = pickle.load(f)

    global index_dict
    global encode_method

    encode_method = index['method']
    index_dict = index['data']

    for query in sys.stdin:
        # print
        # print '%'*20
        query = query.strip()
        query_tree = Tree()
        query_tree.build(query)
        # query_tree.print_tree()

        last_doc_id = -1

        global omega_id
        omega_id = len(urls)
        # print 'omega', omega_id
        found_doc_ids = {}

        while last_doc_id < omega_id - 1:
            # print '#'*20
            query_tree.last_doc_id = last_doc_id
            # print 'last checked doc_id:', last_doc_id
            new_doc_id = query_tree.evaluate()
            if new_doc_id == omega_id:
                break
                
            found_doc_ids.setdefault(new_doc_id, 0)
            # print new_doc_id, urls[new_doc_id]
            last_doc_id = new_doc_id
        # print
        # print 'total', omega_id
        # print 'found to query', len(found_doc_ids.keys())
        doc_ids = sorted(found_doc_ids.keys())

        print query
        print len(doc_ids)
        for doc_id in doc_ids:
            print urls[doc_id]
