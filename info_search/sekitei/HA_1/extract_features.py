# coding: utf-8
import sys

# you may add imports if needed (and if they are installed)
import random
import urlparse
import urllib
import re
import operator
import collections

def cut_links(file_name, quantity):
    file = open(file_name)
    # random.seed(0)
    filelinks = []
    somelinks = []
    for line in file:
        filelinks.append(line)
    file.close()
    totallinks = len(filelinks) - 1
    for _ in range(quantity):
        link = filelinks[random.randint(0,totallinks)][:-1]
        somelinks.append(link)
    return somelinks

def get_segments(link):
    segments = urlparse.urlparse(link).path.split('/')
    segments = filter(lambda segment: segment != '', segments)
    return segments

def get_params(link):
    params = urlparse.parse_qs(link)
    for key, value in params.iteritems():
        tmp = key.split('?')
        if len(tmp) == 2:
            params[tmp[1]] = params.pop(key)
    for key, _ in params.iteritems():
        params[key] = params[key][0]
    return params

def add_segments_features(segments, features):
    inc_feature('segments:' + str(len(segments)), features)
    for i, segment in enumerate(segments):
        segment = urllib.unquote(segment)
        inc_feature('segment_len_' + str(i) + ':' + str(len(segment)), features)
        inc_feature('segment_name_' + str(i) + ':' + segment, features)

        ext = segment.split('.')
        if len(ext) == 2:
            inc_feature('segment_ext_' + str(i) + ':' + ext[1], features)  
        if re.match(r'\d+$', segment):
            inc_feature('segment_[0-9]_' + str(i) + ':1', features)
        else:
            if re.match(r'\D+\d+\D', segment):
                inc_feature('segment_substr[0-9]_' + str(i) + ':1', features)
                if len(ext) == 2:
                    inc_feature('segment_ext_substr[0-9]_' + str(i) + ':' + ext[1], features)

def add_params_features(params, features):
    for param_key, param_value in params.iteritems():
        param_key = urllib.unquote(param_key)
        param_value = urllib.unquote(param_value)
        inc_feature('param_name:' + param_key, features)
        inc_feature('param:'+ param_key + '=' + str(param_value), features)

def inc_feature(name, features):
    if name in features:
        features[name] += 1
    else:
        features[name] = 1

def extract_features(INPUT_FILE_1, INPUT_FILE_2, OUTPUT_FILE):
    N = 1000
    freq_edge = 100

    links = cut_links(INPUT_FILE_1, N)
    links += cut_links(INPUT_FILE_2, N)

    features = {}

    for link in links:
        segments = get_segments(link)
        add_segments_features(segments, features)

        params = get_params(link)
        add_params_features(params, features)

    output = open(OUTPUT_FILE, 'w')
    for k, v in sorted(features.iteritems(), key=lambda (k,v):-v):
        if v > freq_edge:
            output.write(k + '\t' + str(v) + '\n')
    output.close()
