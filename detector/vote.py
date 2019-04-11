# -*- coding=utf-8 -*-
from base import *
def vote(X_14, X_recent):
    '''
    simple vote function
    :return: 1 denotes normal, 0 denotes abnormal
    '''
    votel = [0,0]
    basel = [stddev_from_ewma(X_recent),
             recent_compare(X_recent),
             tail_compare(X_recent),
             absolute_periodicity_min(X_14),
             absolute_periodicity_max(X_14),
             amplitude_periodicity(X_14)
             ]
    
    for b in basel:
        votel[b] += 1
    if votel[0] > votel[1]:
        return 0
    return 1
    