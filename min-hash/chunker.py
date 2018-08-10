#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 23:42:25 2018

@author: jackson
"""


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


def chunked_comparator(extending_function):
    
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
            c_start_item = 0
            while c_start_item < item_count:
                c_end_item = next_chunk_end(c_start_item,chunk_length,item_count)
                column_chunks = chunk_input(c_start_item,c_end_item)
                result = extending_function((r_start_item,r_end_item),(c_start_item,c_end_item),row_chunks,column_chunks)
                chunk_output((r_start_item,r_end_item),(c_start_item,c_end_item), result)
                c_start_item = c_end_item
                
            r_start_item = r_end_item
    return wrapper

def chunked_condtional_comparator(extending_function):
    
    def next_chunk_end(start, length, limit):
        end = start + length
        if end > limit:
            end = limit
        return end
    
    def wrapper(item_count = 1,
                chunk_length=1000, 
                chunk_conditional = lambda row_range,column_range:[],
                chunk_input=lambda start,end: [],
                chunk_output=lambda row_range,column_range,matrix:None):
        r_start_item = 0
        
        while r_start_item < item_count:
            r_end_item = next_chunk_end(r_start_item,chunk_length,item_count) 
            row_chunks = chunk_input(r_start_item,r_end_item)
            c_start_item = 0
            while c_start_item < item_count:
                c_end_item = next_chunk_end(c_start_item,chunk_length,item_count)
                #print('----c',c_start_item,c_end_item)
                column_chunks = chunk_input(c_start_item,c_end_item)
                print('----c',c_start_item,c_end_item,':',len(column_chunks))
                condition_chunk = chunk_conditional((r_start_item,r_end_item),(c_start_item,c_end_item))
                print((r_start_item,r_end_item),(c_start_item,c_end_item),condition_chunk)
                result = extending_function((r_start_item,r_end_item),(c_start_item,c_end_item),condition_chunk,row_chunks,column_chunks)
                chunk_output((r_start_item,r_end_item),(c_start_item,c_end_item), result)
                c_start_item = c_end_item
                
            r_start_item = r_end_item
    return wrapper