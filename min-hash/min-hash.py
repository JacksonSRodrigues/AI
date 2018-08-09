import binascii
import random

def chunk_data_processor(extending_function):
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

@chunk_data_processor
def generate_shingles_for_items(row_data_collection):
    return list(map(lambda row: get_shingles(row, hasher=lambda x:binascii.crc32(bytearray(x,'UTF-8')) & 0xffffffff),
                    row_data_collection))
    
@chunk_data_processor
def generate_signature_for_items(rows):
    global hash_count
    return list(map(lambda row: list(map(lambda c_index:get_hash_code(row, coeffs_a[c_index],coeffs_b[c_index],nearest_prime_larger_than_max_shingle_id ),
            range(0,hash_count))),
            rows))
    

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

def fetch_data(start,end):
  print('fetching',start,end)
  return shingles[start:end]

def write_data(start,end,data):
  global signatures
  signatures.extend(data)
  print('writing',start,end,data)
  



    

    
