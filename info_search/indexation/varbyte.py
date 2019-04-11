#!/usr/bin/env python
from struct import pack, unpack

def encode_num(num):
    bytestream = []
    while True:
        bytestream.insert(0, num % 128)
        if num < 128:
            break
        num /= 128
    bytestream[-1] += 128
    return pack('%dB' % len(bytestream), *bytestream)

def encode(doc_ids):
    encoded_str = ''
    for doc_id in doc_ids:
        encoded_str += encode_num(doc_id)
    return encoded_str

def decode(bytestream):
    n = 0
    nums = []
    bytestream = unpack('%dB' % len(bytestream), bytestream)
    for byte in bytestream:
        if byte < 128:
            n = 128 * n + byte
        else:
            n = 128 * n + (byte - 128)
            nums.append(n)
            n = 0
    return nums

def compress(index_dict):
    compressed_dict = {}
    for word, doc_ids in index_dict.items():
        compressed_dict[word] = encode(doc_ids)
    return compressed_dict

def decompress(compressed_dict):
    index_dict = {}
    for word, bytestream in compressed_dict.items():
        index_dict[word] = decode(bytestream)
    return index_dict