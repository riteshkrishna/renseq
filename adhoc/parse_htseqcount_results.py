__author__ = 'ritesh'

import re

'''
    This file is for Ben's data and by mistake is present in this project.

    I have prepared a consolidated file containing outputs of Htseq-count for a number of bam files. The results
    are separeted by blocks starting with "BEGIN file_name" and ending with an "END". This program will parse the
    file and arrange the results in the format required by Ben's experiment.

'''

def prepare_output_files(htseq_file):
    '''
    Example file name - 10-227_T8_140313_L006_R1.fastq.gz where 227 is animal-id, T8 is one of the three time points
    (T4, T8 and T52). Each file has two pairs, identfied by L006, L002 etc...
    '''

    # Aminal and time-period identifiers are arranged here
    t4_list = ('217_T4', '236_T4','239_T4', '226_T4', '222_T4','240_T4','227_T4', '231_T4', '238_T4')
    t8_list = ('217_T8','236_T8','239_T8','226_T8','222_T8','240_T8','227_T8','231_T8','238_T8')
    t52_list = ('228_T52', '236_T52', '239_T52','226_T52','222_T52','205_T52')

    pattern = "2[0-9][0-9]_T[485]+"

    t4_file = open('../Temp/T4_counts.txt','w')
    t8_file = open('../Temp/T8_counts.txt','w')
    t52_file = open('../Temp/T52_counts.txt','w')

    headers = {t4_file: True, t8_file:True, t52_file:True}

    count_file = open(htseq_file)

    file_to_write_to = ''
    read_block = ''
    key_time_l_pair_id = ''

    for line in count_file:
        if line.startswith('BEGIN'):

            file_identifier = line.split(' ')
            file_name = file_identifier[1].rstrip()
            name_parts = file_name.split('-')
            if name_parts[0] == file_name: # If the name is not like 8-226_T8_140328_L002_R1 but 8_226_T8_140328_L002_R1
                name_parts = file_name.split('_')
                animal_id = name_parts[1]
                time_id =  name_parts[2]
                date_id = name_parts[3]
                l_id = name_parts[4]
                pair_id = name_parts[5]
            else:
                ids = name_parts[1].split('_')
                animal_id = ids[0]
                time_id = ids[1]
                date_id = ids[2]
                l_id = ids[3]
                pair_id = ids[4]

            key_pair = animal_id + '_' + time_id
            key_time_l_pair_id = key_pair + '_' + l_id + '_' + pair_id

            if key_pair in t4_list:
                file_to_write_to = t4_file
            elif key_pair in t8_list:
                file_to_write_to = t8_file
            elif key_pair in t52_list:
                file_to_write_to = t52_file
            else:
                print ('No file to write to for the key ' + key_pair)

        elif line.startswith('END'):
            # dump read_block in appropriate file
            process_readblock(read_block, file_to_write_to, headers, key_time_l_pair_id)
            file_to_write_to = ''
            read_block = ''
        else:
            read_block = read_block + line


    count_file.close()
    t4_file.close()
    t8_file.close()
    t52_file.close()

def process_readblock(read_block, file_identifier, headers, key_time_l_pair_id):
    # Need to arrange data in tune with 2-column and across file formats
    #print read_block

    lines = str.splitlines(read_block)
    dict_transcript = {}
    keys = []
    for line in lines:
        pairs = line.split('\t')
        keys.append(pairs[0])

    dict_transcript = dict.fromkeys(keys)


    for line in lines:
        pairs = line.split('\t')
        dict_transcript[pairs[0]] = pairs[1]

    #print (dict_transcript.keys())
    #print (len(dict_transcript))
    #print (dict_transcript.values())
    print ('Processing ...' + key_time_l_pair_id)

    # Sort the keys, so they remain in the same order across files
    allKeys = dict_transcript.keys()
    sorted_keys = sorted(allKeys)

    # Write header in the file, if not present already
    if headers[file_identifier] == True:
        file_identifier.write('File_id' + '\t')
        file_identifier.write('\t'.join(sorted_keys))
        file_identifier.write('\n')
        headers[file_identifier] = False

    # Write values
    file_identifier.write(key_time_l_pair_id + '\t')
    for key in sorted_keys:
        file_identifier.write(dict_transcript[key] + '\t')
    file_identifier.write('\n')


if __name__ == "__main__":

    # pattern = "-2[0-9][0-9]_T[485]+"
    # valid = re.compile(pattern)
    # print (valid.match("-227_T8_").string)
    # print (valid.match("-227_T6_").string)

    htseq_file = '/home/ritesh/PycharmProjects/renseq/Temp/bostaurus/htseq_count_allbams_bostaurus.txt'
    prepare_output_files(htseq_file)


