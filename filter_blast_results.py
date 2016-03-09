__author__ = 'ritesh'

import sys, getopt


def parse_blast(blast_results, outfile, length_thres, eval_thres, aln_percent):
    fin = open(blast_results)
    fout = open(outfile, 'w')

    # Count starts from 0
    col_alnpercent = 2
    col_length = 3
    col_eval = 10

    print('Paramaters : ' + str(length_thres) + '\t' + str(eval_thres) + '\t' + str(aln_percent))
	
    for line in fin:
        blast_line = line.split('\t')
        if len(blast_line) != 12:
	    print('Skip : ' + line)
            continue
        else:
            aln = float(blast_line[col_alnpercent])
            length = int(blast_line[col_length])
            evalue = float(blast_line[col_eval])

        if ((aln >= aln_percent) and (length >= length_thres) and (evalue <= eval_thres)):
            fout.write(line)

    fin.close()
    fout.close()


def main(argv):

    try:
        opts, args = getopt.getopt(argv, "i:o:l:e:a:", ["in=", "out=", "length_thresh=", "evalue_thres=", "aln_percent="])
    except getopt.GetoptError:
        print 'filter_blast_results.py -i blastfile.txt  -o filtered_output.txt -l 100 -e 0.0001 -a 90'
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-i", "--in"):
            blast_results = arg
        elif opt in ("-o", "--out"):
            outfile = arg
        elif opt in ("-l", "length_thresh="):
            length_thres = int(arg)
        elif opt in ("-e", "evalue_thres="):
            eval_thres = float(arg)
        elif opt in ("-a", "aln_percent="):
            aln_percent = float(arg)

    parse_blast(blast_results, outfile, length_thres, eval_thres, aln_percent)



if __name__ == "__main__":
    main(sys.argv[1:])


