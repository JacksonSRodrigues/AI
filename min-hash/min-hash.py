import binascii
import random
import numpy as np

def chunked_iterator(extending_function):
    def wrapper(item_count = 1,
                chunk_length=1000, 
                chunk_input=lambda start,end: [],
                chunk_output=lambda start,end,shingles:None):
        c_start_item = 0
        while c_start_item < item_count:
            c_end_item = c_start_item + chunk_length
            if c_end_item > item_count:
                c_end_item = item_count

            chunked_items = chunk_input(c_start_item,c_end_item)
            result = extending_function(chunked_items)
            chunk_output(c_start_item,c_end_item, result)
            c_start_item = c_end_item
    return wrapper


def chunked_comparison(extending_function):
    
    def next_chunk_end(start, length, limit):
        end = start + length
        if end > limit:
            end = limit
        return end
    
    def wrapper(item_count = 1,
                chunk_length=1000, 
                chunk_input=lambda start,end: [],
                chunk_output=lambda row_range,column_range,matrix:None):
        r_start_item = 0
        
        while r_start_item < item_count:
            r_end_item = next_chunk_end(r_start_item,chunk_length,item_count) 
            row_chunks = chunk_input(r_start_item,r_end_item)
            print(len(row_chunks))
            c_start_item = 0
            while c_start_item < item_count:
                c_end_item = next_chunk_end(c_start_item,chunk_length,item_count)
                column_chunks = chunk_input(c_start_item,c_end_item)
                result = extending_function(row_chunks,column_chunks,(r_start_item,r_end_item),(c_start_item,c_end_item))
                chunk_output((r_start_item,r_end_item),(c_start_item,c_end_item), result)
                c_start_item = c_end_item
                
            r_start_item = r_end_item
    return wrapper
        

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
def generate_shingles_for_items(row_data_collection):
    return list(map(lambda row: get_shingles(row, hasher=lambda x:binascii.crc32(bytearray(x,'UTF-8')) & 0xffffffff),
                    row_data_collection))
    
@chunked_iterator
def generate_signature_for_items(rows):
    global hash_count
    return list(map(lambda row: list(map(lambda c_index:get_hash_code(row, coeffs_a[c_index],coeffs_b[c_index],nearest_prime_larger_than_max_shingle_id ),
            range(0,hash_count))),
            rows))

@chunked_comparison
def generate_signature_comparision(rows,columns,row_range,column_range):
    m_rows = []
    for row in rows:
        size = len(row)
        m_cols = []
        for column in columns:
            match=sum(map(lambda index: row[index]==column[index] ,range(0,size)))
            m_cols.append(match/size)
        m_rows.append(m_cols)
    return m_rows

max_shingle_id = 2**32 - 1
nearest_prime_larger_than_max_shingle_id = 4294967311 
hash_count = 10


source = [['abc','def','hij','klm','abc','der','sdf','fwr'],
          ['def','hij','der','sdf','fwr'],
          ['klm','abc','der','sdf','fwr'],
          ['hij','klm','abc','der','sdf','fwr'],
          ['der','sdf','fwr']]

shingles = []
generate_shingles_for_items(item_count=len(source), chunk_length=2, 
                            chunk_input=lambda start,end: source[start:end], 
                            chunk_output=lambda start,end, data: shingles.extend(data))

coeffs_a = get_random_coefficients(hash_count,max_shingle_id) 
coeffs_b = get_random_coefficients(hash_count,max_shingle_id)

signatures = []
generate_signature_for_items(item_count=len(shingles),chunk_length=2,
                             chunk_input= lambda start,end: shingles[start:end],
                             chunk_output= lambda start,end, data: signatures.extend(data))

signature_matrix = np.zeros(shape=(len(signatures),len(signatures)))
def write_signature_chunk(row_range,col_range,data):
    global signature_matrix
    r_start,r_end = row_range
    c_start,c_end = col_range
    for row in range(r_start,r_end):
        np.put(signature_matrix[row],range(c_start,c_end),data[row-r_start])
    print('writing',row_range,col_range,data)
  

generate_signature_comparision(item_count=len(signatures), chunk_length=2,
                               chunk_input=lambda start,end: signatures[start:end],
                               chunk_output= write_signature_chunk)





    

    
