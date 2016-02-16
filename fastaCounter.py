#!/usr/bin/python
__author__ = 'riteshk'

# counts length of FASTA sequences

import sys, getopt
from itertools import groupby

def fasta_iter(fasta_name):
    """
    given a fasta file. yield tuples of header, sequence
    """
    fh = open(fasta_name)
    # ditch the boolean (x[0]) and just keep the header or sequence since
    # we know they alternate.
    faiter = (x[1] for x in groupby(fh, lambda line: line[0] == ">"))
    for header in faiter:
        header = header.next().strip()
        # join all sequence lines to one.
        seq = "".join(s.strip() for s in faiter.next())
        yield header, seq

def count(fastaFile, output):

    fout = open(output,"w")
    mygenerator = fasta_iter(fastaFile)
    for head, seq in mygenerator:
        stripped_head = head.lstrip('>')
	front_head = stripped_head.split()
        fout.write(front_head[0] + '\t' + str(len(seq)) + '\n')

    fout.close()

def main(argv):
	inputFile = ''
	outputFile = ''
	
	try:
		opts, args = getopt.getopt(argv,"i:o:",["in=","out="])
	except getopt.GetoptError:
		print 'fastaCounter.py -i fastaFile -o outFile.txt'
		sys.exit(2)
	
	for opt, arg in opts:
		if opt in ("-i","--in"):
			inputFile = arg
		elif opt in ("-o","--out"):
			outputFile = arg
	
	print 'Input file :', inputFile
	print 'Output file:', outputFile

	count(inputFile, outputFile)
if __name__ == "__main__":
	main(sys.argv[1:])
