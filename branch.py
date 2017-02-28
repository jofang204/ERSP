# ERSP SAHOO
# updated 02.21.17
# Description: Take in a soft file and writes the expression file

import sys
import re

def parse(fname):
    for l in open(fname):
        yield str(l)               

data = parse('./GSE9576_family.soft')

#array for all the IDs
array_ids = []

#array for all the headers
arrayheader = []

#array for all the clinical headers
clinicalhheader = []

for line in data:
    if '^SAMPLE' in line:
        array_id = line.strip('^SAMPLE = ')
        array_id = array_id.strip('\n')
        array_ids.append(array_id)
        arrayheader.append(array_id)
    if '!Sample_title' in line:
    	cheader = line.strip('!Sample_title = ')
        cheader = cheader.strip('\n')
        clinicalhheader.append(cheader)
    	continue


ih_file = open("ih.txt", "w")
ih_header = "ArrayID" + '\t' + "ArrayHeader" + '\t' + "ClinicalhHeader" 
ih_file.write(ih_header)
ih_file.write('\n')

for i in xrange(len(array_ids)):

    # write probe id and description
    ih_file.write('\t'.join([str(array_ids[i]), str(arrayheader[i]), str(clinicalhheader[i])]))
    
    ih_file.write('\n')

ih_file.close()