#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import document_pb2
import struct
import gzip
import sys

import varbyte
import simple9
import mmh3
import cPickle
from doc2words import extract_words

# import cProfile


class DocumentStreamReader:
    def __init__(self, paths):
        self.paths = paths

    def open_single(self, path):
        return gzip.open(path, 'rb') if path.endswith('.gz') else open(path, 'rb')

    def __iter__(self):
        for path in self.paths:
            with self.open_single(path) as stream:
                while True:
                    sb = stream.read(4)
                    if sb == '':
                        break

                    size = struct.unpack('i', sb)[0]
                    msg = stream.read(size)
                    doc = document_pb2.document()
                    doc.ParseFromString(msg)
                    yield doc


def parse_command_line():
    parser = argparse.ArgumentParser(description='compressed documents reader')
    parser.add_argument('files', nargs='+', help='Input files (.gz or plain) to process')
    return parser.parse_args()

def precompress(index_dict):
    for word, doc_id_arr in index_dict.items():
        diff_arr = []
        for i, doc_id in enumerate(doc_id_arr):
            if i == 0:
                diff_arr.append(doc_id_arr[i])
            else:
                diff_arr.append(doc_id_arr[i] - doc_id_arr[i-1])
        index_dict[word] = diff_arr

def compress(method, index_dict):
    if method == 'varbyte':
        return varbyte.compress(index_dict)
    elif method == 'simple9':
        return simple9.compress(index_dict)
        # return cProfile.run('simple9.compress(index_dict)')
    else:
        print 'not supported yet'
        return index_dict


if __name__ == '__main__':
    index_dict = {}
    urls = []
    doc_id = 0

    encode_method = parse_command_line().files[0]
    reader = DocumentStreamReader(parse_command_line().files[1:])
    for doc in reader:
        doc_words = extract_words(doc.text)
        doc_unique_words = list(set(doc_words))
        for word in doc_unique_words:
            index_dict.setdefault(word, []).append(doc_id)
        doc_id += 1
        urls.append(doc.url)

    # for k,v in index_dict.items():
    #     if k == u'путин':
    #         print v

    precompress(index_dict)

    index = {}
    index['method'] = encode_method
    index['data'] = compress(encode_method, index_dict)

    with open('./index', 'wb') as f:
        cPickle.dump(index, f)

    with open('./urls', 'wb') as f:
        cPickle.dump(urls, f)