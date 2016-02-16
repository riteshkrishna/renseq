__author__ = 'riteshk'

'''
    Takes a BED like file with blast hit co-ordinates and looks in a GFF if the blast hists are within the genic region
     or outside. Also if there are any nearby genes annotated. This is specifically for wheat so can be quite messy in
     terms of number of (non)annotations.

     Useful outputs can be - chromosome specific and contig-specific -
     blast hits within genic region -> blast_query - gene name +  blast-location
     non genic hits -> blast_query - nearest gene(if any, blank otherwise) + distance to nearest gene + blast-location

'''

def process_gff(gffFile,blastFile,scaf_gff_file, chr_outFile,nonchr_outFile):
    # relevant gff fields - chr, gene, st, end
    chromosomes = ['1A','1B','1D','2A','2B','2D',
                   '3A','3B','3D','4A','4B','4D',
                   '5A','5B','5D','6A','6B','6D',
                   '7A','7B','7D']

    geneListChrwise = [[] for i in range(21)]
    sorted_geneListChrwise = [[] for i in range(21)]

    gff_in = open(gffFile)
    nonchr_out = open(scaf_gff_file,'w') # All non-chromosome gene records go here

    # Read GFF and create data structures for chr-specific records. All non-chr genes go in nonchr_out file.
    for line in gff_in:
        if line.startswith("##"):
            continue

        parts = line.split('\t')
        if parts[0] in chromosomes:
            if parts[2] == 'gene':
                attFields = parts[8]
                geneField = attFields.split(';')
                geneID = geneField[0].split('gene:')
                gene_name = geneID[1]
                start = int(parts[3])
                end = int(parts[4])
                chr_index = chromosomes.index(parts[0])
                geneListChrwise[chr_index].append([gene_name,start,end])
        else:
            if parts[2] == 'gene':
                attFields = parts[8]
                geneField = attFields.split(';')
                geneID = geneField[0].split('gene:')
                gene_name = geneID[1]
                start = int(parts[3])
                end = int(parts[4])
                nonchr_out.write(parts[0] + "\t" + gene_name + "\t" + str(start) + "\t" + str(end) + "\n")

    #For each chromosome, sort the gene entries according to the start co-ord
    for chr in chromosomes:
        chr_index = chromosomes.index(chr)
        sorted_geneListChrwise[chr_index] = sorted(geneListChrwise[chr_index], key=lambda tup:tup[1])

    #for items in sorted_geneListChrwise:
    #    for genes in items:
    #        print (genes[0] + "\t" + str(genes[1]) + "\t" + str(genes[2]))
    #    print("\n\n")

    blast_in = open(blastFile)
    out_hits_chr = open(chr_outFile,'w')

    # Process blast file, only for chr blast hits
    for line in blast_in:
        parts = line.split("\t")
        query_id = parts[0]
        subject_id = parts[1]
        subject_start = int(parts[8])
        subject_end = int(parts[9])

        # Swap start and end if on -ve strand
        if subject_end < subject_start:
            temp = subject_end
            subject_end = subject_start
            subject_start = temp

        if subject_id in chromosomes:
            chr_index = chromosomes.index(subject_id)
            for i in range(len(sorted_geneListChrwise[chr_index])):
                if subject_start <= sorted_geneListChrwise[chr_index][i][2]:
                    i_start = sorted_geneListChrwise[chr_index][i][1]
                    i_end = sorted_geneListChrwise[chr_index][i][2]
                    if ((subject_start <= i_start) and (subject_end >= i_start)) or \
                        ((subject_start <= i_start) and (subject_end >= i_end)) or \
                        ((subject_start >= i_start) and (subject_start <= i_end)) or \
                        ((subject_start >= i_start) and (subject_end <= i_end)):
                        #print ("")
                        out_hits_chr.write("Overlapping \t" + query_id  + "\t" + subject_id  + "\t" + str(subject_start) + "\t" + str(subject_end) + "\t" + sorted_geneListChrwise[chr_index][i][0] + "\n")
                        break
                    else:
                        out_hits_chr.write("Non-Overlapping \t" + query_id  + "\t" + subject_id  + "\t" + str(subject_start) + "\t" + str(subject_end) + "\t" + sorted_geneListChrwise[chr_index][i-1][0] + "\t" + sorted_geneListChrwise[chr_index][i][0]+ "\n")
                        break
    blast_in.close()
    out_hits_chr.close()
    nonchr_out.close()
    gff_in.close()

    process_nonchr_blasthits(scaf_gff_file,blastFile, nonchr_outFile)

