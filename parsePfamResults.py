# Copied from window machine RK_Utility project folder, modify for unix when needed
# Script to parse pfam results obtained via email on the strand specific translated dna sequences produced via the assembly

__author__ = 'riteshk'

def parsePfam(pfam_file, processed_output):
    fin = open(pfam_file)
    fout = open(processed_output,'w')

    part_lengths = set()
    contig_names = {}

    for line in fin:
        if line.startswith('#'):
            continue
        if line in ['\n', '\r\n']:
            continue
        parts = line.split()
        part_lengths.add(len(parts))

        if len(parts) >=13 :
            name = parts[0]

            if len(parts) == 15:
                domain = parts[6]
                score = float(parts[12])
            elif len(parts) == 16:
                domain = parts[7]
                score = float(parts[13])

            if score < 0.0001:
                name_frame = name.split('_') # remove _ from the contig name
                name_only = name_frame[0]
                if name_only in contig_names:
                    domain_list = contig_names[name_only]
                    domain_list.add(domain)
                    contig_names[name_only] = domain_list
                else:
                    domain_list = {domain} # values as set, rather than list
                    contig_names[name_only] = domain_list

            out_line = name + '\t' + domain + '\t' + str(score) + '\n'
            #print (out_line)

    print(part_lengths)
    print(contig_names)
    fin.close()

    for k,v in contig_names.items():
        fout.write(k + "\t" + str(list(v)) + "\n")

    fout.close()

if __name__ == "__main__":
    pfam_file = "C:\Ritesh_Work\wheat\out_61_blastn_allpfam.txt"
    parsed_out_file = "C:\Ritesh_Work\wheat\out_61_blastn_allpfam_processed.txt"
    parsePfam(pfam_file,parsed_out_file)

