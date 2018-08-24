#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 24 15:10:12 2018

@author: jackson
"""

import  min_hash 

max_shingle_id = 2**32 - 1
nearest_prime_larger_than_max_shingle_id = 4294967311 
hash_count = 10
document_count = 10000
chunk_length = 1000
band_size=2


source = [['abc','def','hij','klm','abc','der','sdf','fwr'],
          ['def','hij','der','sdf','fwr'],
          ['klm','abc','der','sdf','fwr'],
          ['hij','klm','abc','der','sdf','fwr'],
          ['der','sdf','fwr'],
          ['1','2','3','4'],
          ['3','4','5','6'],
          ['5','6','7','8'],]


coefficients_a = min_hash.get_random_coefficients(hash_count,max_shingle_id) 
coefficients_b = min_hash.get_random_coefficients(hash_count,max_shingle_id)

shingles = min_hash.generate_shingles_for_items(source)
signatures = min_hash.generate_signature_for_items(shingles,coefficients_a,coefficients_b,hash_count,nearest_prime_larger_than_max_shingle_id)

def band_row_signature(signatures, sig_count=2):
    return list(map(lambda index: frozenset(signatures[index:index+sig_count]),
                    range(0,len(signatures),sig_count)))
    

def band_item_signatures(row_wise_signatures, sig_count=2):
    return list(map(lambda row_signatures:band_row_signature(row_signatures,sig_count), row_wise_signatures))

banded_signatures = band_item_signatures(signatures,band_size)

bucket_bands = {}
for index,band_items in enumerate(banded_signatures):
    for band_item in band_items:
        indices = bucket_bands.get(band_item)
        if indices is None:
            indices = []
        indices.append(index)
        bucket_bands[band_item] = indices
        
bucket_bands

