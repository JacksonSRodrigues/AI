import binascii

def get_shingles(words, k=2, hasher=lambda x: x):
  shingles = set()
  for i in range(0,len(words)-k+1):
    shingle = ' '.join(words[i:i+k])
    shingle = hasher(shingle)
    shingles.add(shingle)
  return shingles


def generate_shingles(data_source=lambda start,end: [], rows=1, page_size=1000, data_write=lambda start,end,shingles:None):

  c_start_row = 0
  while c_start_row < rows:
    c_end_row = c_start_row + page_size
    if c_end_row > rows:
      c_end_row = rows

    row_data_collection = data_source(c_start_row,c_end_row)
    shingles = list(map(lambda row: get_shingles(row, hasher=lambda x:x# binascii.crc32(bytearray(x)) & 0xffffffff 
    ),row_data_collection))
    data_write(c_start_row,c_end_row, shingles)
    
    c_start_row = c_end_row

source = [['abc','def','hij','klm','abc','der','sdf','fwr'],
          ['def','hij','der','sdf','fwr'],
          ['klm','abc','der','sdf','fwr'],
          ['hij','klm','abc','der','sdf','fwr'],
          ['der','sdf','fwr']]
def fetch_data(start,end):
  print('fetching',start,end)
  return source[start:end]

def write_data(start,end,data):
  print('writing',start,end,data)

generate_shingles(fetch_data,rows=len(source),page_size=2,data_write=write_data)

print(get_shingles(['abc','def','hij','klm','abc'], k=1))