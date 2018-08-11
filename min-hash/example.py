#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 10 15:07:24 2018

@author: jackson
"""
import numpy as np
import min_hash
from chunker import _named_args
import tables
import memory_logger

max_shingle_id = 2**32 - 1
nearest_prime_larger_than_max_shingle_id = 4294967311 
hash_count = 10


source = [['abc','def','hij','klm','abc','der','sdf','fwr'],
          ['def','hij','der','sdf','fwr'],
          ['klm','abc','der','sdf','fwr'],
          ['hij','klm','abc','der','sdf','fwr'],
          ['der','sdf','fwr']]


# Generate shingle from source

h5file_path = 'document_sim.h5'
h5file = tables.open_file(h5file_path, mode='a')

shingles = h5file.create_vlarray(h5file.root, 'shingles', tables.Int64Atom(shape=()), filters=tables.Filters(1))
#shingles = []
def read_documents(start,end):
    if start % 100000 == 0:
        memory_logger.log_ram_usage(start)
    return _named_args(rows=source[start%5:start%5+end-start])


def write_shingles(start,end, data):
    global shingles
    for row in data:
        shingles.append(row)

min_hash.generate_shingles_for_items(item_count=1000000, chunk_length=5, 
                            chunk_input=read_documents, 
                            chunk_output=write_shingles)
h5file.close()


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


With In memory Array
0  - ram:  156.8MB
100000  - ram:  161.8MB
200000  - ram:  188.6MB
300000  - ram:  215.4MB
400000  - ram:  242.3MB
500000  - ram:  269.0MB
600000  - ram:  296.1MB
700000  - ram:  323.0MB
800000  - ram:  350.8MB
900000  - ram:  378.3MB

With Pytables VLArray
0  - ram:  159.3MB
100000  - ram:  159.3MB
200000  - ram:  159.3MB
300000  - ram:  159.3MB
400000  - ram:  159.3MB
500000  - ram:  159.3MB
600000  - ram:  159.3MB
700000  - ram:  159.3MB
800000  - ram:  159.3MB
900000  - ram:  159.3MB