# Routine to process non-chr blast hits
def process_nonchr_blasthits(scaf_gff_file,blastFile, nonchr_outFile):

    scaf_in = open(scaf_gff_file)
    nonchr_out = open(nonchr_outFile,'w')

    nonchr_gene_list = []
    for line in scaf_in:
        parts = line.split("\t");
        if len(parts) == 4:
            nonchr_gene_list.append([parts[0],parts[1],int(parts[2]),int(parts[3])]) #chr, gene, start, end

    scaf_in.close()

    # Sort the records
    sorted_nonchr_gene_list = sorted(nonchr_gene_list, key=lambda tup:tup[0]) # Sort by name this time on chr
    sorted_scaf_names = [row[0] for row in sorted_nonchr_gene_list]

    chromosomes = ['1A','1B','1D','2A','2B','2D',
                   '3A','3B','3D','4A','4B','4D',
                   '5A','5B','5D','6A','6B','6D',
                   '7A','7B','7D']


    blast_in = open(blastFile)
    for line in blast_in:
        parts = line.split("\t")
        parts = line.split("\t")
        query_id = parts[0]
        subject_id = parts[1]
        subject_start = int(parts[8])
        subject_end = int(parts[9])

        # Swap start and end if on -ve strand
        if subject_end < subject_start:
            temp = subject_end
            subject_end = subject_start
            subject_start = temp

        if subject_id not in chromosomes: # Not a chromosome, so a scaffold
            if subject_id in sorted_scaf_names: # scaf present in GFF file
                total_genes = sorted_scaf_names.count(subject_id) # total genes list on that scaffold
                if total_genes == 1: # just output the gene name
                    index = sorted_scaf_names.index(subject_id)
                    gene_name = sorted_nonchr_gene_list[index][1]
                    i_start   = sorted_nonchr_gene_list[index][2]
                    i_end  = sorted_nonchr_gene_list[index][3]
                    if ((subject_start <= i_start) and (subject_end >= i_start)) or \
                        ((subject_start <= i_start) and (subject_end >= i_end)) or \
                        ((subject_start >= i_start) and (subject_start <= i_end)) or \
                        ((subject_start >= i_start) and (subject_end <= i_end)):
                        #print ("")
                        nonchr_out.write("Overlapping \t" + query_id  + "\t" + subject_id  + "\t" + str(subject_start) + "\t" + str(subject_end) + "\t" + gene_name + "\n")
                        #break
                    else:
                        nonchr_out.write("Non-Overlapping \t" + query_id  + "\t" + subject_id  + "\t" + str(subject_start) + "\t" + str(subject_end) + "\t" + gene_name + "\t" + gene_name + "\n")
                        #break
                else: # if more genes, then find the neighbour

                    this_scaf_records = []
                    first_index = sorted_scaf_names.index(subject_id)

                    for i in range(total_genes):
                        #scaf_name = sorted_nonchr_gene_list[first_index + i - 1][0]
                        gene_name = sorted_nonchr_gene_list[first_index + i - 1][1]
                        start   = sorted_nonchr_gene_list[first_index + i - 1][2]
                        end  = sorted_nonchr_gene_list[first_index + i - 1][3]
                        this_scaf_records.append([gene_name,start,end])

                    sorted_this_scaf_records = sorted(this_scaf_records, key=lambda tup:tup[1])

                    for i in range(len(sorted_this_scaf_records)):
                        if subject_start <= sorted_this_scaf_records[i][2]:
                            i_start = sorted_this_scaf_records[i][1]
                            i_end = sorted_this_scaf_records[i][2]
                            if ((subject_start <= i_start) and (subject_end >= i_start)) or \
                                ((subject_start <= i_start) and (subject_end >= i_end)) or \
                                ((subject_start >= i_start) and (subject_start <= i_end)) or \
                                ((subject_start >= i_start) and (subject_end <= i_end)):
                                #print ("")
                                nonchr_out.write("Overlapping \t" + query_id  + "\t" + subject_id  + "\t" + str(subject_start) + "\t" + str(subject_end) + "\t" + sorted_this_scaf_records[i][0] + "\n")
                                break
                            else:
                                nonchr_out.write("Non-Overlapping \t" + query_id  + "\t" + subject_id  + "\t" + str(subject_start) + "\t" + str(subject_end) + "\t" + sorted_this_scaf_records[i-1][0] + "\t" + sorted_this_scaf_records[i][0]+ "\n")
                                break

            else: # scaf not annotated and missing from GFF file
                nonchr_out.write("Unannotated \t" + query_id  + "\t" + subject_id  + "\t" +  str(subject_start) + "\t" + str(subject_end) + "\n")


    blast_in.close()
    nonchr_out.close()


if __name__ == "__main__":

    gffFile = '/Users/ritesh/Ritesh_iPlant/wheat_renseq/Triticum_aestivum.IWGSC1.0_popseq.27.gff3'
    blastFile = '/Users/ritesh/Ritesh_iPlant/wheat_renseq/out_61_blastn_hits_gt200_90p_eval05.txt'

    scaf_gffRecords = '/Users/ritesh/Ritesh_iPlant/wheat_renseq/scaf_gffRecords.txt'
    chr_outFile = '/Users/ritesh/Ritesh_iPlant/wheat_renseq/chr_geneneighbour.txt'
    nonchr_outFile = '/Users/ritesh/Ritesh_iPlant/wheat_renseq/nonchr_geneneighbour.txt'

    process_gff(gffFile,blastFile,scaf_gffRecords, chr_outFile,nonchr_outFile)
