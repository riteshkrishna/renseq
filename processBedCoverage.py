#!/usr/bin/python

def processBed(bedfile,outfile):
    fin = open(bedfile)
    fout = open(outfile,'w')

    for line in fin:
        parts = line.split('\t')
        coverage = parts[len(parts)-1]
        if float(coverage) > 0.0:
            identifier = parts[3]
            id_name = identifier.split(';')
            name = id_name[0].split(':')
            final_name=name[1]
            fout.write(parts[0] + '\t' + parts[1] + '\t' + parts[2]
                  + '\t' + final_name + '\t' + parts[4]
                  + '\t' + parts[5] + '\t' + parts[6] + '\t' + parts[7])


    fin.close()
    fout.close()

if __name__ == "__main__":
    bedFile = '/Users/ritesh/Ritesh_Extra_Work/wheat/CS_CS27.sorted.bed'
    geneFile = '/Users/ritesh/Ritesh_Extra_Work/wheat/filteredGenes_CS_CS27.sorted.bed'
    processBed(bedFile,geneFile)