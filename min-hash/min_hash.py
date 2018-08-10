import binascii
import random
import numpy as np
from chunker import chunked_iterator,chunked_comparator,chunked_condtional_comparator



def get_shingles(words, k=2, hasher=lambda x: x):
  shingles = set()
  for i in range(0,len(words)-k+1):
    shingle = ' '.join(words[i:i+k])
    shingle = hasher(shingle)
    shingles.add(shingle)
  return list(shingles)

def get_hash_code(row_shingles, coeff_a, coeff_b, prime_greater_than_max_shingle):
    return min(map(lambda shingle_id: (coeff_a*shingle_id + coeff_b)% prime_greater_than_max_shingle, 
        row_shingles))
    
def get_random_coefficients(k, max_shingle):
    coefficients = set()
    while(len(coefficients) < k):
        coefficient = random.randint(0, max_shingle)
        coefficients.add(coefficient)
    return list(coefficients)

@chunked_iterator
def generate_shingles_for_items(rows):
    return list(map(lambda row: get_shingles(row, hasher=lambda x:binascii.crc32(bytearray(x,'UTF-8')) & 0xffffffff),
                    rows))
    
@chunked_iterator
def generate_signature_for_items(rows,coeffs_a,coeffs_b,hash_count,max_prime):
    return list(map(lambda row: list(map(lambda c_index:get_hash_code(row, coeffs_a[c_index],coeffs_b[c_index],max_prime),
            range(0,hash_count))),
            rows))

@chunked_comparator
def generate_signature_comparision(row_range,column_range,rows,columns):
    m_rows = []
    for row in rows:
        size = len(row)
        m_cols = []
        for column in columns:
            match=sum(map(lambda index: row[index]==column[index] ,range(0,size)))
            m_cols.append(match/size)
        m_rows.append(m_cols)
    return m_rows


@chunked_condtional_comparator
def generate_conditional_comparision(row_range,column_range,conditional_matrix,rows,columns):
    m_rows = []
    r_start,r_end = row_range
    c_start,c_end = column_range
    #print(len(rows),len(columns))
    for r_index in range(0,r_end-r_start):
        row = set(rows[r_index])
        m_cols = []
        #print('-r',r_index)
        for c_index in range(0,c_end-c_start):
            column = set(columns[c_index])
            match_percentage = 0
            #print('--c',c_index)
            if conditional_matrix[r_index][c_index]:
                match_percentage= len(row.intersection(column))/len(row.union(column))
            m_cols.append(match_percentage)
        m_rows.append(m_cols)
    return m_rows