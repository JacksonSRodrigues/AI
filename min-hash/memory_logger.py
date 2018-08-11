#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 11 12:36:40 2018

@author: jackson
"""

import os
import psutil
process = psutil.Process(os.getpid())

def size_format(b):
    if b < 1000:
              return '%i' % b + 'B'
    elif 1000 <= b < 1000000:
        return '%.1f' % float(b/1000) + 'KB'
    elif 1000000 <= b < 1000000000:
        return '%.1f' % float(b/1000000) + 'MB'
    elif 1000000000 <= b < 1000000000000:
        return '%.1f' % float(b/1000000000) + 'GB'
    elif 1000000000000 <= b:
        return '%.1f' % float(b/1000000000000) + 'TB'

def log_ram_usage(info=''):
    global process
    print(info,' - ram: ',size_format(process.memory_info().rss))