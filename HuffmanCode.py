#!/usr/bin/env python
'''
Copyright 2018 Suhird Singh (UWin License)
This is an intellectual property
Incase of any distribution rights, copyright, modification,
please contact the author at Suhirdsingh92@gmail.com

'''
__author__ = 'Suhird Singh'


import os, json,sys
from collections import Counter
from heapq import heapify, heappop, heappush
from myownutils import _to_Bytes, pad_encoded_text, remove_padding
from argparse import ArgumentParser
#follwing libraries are 3rd party and needs to be installed
from bitstring import BitArray



def encode(file_data):
	symb2freq = Counter(file_data)
	heap = [[wt, [sym, '']] for sym, wt in symb2freq.items()]
	heapify(heap)
	while len(heap) > 1:
		lo = heappop(heap)
		hi = heappop(heap)
		for pair in lo[1:]:
			pair[1] = '0' + pair[1]
		for pair in hi[1:]:
			pair[1] = '1' + pair[1]
		heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
	return sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))


def decode(huffman_json_file,encoded_file):
	temp_str = ''
	final_decoded_str = ''
	json_data = open(huffman_json_file).read()
	huffman_tree = json.loads(json_data)
	with open(encoded_file,'rb') as bin_file:
		data = bin_file.read()
	_bitstream = BitArray(bytes=data)
	encoded_text = remove_padding(str(_bitstream.bin))
	for c in encoded_text:
		temp_str += c
		# print(temp_str)
		for _arr in huffman_tree:
			if temp_str == _arr[1]:
				final_decoded_str += _arr[0]
				temp_str = ''

	return final_decoded_str



def original_file_to_bin(data):
	#print('Original bit Stream=', ''.join(format(ord(x), 'b') for x in data))
	data_bit_stream = ''.join(format(ord(x), 'b') for x in data)

	with open('Original_Bit_Form.bin', 'wb') as original_bin_file:
		original_bin_file.write(_to_Bytes(data_bit_stream))


def huffman_code_to_file(data,huff):
	coded_bit_stream = ''.join(i[1] for char in data for i in huff if char == i[0])
	padded_coded_text = pad_encoded_text(coded_bit_stream)
	#print(padded_coded_text)
	coded_text_in_byte_form = _to_Bytes(padded_coded_text)
	#print(coded_text_in_byte_form)
	with open('Huffman_Encoded_file.bin','wb') as encoded_file:
		encoded_file.write(coded_text_in_byte_form)
	# The above comprehension means as show below..
	# for str in string:
	# 	for i in huff:
	# 		if str == i[0]:
	# 			coded_string+=i[1]

def huffman_tree_to_file(huff):
	with open('huffman_tree.json','w') as my_file:
		json.dump(huff, my_file)


if __name__ == '__main__':
	parser = ArgumentParser(description='Code to Compress/Extract a file.')
	parser.add_argument('-a','--action',required=True,help='only 2 values(encode/decode)')
	parser.add_argument('-f','--filename',required=True, help='original text filename')
	parser.add_argument('-huff','--huffman',help = 'name of huffman tree file')
	result = parser.parse_args()

	FILENAME = result.filename
	if result.action == 'encode':
		print('##Reading Text File##')
		with open(FILENAME, 'r') as text_file:
			data = text_file.read()
		print('##Performaing Huffman Encoding##')
		huff = encode(data)
		#print('Final HuffMan Tree=', huff)
		print('##Converting original file to bin file##')
		#original_file_to_bin(data)
		print('##Writing Encoded bit stream to Encoded bin file')
		huffman_code_to_file(data,huff)
		print('##Saving Huffman Tree to json file')
		huffman_tree_to_file(huff)
		#_o = os.path.getsize('Original_Bit_Form.bin')
		_c = os.path.getsize('Huffman_Encoded_file.bin')
		_t = os.path.getsize(FILENAME)
		#print(f'Original Binary File: {_o} bytes')
		print(f'Original Text File:{_t} bytes')
		print(f'Compressed Binary File: {_c} bytes')
		print('Compressed file to about {}% of original'.format(round((((_t - _c) / _t) * 100), 0)))
	elif result.action=='decode':
		decoded_text = decode(result.huffman, result.filename)
		print('Decoded Text=',decoded_text)

