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

gene_title = "Gene Title"
gene_symbol = "Gene Symbol"
title_ind = 0
symbol = 0

# dictionary of probe id/gene's
# probe id/gene --> description
gene_description = {}

# empty dictionary that maps sample to a list of expr values 
sampleID = {}

# empty array
empty = [] 

# stores all values for a sample 
temp_id = []
temp = []

# stores file pointer
fileptr = {}

id_string = ''

# gets each probe id and its description 
for line in data:

    if '^SAMPLE' in line:
        id_string = line.strip('^SAMPLE = ')
        id_string = id_string.strip('\n')
        sampleID.update({id_string : empty})
        fileptr[id_string] = []
        continue

    # gets gene descriptions
    if '!platform_table_begin\n' in line:
        line = next(data).split('\t')
        title_ind = line.index(gene_title)
        symbol_ind = line.index(gene_symbol)
        descripFlag = True
        continue

    elif '!platform_table_end\n' in line:
        descripFlag = False
        continue

    # gets expression values for each probe idea in a sample
    elif '!sample_table_begin' in line:
        line = next(data)
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
        geneTitle = line2[title_ind]
        geneSymbol = line2[symbol_ind]

        if geneTitle == "":
            geneTitle = "---"
        if geneSymbol == "":
            geneSymbol = "---"

        gene_description[probeid] = geneSymbol + ": " + geneTitle
    
    # grabs the expression value
    if sampleFlag == True:
        list = re.split(r'\t+', line.rstrip('\t'))
        temp.append (list[1])
        if flag == True:
            temp_id.append(list[0])

# opens files for writing 
expr_file = open("GSE9576-expr.txt", 'w+') 
idx_file = open("GSE9576-idx.txt", 'w+') 

# writes header to expression file
expr_header = "ProbeID" + '\t' + 'Name' + '\t' + '\t'.join([str(i) for i in sampleID])
expr_file.write(expr_header)
expr_file.write('\n')

# writes header to idx file
idx_header = "ProbeID" + '\t' + 'Ptr' + '\t' + "Name" + '\t' + "Description" + '\n'
idx_file.write(idx_header)

print(sampleID["GSM242028"][:10])

i = 0
# write to files
for id in temp_id:
    
    # write idx file
    idx_file.write('\t'.join([id, str(expr_file.tell()), gene_description[id].split(": ")[0], gene_description[id].split(": ")[1]]))

    # write probe id and description to expression file
    expr_file.write('\t'.join([id, gene_description[id]]))
    
    # writes each expr value from each GSM
    for element in sampleID.items():
        values = element[1]
        expr_file.write('\t')
        expr_file.write(str(values[i]))

    expr_file.write('\n')
    idx_file.write('\n')

    i += 1

position = expr_file.seek(6735);
str = expr_file.readline()

print(str)
