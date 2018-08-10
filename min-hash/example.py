#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 15:07:24 2018

@author: jackson
"""
import numpy as np
import min_hash
from chunker import _named_args

max_shingle_id = 2**32 - 1
nearest_prime_larger_than_max_shingle_id = 4294967311 
hash_count = 10


source = [['abc','def','hij','klm','abc','der','sdf','fwr'],
          ['def','hij','der','sdf','fwr'],
          ['klm','abc','der','sdf','fwr'],
          ['hij','klm','abc','der','sdf','fwr'],
          ['der','sdf','fwr']]

# Generate shingle from source
shingles = []
min_hash.generate_shingles_for_items(item_count=len(source), chunk_length=2, 
                            chunk_input=lambda start,end: _named_args(rows=source[start:end]), 
                            chunk_output=lambda start,end, data: shingles.extend(data))


# Generate random coefficients
coefficients_a = min_hash.get_random_coefficients(hash_count,max_shingle_id) 
coefficients_b = min_hash.get_random_coefficients(hash_count,max_shingle_id)


# Generate Signature for each row shingles
signatures = []
min_hash.generate_signature_for_items(item_count=len(shingles),chunk_length=2,
                             chunk_input= lambda start,end: _named_args(rows=shingles[start:end],
                                                                        coeffs_a=coefficients_a,
                                                                        coeffs_b=coefficients_b,
                                                                        hash_count=hash_count,
                                                                        max_prime=nearest_prime_larger_than_max_shingle_id),
                             chunk_output= lambda start,end, data: signatures.extend(data))



##################################
# generate problisting similarity with signatures
##################################
signature_matrix = np.zeros(shape=(len(signatures),len(signatures)))

def read_signature_chunks(row_range,col_range):
    global signatures
    r_start,r_end = row_range
    c_start,c_end = col_range
    return _named_args(rows=signatures[r_start:r_end],columns=signatures[c_start:c_end])

def write_signature_comparison_chunk(row_range,col_range,data):
    global signature_matrix
    r_start,r_end = row_range
    c_start,c_end = col_range
    for row in range(r_start,r_end):
        np.put(signature_matrix[row],range(c_start,c_end),data[row-r_start])
    #print('writing',row_range,col_range,data)
  

min_hash.generate_signature_comparision(item_count=len(signatures), chunk_length=2,
                               chunk_input=read_signature_chunks,
                               chunk_output= write_signature_comparison_chunk)


##################################
# generate final similarity matrix
##################################
simlarity_matrix = np.zeros(shape=(len(signatures),len(signatures)))

def read_shingles_and_signature_matrix_chunk(row_range,column_range):
    global signature_matrix
    global shingles
    r_start,r_end = row_range
    c_start,c_end = column_range
    return _named_args(rows=shingles[r_start:r_end], columns=shingles[c_start:c_end],
                       conditional_matrix=(signature_matrix[r_start:r_end,c_start:c_end] >= 0.5))

def write_similarity_matrix_chunk(row_range,col_range,data):
    global simlarity_matrix
    r_start,r_end = row_range
    c_start,c_end = col_range
    for row in range(r_start,r_end):
        np.put(simlarity_matrix[row],range(c_start,c_end),data[row-r_start])
    #print('writing',row_range,col_range,data)
    
min_hash.generate_conditional_comparision(item_count=len(signatures), chunk_length=2,
                               chunk_input=read_shingles_and_signature_matrix_chunk,
                               chunk_output= write_similarity_matrix_chunk)