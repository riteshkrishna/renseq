__author__ = 'riteshk'

# counts length of FASTA sequences
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

    fout = open(output,'w')
    mygenerator = fasta_iter(fastaFile)
    for head, seq in mygenerator:
        stripped_head = head.lstrip('>')
        fout.write(stripped_head + '\t' + str(len(seq)) + '\n')

    fout.close()

if __name__ == "__main__":
    fastaFile = ''
    outputFile = ''
    count(fastaFile,outputFile)