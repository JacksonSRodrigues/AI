#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 23:42:25 2018

@author: jackson
"""

import types
import functools

def func_copy(f):
    g = types.FunctionType(f.__code__, f.__globals__, name=f.__name__,
                           argdefs=f.__defaults__,
                           closure=f.__closure__)
    g = functools.update_wrapper(g, f)
    g.__kwdefaults__ = f.__kwdefaults__
    return g


def _named_args(**kwargs):
    return kwargs

    

def chunked_iterator(extending_function):
    extending_func_copy = func_copy(extending_function)
    def wrapper(item_count = 1,
                chunk_length=1000, 
                chunk_input=lambda start,end: [],
                chunk_output=lambda start,end,shingles:None):
        c_start_item = 0
        while c_start_item < item_count:
            c_end_item = c_start_item + chunk_length
            if c_end_item > item_count:
                c_end_item = item_count

            named_args = chunk_input(c_start_item,c_end_item)
            result = extending_function(**named_args)
            chunk_output(c_start_item,c_end_item, result)
            
            c_start_item = c_end_item
            
    extending_func_copy._chunked = wrapper
    return extending_func_copy



def chunked_comparator(extending_function):
    extending_func_copy = func_copy(extending_function)
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
            #row_chunks = chunk_input(r_start_item,r_end_item)
            c_start_item = 0
            while c_start_item < item_count:
                c_end_item = next_chunk_end(c_start_item,chunk_length,item_count)
                #column_chunks = chunk_input(c_start_item,c_end_item)
                named_args = chunk_input((r_start_item,r_end_item),(c_start_item,c_end_item))
                result = extending_function((r_start_item,r_end_item),(c_start_item,c_end_item),**named_args)
                chunk_output((r_start_item,r_end_item),(c_start_item,c_end_item), result)
                c_start_item = c_end_item
                
            r_start_item = r_end_item
    
    extending_func_copy._chunked = wrapper
    return extending_func_copy
