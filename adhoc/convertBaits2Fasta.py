__author__ = 'ritesh'

'''
    script to deal with 4-column bait file provided by LG. Creates FASTA file of bait sequences.
'''

def convertbaits2fasta(baitfile, outfasta):
    fin = open(baitfile)
    fout = open(outfasta,'w')

    header = fin.readline()
    print (header)

    for line in fin:
        line_parts = line.split('\t')
        if len(line_parts) >= 4:
            id = line_parts[1]
            seq = line_parts[2]
            towrite= '>' + id + '\n' + seq + '\n'
            fout.write(towrite)
        else:
            print(line)


    fin.close()
    fout.close()

if __name__ == "__main__":
    baitfile = '/home/ritesh/Ritesh_Work/wheat/LauraData/NBS-LRR_associated_probes.txt'
    fastafile = '/home/ritesh/Ritesh_Work/wheat/LauraData/NBS-LRR_associated_probes_fasta.fa'
    convertbaits2fasta(baitfile,fastafile)
