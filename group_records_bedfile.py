__author__ = 'ritesh'

'''
    The program reads a sparse BED3 file and group the no-zero records together based on neighbourhood. Particularly
    used for renseq analysis where the data is analyzed in equal-sized bins, and only some bins are full. This procudes
    result in another BED3 file where neighbouring non-zero bins are merged and the rest remain the same.

    Example:
    1. 1D      3400    3600    1       117     200     0.5850000
    2. 1D      3600    3800    2       71      200     0.3550000
    3. 1D      3800    4000    1       62      200     0.3100000
    4. 1D      4000    4200    0       0       200     0.0000000
    5. 1D      4200    4400    14      153     200     0.7650000
    6. 1D      4400    4600    11      107     200     0.5350000
    7. 1D      4600    4800    1       60      200     0.3000000
    8. 1D      4800    5000    2       159     200     0.7950000

    Rows 1,2,3 will create a joint record that will look like -
    1D      3400    4000    1+2+1       117+71+62     200+200+200     (0.585+0.355+0.31)/3
    And similarly, rows 5,6,7 and 8 will create another joint entry.  Row 4 will continue to
    remain between the two joint records

'''
def process_bedfile(inputbed, outputbed):

    out_bed = open(outputbed,'w')
    in_bed = open(inputbed)

    group_id = ''
    group_start = 0
    group_end = 0
    group_readcount = 0
    group_basecount = 0
    group_length = 0
    group_precent = 0.0

    num_grouped_lines = 0

    # Read the first line
    line = in_bed.readline()

    while line:

        bed_fields = line.split('\t')
        if len(bed_fields) != 7:
            line = in_bed.readline()
            continue

        current_id = bed_fields[0]
        current_start = int(bed_fields[1])
        current_end = int(bed_fields[2])
        current_readcount = int(bed_fields[3])
        current_basecount = int(bed_fields[4])
        current_length = int(bed_fields[5])
        current_precent = float(bed_fields[6])

        if current_readcount == 0 and num_grouped_lines == 0: # No grouping happened

            out_bed.write(line)

        elif current_readcount == 0 and num_grouped_lines >= 1: # Grouping happened

            out_bed.write(group_id + '\t' + str(group_start) + '\t' + str(group_end) + '\t' + str(group_readcount) + '\t'
                          + str(group_basecount) + '\t' + str(group_length) + '\t' + str(group_precent) + '\n')
            out_bed.write(line)

            group_id = ''
            group_start = 0
            group_end = 0
            group_readcount = 0
            group_basecount = 0
            group_length = 0
            group_precent = 0.0
            num_grouped_lines = 0

        else:
            num_grouped_lines = num_grouped_lines + 1

            if num_grouped_lines == 1:
                group_id = current_id
                group_start = current_start
            else:
                if group_id !=  current_id: # In case there are two non-zero conc. records but with different identifiers
                    out_bed.write(group_id + '\t' + str(group_start) + '\t' + str(group_end) + '\t' + str(group_readcount) + '\t'
                          + str(group_basecount) + '\t' + str(group_length) + '\t' + str(group_precent) + '\n')
                    group_id = current_id
                    group_start = current_start
                    num_grouped_lines = 1

            group_end = current_end
            group_readcount = group_readcount + current_readcount
            group_basecount = group_basecount + current_basecount
            group_length = group_length + current_length
            group_precent = float(group_basecount) / float(group_length)

        line = in_bed.readline()


    in_bed.close
    out_bed.close()


if __name__=="__main__":
    input_bedfile = "/home/ritesh/PycharmProjects/renseq/Temp/test.bed"
    output_bedfile = "/home/ritesh/PycharmProjects/renseq/Temp/test_retouched.bed"
    process_bedfile(input_bedfile, output_bedfile)
