#!/usr/bin/env python
# -*- coding: utf-8 -*-

import varbyte
import simple9
import mmh3
import cPickle

if __name__ == '__main__':
    with open('index', 'rb') as f:
        index = cPickle.load(f)

    new_index_data = {}
    words_by_hash = {}

    for word, compressed_doc_ids in index['data'].items():
        key = mmh3.hash(word.encode('utf-8'))
        new_index_data[key] = compressed_doc_ids
        words_by_hash[key] = word

    index['data'] = new_index_data

    with open('./index', 'wb') as f:
        cPickle.dump(index, f)