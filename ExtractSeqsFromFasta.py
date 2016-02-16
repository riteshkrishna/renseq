#!/usr/bin/env python

__author__ = 'ritesh'
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


def extract_requiredSequences(fastaFile,accessionFile,out_acc_fasta):
    '''
    We need only those sequences that start with a particular pattern in accession.
    We provide the pattern here and pull out the ones required
    '''

    f_out = open(out_acc_fasta,'w')
    f_in = open(accessionFile, 'r')

    L = list()
    for line in f_in:
        L.append(line.rstrip())
    print ('L Before :', len(L))

    # Find unique accessions
    set_L = set(L)
    print ('set_L length :', len(set_L))

    new_L = list(set_L)

    mygenerator = fasta_iter(fastaFile)
    for head, seq in mygenerator:
        stripped_head = head.lstrip('>')
        head_to_search = stripped_head.split()
        if head_to_search[0] in new_L:
            f_out.write(head)
            f_out.write('\n')
            f_out.write(seq)
            f_out.write('\n')

    f_in.close()
    f_out.close()


def main(argv):
        fastaFile = ''
        accessionFile = ''
	out_acc_fasta = ''

        try:
                opts, args = getopt.getopt(argv,"i:o:a:",["in=","out=","accn="])
        except getopt.GetoptError:
                print 'ExtractSeqsFromFasta.py -i fastaFile -a accesion.txt -o outFasta.txt'
                sys.exit(2)

        for opt, arg in opts:
                if opt in ("-i","--in"):
                        fastaFile = arg
                elif opt in ("-o","--out"):
                        out_acc_fasta = arg
		elif opt in ("-a","accn="):
			accessionFile = arg

        print 'Input Fasta :', fastaFile
        print 'Accession file:', accessionFile
	print 'Out Fasta: ', out_acc_fasta


    	extract_requiredSequences(fastaFile,accessionFile,out_acc_fasta)

if __name__ == "__main__":
        main(sys.argv[1:])


##if __name__ == "__main__":
##
##
##    # Fasta file that you want to use
##    fastaFile = '../Analysis/assembly/out_assembly/out.61/case_gapcloser.scafSeq'
##    # File containing FASTA accessions
##    accessionFile = '../Analysis/out_61_blastn_hits_gt200_90p_eval05_genenames.txt'
##    # Output FASTA file
##    out_acc_fasta = '../Analysis/out_61_blastn_hits_gt200_90p_eval05_genenames.fasta'
##
##    extract_requiredSequences(fastaFile,accessionFile,out_acc_fasta)



