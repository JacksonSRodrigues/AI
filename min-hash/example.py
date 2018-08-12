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
import datetime

def get_node_from_pytable_file(hdf5file,node_path=""):
    _node = None
    if hdf5file.__contains__('/{}'.format(node_path)):
        _node = hdf5file.get_node('/{}'.format(node_path))
    return _node
    
def get_pytable_file(file_path,mode='a'):
    _h5file = tables.open_file(file_path, mode=mode)
    return _h5file

max_shingle_id = 2**32 - 1
nearest_prime_larger_than_max_shingle_id = 4294967311 
hash_count = 10
document_count = 10000
chunk_length = 1000


source = [['abc','def','hij','klm','abc','der','sdf','fwr'],
          ['def','hij','der','sdf','fwr'],
          ['klm','abc','der','sdf','fwr'],
          ['hij','klm','abc','der','sdf','fwr'],
          ['der','sdf','fwr']]

memory_logger.log_ram_usage('Started Process {}'.format(datetime.datetime.now()))

# Generate shingle from source
h5file_path = 'document_sim.h5'

h5file = get_pytable_file(h5file_path)
shingles = get_node_from_pytable_file(h5file,node_path='shingles')
if shingles is None:
    shingles = h5file.create_vlarray(h5file.root, 'shingles', tables.Int64Atom(shape=()), filters=tables.Filters(1))


def read_documents(start,end):
    if start % 10 == 0:
        memory_logger.log_ram_usage(start)
    return _named_args(rows=source[start%5:start%5+end-start])


def write_shingles(start,end, data):
    global shingles
    for row in data:
        shingles.append(row)

min_hash.generate_shingles_for_items(item_count=document_count, chunk_length=5, 
                            chunk_input=read_documents, 
                            chunk_output=write_shingles)
h5file.close()

memory_logger.log_ram_usage('Finished Generating Shingles {}'.format(datetime.datetime.now()))

# Generate random coefficients
coefficients_a = min_hash.get_random_coefficients(hash_count,max_shingle_id) 
coefficients_b = min_hash.get_random_coefficients(hash_count,max_shingle_id)


# Generate Signature for each row shingles
h5file = get_pytable_file(h5file_path)
shingles = get_node_from_pytable_file(h5file,'shingles')
signatures = get_node_from_pytable_file(h5file,'signatures')
if signatures is None:
    signatures = h5file.create_vlarray(h5file.root, 'signatures', tables.Int64Atom(shape=()), filters=tables.Filters(1))



def write_signatures(start,end, data):
    global signatures
    for row in data:
        signatures.append(row)

min_hash.generate_signature_for_items(item_count=document_count,chunk_length=chunk_length,
                             chunk_input= lambda start,end: _named_args(rows=shingles[start:end],
                                                                        coeffs_a=coefficients_a,
                                                                        coeffs_b=coefficients_b,
                                                                        hash_count=hash_count,
                                                                        max_prime=nearest_prime_larger_than_max_shingle_id),
                             chunk_output= write_signatures)
h5file.close()
memory_logger.log_ram_usage('Finished Generating Signatures {}'.format(datetime.datetime.now()))


##################################
# generate problisting similarity with signatures
##################################
def fill_zeros_earray_matrix(matrix,nrows,chunk_length=1000):
    current_row = 0
    while current_row < nrows:
        if current_row + chunk_length >= nrows:
            chunk_length = nrows - current_row
        matrix.append(np.zeros(shape=(chunk_length,nrows)))
        current_row = current_row+ chunk_length
    return matrix


h5file = get_pytable_file(h5file_path)
signatures = get_node_from_pytable_file(h5file,'signatures')
signature_matrix = get_node_from_pytable_file(h5file,'signature_matrix')
if signature_matrix is None:
    signature_matrix = h5file.create_earray(h5file.root, 'signature_matrix', 
                                            tables.Float64Atom(shape=()),
                                            shape=(0, document_count), 
                                            filters=tables.Filters(1),
                                            expectedrows=document_count)
    signature_matrix = fill_zeros_earray_matrix(signature_matrix,document_count,chunk_length)

    


def read_signature_chunks(row_range,col_range):
    global signatures
    r_start,r_end = row_range
    c_start,c_end = col_range
    memory_logger.log_ram_usage('{} , {} - {}'.format(row_range,col_range,datetime.datetime.now()))
    #print('read',len(signatures[r_start:r_end]))
    return _named_args(rows=signatures[r_start:r_end],columns=signatures[c_start:c_end])

def write_signature_comparison_chunk(row_range,col_range,data):
    global signature_matrix
    r_start,r_end = row_range
    c_start,c_end = col_range
    #print((r_start,r_end-1),'data-len',len(data))
    for row in range(r_start,r_end-1):
        # can only update individual row not intersection.
        _tmp_row = signature_matrix[row] # so fetch the whole row
        #print('write',row_range,col_range,' : row -inserted', row-r_start)
        np.put(_tmp_row,range(c_start,c_end),data[row-r_start]) # update desired section
        signature_matrix[row] = _tmp_row # set back values
        
  

min_hash.generate_signature_comparision(item_count=document_count, chunk_length=chunk_length,
                               chunk_input=read_signature_chunks,
                               chunk_output= write_signature_comparison_chunk)

h5file.close()
memory_logger.log_ram_usage('Finished Generating Signature Matrix {}'.format(datetime.datetime.now()))


##################################
# generate final similarity matrix
##################################
h5file = get_pytable_file(h5file_path)
shingles = get_node_from_pytable_file(h5file,'shingles')
signature_matrix = get_node_from_pytable_file(h5file,'signature_matrix')
simlarity_matrix = get_node_from_pytable_file(h5file,'simlarity_matrix')
if simlarity_matrix is None:
    simlarity_matrix = h5file.create_earray(h5file.root, 'simlarity_matrix', 
                                            tables.Float64Atom(shape=()),
                                            shape=(0, document_count), 
                                            filters=tables.Filters(1),
                                            expectedrows=document_count)
    simlarity_matrix = fill_zeros_earray_matrix(simlarity_matrix,document_count)



def read_shingles_and_signature_matrix_chunk(row_range,column_range):
    global signature_matrix
    global shingles
    r_start,r_end = row_range
    c_start,c_end = column_range
    memory_logger.log_ram_usage('{} , {} - {}'.format(row_range,column_range,datetime.datetime.now()))
    return _named_args(rows=shingles[r_start:r_end], columns=shingles[c_start:c_end],
                       conditional_matrix=(signature_matrix[r_start:r_end,c_start:c_end] >= 0.5))

def write_similarity_matrix_chunk(row_range,col_range,data):
    global simlarity_matrix
    r_start,r_end = row_range
    c_start,c_end = col_range
    #print('writing',row_range,col_range)
    for row in range(r_start,r_end):
        _tmp_row = simlarity_matrix[row] # so fetch the whole row
        np.put(_tmp_row,range(c_start,c_end),data[row-r_start]) # update desired section
        simlarity_matrix[row] = _tmp_row # set back values
        
    #print('writing',row_range,col_range,data)
    
min_hash.generate_conditional_comparision(item_count=document_count, chunk_length=chunk_length,
                               chunk_input=read_shingles_and_signature_matrix_chunk,
                               chunk_output= write_similarity_matrix_chunk)

h5file.close()

memory_logger.log_ram_usage('Finished Generating Similarity Matrix {}'.format(datetime.datetime.now()))