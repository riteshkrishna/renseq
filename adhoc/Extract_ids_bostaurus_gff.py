__author__ = 'ritesh'
import re

'''
    AC_000158.1     Gnomon  mRNA    122904  180159  .       -       .
    ID=rna1;Parent=gene3;Dbxref=GeneID:507243,Genbank:XM_002684585.5,BGD:BT17749;
    Name=XM_002684585.5;gbkey=mRNA;gene=CLIC6;model_evidence=Supporting evidence
    includes similarity to: 15 ESTs%2C 12 Proteins%2C and 100%25 coverage of the
    annotated genomic feature by RNAseq alignments%2C including 38 samples with
    support for all annotated introns;product=chloride intracellular channel 6;
    transcript_id=XM_002684585.5

'''

def parse_gff_bos_taurus(gff_file, map_file):
    gff_in = open(gff_file)
    map_out = open(map_file,'w')

    for line in gff_in:
        if line.startswith('#'):
            continue

        #parts = re.split(r'\t+', line)
        parts = line.split()

        if len(parts) < int(9):
            continue

        if 'mRNA' in parts[2]:
            attrbs = parts[8].split(';')
            for attr in attrbs:
                if 'ID=' in attr:
                    (symb, rna) = attr.split('=')
                if 'Dbxref=' in attr:
                    #(key, value) = attr.split(':')

                    map_out.write(rna + '\t' + attr + '\n')

    gff_in.close()
    map_out.close()

if __name__ == "__main__":

    gff_input = "../Temp/temp.gff"
    map_output = "../Temp/map.txt"
    parse_gff_bos_taurus(gff_input,map_output)



