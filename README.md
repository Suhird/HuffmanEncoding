# Huffman Compression and Decompression
### A Python implementation of Huffman Encoding and Decoding
#### Python 3 compatible 
A python program ***HuffmanCode.py*** is a command line tool which encodes a text file given as paramater and generates a compressed ***bin*** file along with a ***json*** file which saves the huffman tree.
The program uses ***priority queues*** for encoding and creation of tree.
Only ***bitstring*** was used as a third party library. Please install using pip.
```
pip install bitstring
```


The decoding is also done using the same ***HuffmanCode.py***.

#### How to run the program:
Command line syntax for running the program is as follows:
```
python HuffmanCode.py -a encode -f test.txt

python HuffmanCode.py -a decode -f Huffman_Encoded_file.bin -huff huffman_tree.json
```

