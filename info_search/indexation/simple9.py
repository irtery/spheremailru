#!/usr/bin/env python
from struct import pack, unpack
import sys
import varbyte

WORDS_IN_BLOCK = [28, 14, 7, 4, 2, 1]
PAYLOAD_MAX = 28

def try_to_fill(words_count, words):
    max_word_size = PAYLOAD_MAX / words_count
    for word in words:
        if word.bit_length() > max_word_size:
            return False
    return True

def max_words_in_block(words):
    for wib in WORDS_IN_BLOCK:
        if try_to_fill(wib, words[:wib]):
            return wib
    return 0

def fill_code(words_in_block):
    if words_in_block == PAYLOAD_MAX:
        return '1111' # to fill in 4 bits
    return bin(words_in_block)[2:].zfill(4)

def fill_payload(words_in_block, words):
    result = ''
    for word in words:
        result += bin(word)[2:].zfill(PAYLOAD_MAX / words_in_block)
    while len(result) < 28:
        result += '0'
    return result

def fill_block(words_in_block, words):
    block = ''
    block += fill_code(words_in_block)
    block += fill_payload(words_in_block, words)
    return int(block, 2)

def encode(doc_ids):
    packed = 0
    blocks = []
    while packed < len(doc_ids):
        words_in_block = max_words_in_block(doc_ids[packed:])
        block = fill_block(words_in_block, doc_ids[packed:(packed+words_in_block)])
        blocks.append(block)
        packed += words_in_block
    encoded_str = varbyte.encode(blocks)
    return encoded_str

def free_block(block):
    nums = []
    blockstream = bin(block)[2:].zfill(32)
    words_count = int(blockstream[:4], 2)
    words_len = PAYLOAD_MAX / words_count
    blockstream = blockstream[4:]
    for word_num in range(words_count):
        num = blockstream[word_num*words_len:(word_num+1)*words_len]
        if int(num, 2) == 0:
            break
        nums.append(int(num, 2))
    return nums

def decode(bytestream):
    blocks = varbyte.decode(bytestream)
    doc_ids = []
    for block in blocks:
        some_doc_ids = free_block(block)
        doc_ids.extend(some_doc_ids)
    return doc_ids

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