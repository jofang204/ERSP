# ERSP SAHOO
# updated 02.21.17
# Description: Take in a soft file and writes the expression file

import sys
import re

def parse(fname):
    for l in open(fname):
        yield str(l)               

data = parse('./GSE9576_family.soft')

flag = 1
descripFlag = False
sampleFlag = False

# dictionary of probe id/gene's
# probe id/gene --> description
gene_description = {}

# empty dictionary that maps sample to a list of expr values 
sampleID = {}

# empty array
empty = [] 

# contains lists of valyes (an array of array)
#info = [] 

# stores all values for a sample 
temp_id = []
temp = []

id_string = ''

# gets each probe id and its description 
for line in data:

    if '^SAMPLE' in line:
        id_string = line.strip('^SAMPLE = ')
        id_string = id_string.strip('\n')
        sampleID.update({id_string : empty})
        continue

    # gets gene descriptions
    if '!platform_table_begin\n' in line:
        line = data.next()
        descripFlag = True
        continue
    elif '!platform_table_end\n' in line:
        descripFlag = False
        continue

    # gets expression values for each probe idea in a sample
    elif '!sample_table_begin' in line:
        line = data.next()
        sampleFlag = True
        temp = [] # CLEAR IT!!
        continue
    elif '!sample_table_end' in line:
        sampleFlag = False
        flag = False
        sampleID.update({id_string : temp})
            
    # grabs the probe id/gene's description
    if descripFlag == True:
        line2 = line.split("\t")
        probeid = line2[0]
        geneTitle = line2[9]
        geneSymbol = line2[10]
        gene_description[probeid] = geneSymbol + ": " + geneTitle

        # leaves description blank if there isn't one
        if gene_description[probeid] == ": ":
            gene_description[probeid] = " "
    
    # grabs the expression value
    if sampleFlag == True:
        list = re.split(r'\t+', line.rstrip('\t'))
        temp.append (list[1])
        if flag == True:
            temp_id.append(list[0])

# opens file for writing 
toWrite = open("test.txt", 'w') # specify the output file

# writes header to output file
header = "ProbeID" + '\t' + 'Name' + '\t' + '\t'.join([str(i) for i in sampleID])
toWrite.write(header)
toWrite.write('\n')

for i in range(0,len(temp_id)):

    # write probe id and description
    toWrite.write('\t'.join([temp_id[i], gene_description[temp_id[i]]]))
    
    # writes each expr value from each GSM
    for element in sampleID.items():
        values = element[1]
        toWrite.write('\t')
        toWrite.write(str(values[i]))     

    toWrite.write('\n')
