__author__ = 'riteshk'

import sys, getopt

"""
    The FASTA index file (.fai) as created from samtools faidx, creates a text file with 5 columns. These columns are
    accession, length, offset of the first base of the given accession, length of fasta lines and line blen (guess that
    is length of fasta lines + 1). this file needs to be read line by line and a corresponding BED3 file can be created.
"""


def create_bed3(fai_file, bed3_file):
    f_in = open(fai_file, 'r')
    f_out = open(bed3_file, 'w')

    for line in f_in:
        fields = line.split('\t')
        if len(fields) == 5:
            accession = fields[0]
            size = int(fields[1]) - 1
            f_out.write(accession + "\t" + str(0) + "\t" + str(size) + "\n")

    f_in.close()
    f_out.close()


def main(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print ('CreateBED3fromFastaIndex.py -i <file.fai> -o <out.bed>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('CreateBED3fromFastaIndex.py -i <file.fai> -o <out.bed>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg

    print ('Input file is ', inputfile)
    print ('Output file is ', outputfile)
    create_bed3(inputfile, outputfile)


if __name__ == "__main__":
    main(sys.argv[1:])
