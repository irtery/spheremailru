 # coding: utf-8


import sys
import os
import re
import random
import time
from sklearn.cluster import MiniBatchKMeans
import numpy as np
import urlparse
import urllib
import re


class sekitei:
    features = {}
    num_clusters = 11

    cluster = MiniBatchKMeans(num_clusters, max_iter=400, random_state=0, batch_size=500)

    def features_names(self):
        return self.features.keys()

sekitei_instance = sekitei()

def get_segments(url):
    segments = urlparse.urlparse(url).path.split('/')
    segments = filter(lambda segment: segment != '', segments)
    return segments

def get_params(url):
    params = urlparse.parse_qs(url)
    for key, value in params.iteritems():
        tmp = key.split('?')
        if len(tmp) == 2:
            params[tmp[1]] = params.pop(key)
    for key, _ in params.iteritems():
        params[key] = params[key][0]
    return params

def add_segments_features(segments, features, url_features):
    inc_feature('segments:' + str(len(segments)), features, url_features)
    for i, segment in enumerate(segments):
        segment = urllib.unquote(segment)
        inc_feature('segment_len_' + str(i) + ':' + str(len(segment)), features, url_features)
        inc_feature('segment_name_' + str(i) + ':' + segment, features, url_features)

        ext = segment.split('.')
        if len(ext) == 2:
            inc_feature('segment_ext_' + str(i) + ':' + ext[1], features, url_features)  
        if re.match(r'\d+$', segment):
            inc_feature('segment_[0-9]_' + str(i) + ':1', features, url_features)
        else:
            if re.match(r'\d+', segment):
                inc_feature('segment_substr[0-9]_' + str(i) + ':1', features, url_features)
                if len(ext) == 2:
                    inc_feature('segment_ext_substr[0-9]_' + str(i) + ':' + ext[1], features, url_features)

def add_params_features(params, features, url_features):
    for param_key, param_value in params.iteritems():
        param_key = urllib.unquote(param_key)
        param_value = urllib.unquote(param_value)
        inc_feature('param_name:' + param_key, features, url_features)
        inc_feature('param:'+ param_key + '=' + str(param_value), features, url_features)

def inc_feature(name, features, url_features):
    if name in features:
        features[name] += 1
    else:
        features[name] = 1
    url_features.append(name)

def extract_url_features(url, features):
    url_features = []
    segments = get_segments(url)
    add_segments_features(segments, features, url_features)

    params = get_params(url)
    add_params_features(params, features, url_features)
    return url_features

def extract_features(urls, urls_features):
    N = len(urls)
    alpha = 0.09

    features = {}
    imp_features = {}

    for url in urls:
        url_features = extract_url_features(url, features)
        urls_features.append(url_features)

    for k, v in sorted(features.iteritems(), key=lambda (k,v):-v):
        if v > N*alpha:
           imp_features[k] = v
    return imp_features

def make_X(important_fnames, urls_with_fnames):
    X = np.zeros((len(urls_with_fnames), len(important_fnames)))
    for i, url_fs in enumerate(urls_with_fnames):
        for fname in url_fs:
            if fname in important_fnames:
                X[i][important_fnames.index(fname)] = 1
    return X


def define_segments(QLINK_URLS, UNKNOWN_URLS, QUOTA):
    global sekitei_instance
    sekitei_instance = sekitei()
    urls_features = []

    urls = list(QLINK_URLS)
    urls.extend(UNKNOWN_URLS)

    sekitei_instance.features = extract_features(urls, urls_features)

    X = make_X(sekitei_instance.features_names(), urls_features)
    
    sekitei_instance.cluster.fit(X)
    labels = sekitei_instance.cluster.labels_
    clusters = np.unique(labels)

    sekitei_instance.clusters_quota = np.zeros(sekitei_instance.num_clusters, dtype=int)

    q_clusters, q_counts = np.unique(labels[:len(QLINK_URLS)], return_counts=True)

    for i, cluster in enumerate(q_clusters):
        sekitei_instance.clusters_quota[cluster] = int(q_counts[i] * QUOTA / len(QLINK_URLS))

#
# returns True if need to fetch url
#
def fetch_url(url):
    global sekitei_instance

    features = {}
    url_features = [[]]
    url_features[0] = extract_url_features(url, features)
   
    X = make_X(sekitei_instance.features_names(), url_features)

    pred_cluster = sekitei_instance.cluster.predict(X)[0]

    if sekitei_instance.clusters_quota[pred_cluster] > 0:
        sekitei_instance.clusters_quota[pred_cluster] -= 1
        return True
    
    return False
