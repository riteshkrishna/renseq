__author__ = 'riteshk'

'''
    bedtools intersect with options -wa and -wb result in a TSV file as noted in the onenote entry on March 9.
    Example entry:
    1A 100519 103705 ID=gene:Traes_1AS_BEE845715;biotype=protein_coding;version=1 1A 101600 102000 2 125 400 0.3125
    1A 100519 103705 ID=gene:Traes_1AS_BEE845715;biotype=protein_coding;version=1 1A 102200 102600 2 125 400 0.3125
    Need to count how many reads were aligned against the gene
'''
def count_features(bedfile, outfile):
    in_file = open(bedfile)
    out_file = open(outfile,'w')

    dict_gene_count = {}
    dict_gene_coveragerange = {}
    dict_gene_basecovered = {}	
	
    for line in in_file:
        parts = line.split('\t')
        if len(parts) < 11:
            continue
        gene_entry = parts[3]
        read_count = int(parts[7])
	basecovered = int(parts[8])
	coveragerange = int(parts[9])

        if gene_entry in dict_gene_count:
            new_entry = dict_gene_count[gene_entry] + read_count
            dict_gene_count[gene_entry] = new_entry
	    
            new_cov = dict_gene_coveragerange[gene_entry] + coveragerange
            dict_gene_coveragerange[gene_entry] = new_cov
	    
            new_base = dict_gene_basecovered[gene_entry] + basecovered
            dict_gene_basecovered[gene_entry] = new_base
           
        else:
            dict_gene_count[gene_entry] = read_count
            dict_gene_coveragerange[gene_entry] = coveragerange
            dict_gene_basecovered[gene_entry] = basecovered

    in_file.close()

    all_keys = dict_gene_count.keys()
    for key in all_keys:
        out_file.write(key + '\t' + str(dict_gene_count[key]) + '\t' + str(dict_gene_basecovered[key]) + '\t' + str(dict_gene_coveragerange[key]) + '\n')
        
    out_file.close()

if __name__=="__main__":
    bedfile = '/pub9/ritesh/wheat_renseq/Analysis/analysis_CS/analysis_pbcs/intersect_gene_coverage.bed'
    outfile = '/pub9/ritesh/wheat_renseq/Analysis/analysis_CS/analysis_pbcs/intersect_gene_coverage.count'
    count_features(bedfile, outfile)

