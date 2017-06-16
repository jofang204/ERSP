
# ERSP SAHOO
# updated 02.27.17
# Description: Take in a soft file and writes the expr, idx, ih, survival files

import sys
import math
import re
import os

def parse(fname):
    for l in open(fname):
        yield str(l) 

data = parse(sys.argv[1])

descripFlag = False
sampleFlag = False
GSM_id_order = True
headerFlag = False 

gene_symbol_strings = ["Gene Symbol"]
gene_title_strings = ["Gene Title"]
symbol_index = 0
title_index = 0


# hashes the headers in order to get the gene title and gene symbol
header_strings = {}

# dictionaries that stores data
gene_description = {}   # probeid : "symbol: title"
sampleID = {}   # GSM numbers
fileptr = {}    # probeid: fileptr

# list probe_ids in a specific order
id_order = []

# order of GSM
GSM_order = []

# stores expr values for each sample
temp_values = []

# array for headers (ih file)
array_header = []

# array for clinical headers (ih file)
clinical_header = []

#list of headers of channel info/columns
survival_header_list = ["ArrayId", "time", "status", "series"]

#prefix/type of input of the column
survival_header_pre = ["", "", "", "c "]

#declare channel vairables
channel_num = ""
channel = ""

#whether keys has been added to the dictionary
header_added = False

#initialize survival info dictionary
survival_info = {}
survival_info["ArrayId"] = []
survival_info["time"] = []
survival_info["status"] = []
survival_info["series"] = []

# gets each probe id and its description 
for line in data:

    # gets gene descriptions indices
    if '!platform_table_begin\n' in line:
        line = data.next()
        
        # prepping to get gene decriptions
        # finds the column indices to get the gene title and gene symbol
        headers = line.split("\t")
        
        # hashes the headers -- each header is mapped to its index in the line
        for index in xrange(len(headers)):
            header_strings[headers[index]] = index

        # checks if any common symbol strings are in the header 
        for idx in xrange(len(gene_symbol_strings)):
            if header_strings.has_key(gene_symbol_strings[idx]):
                symbol_index = header_strings.get(gene_symbol_strings[idx])

        # checks if any common title strings are in the header
        for idx in xrange(len(gene_title_strings)):
            if header_strings.has_key(gene_title_strings[idx]):
                title_index = header_strings.get(gene_title_strings[idx])

        # if no symbol string can be found in header, prompt user to input index 
        # reprompts user until their input is an integer between the header range
        if symbol_index == 0:
            while True:
                try:
                    user_input = int(raw_input("Enter an index for gene symbol: "))
                except ValueError:
                    print("Please enter an integer!")
                    continue
                
                if user_input >= 0 and user_input <= len(headers):
                    symbol_index = user_input
                    break
                else:
                    print("Please enter an integer betwen 0 and " + str(len(headers)))
                    continue
        
        # if no title string can be found in header, prompt user to input index 
        # reprompts user until their input is an integer between the header range
        if title_index == 0:
            while True:
                try:
                    user_input = int(raw_input("Enter an index for gene title: "))
                except ValueError:
                    print("Please enter an integer!")
                    continue
                
                if user_input >= 0 and user_input <= len(headers):
                    title_index = user_input
                    break
                else:
                    print("Please enter an integer betwen 0 and " + str(len(headers)))
                    continue
        
        descripFlag = True
        headerFlag = True
        continue

    # done with gene description
    elif '!platform_table_end\n' in line:
        descripFlag = False
        continue

    # gets expression values for each probe idea in a sample
    elif '!sample_table_begin' in line:
        line = data.next()
        sampleFlag = True
        temp_values = [] # CLEAR IT!!
        continue
    elif '!sample_table_end' in line:
        sampleFlag = False
        GSM_id_order = False
        sampleID.update({id_string : temp_values})

    # gets sample id, initialize sampleID dict
    if '^SAMPLE' in line:
        id_string = line.strip('^SAMPLE = ')
        id_string = id_string.strip('\n')
        GSM_order.append(id_string)
        array_header.append(id_string)
        sampleID.update({id_string : []})
        fileptr[id_string] = []
        survival_info["ArrayId"].append(id_string)
        continue
            
    # grabs the probe id/gene's description
    if descripFlag == True:
        line = line.split('\t')
        probe_id = line[0]   # gets the probe id which is first column
        
        gene_symbol = line[symbol_index]
        gene_title = line[title_index]
        if gene_symbol == "":
            gene_symbol = "---"
        if gene_title == "":
            gene_title = "---"

        gene_description[probe_id] = gene_symbol + ": " + gene_title

    
    # grabs the expression value
    if sampleFlag == True:
        list = re.split(r'\t+', line.rstrip('\t'))
        temp_values.append(math.log(float(list[1]),2))

        # keep track of correct order of probe ids that appear in soft file
        if GSM_id_order == True:
            id_order.append(list[0])

# opens files for writing 
expr_file = open("./GPL570-expr.txt", "w+") 
idx_file = open("./GPL570-idx.txt", 'w')

#### EXPR, IH, and IDX WRITING ####

# writes header to idx file
idx_header = "ProbeID" + '\t' + 'Ptr' + '\t' + "Name" + '\t' + "Description" + '\n'
idx_file.write(idx_header)

# read and add gene id to normalized expr data
expr_orig = parse("./GPL570-norm.txt")
for l in expr_orig:
    l = l.rstrip("\n").split("\t")
    if '.txt' in l[0]: # header
        l[0] = "ProbeId"
        l.insert(1, "Name")
    else:
        pid = l[0]
        l.insert(1, gene_description[pid])
        # write idx file, record file pointer
        idx_file.write('\t'.join([pid, str(expr_file.tell()), gene_description[pid].split(":")[0], gene_description[pid].split(":")[1]]))
        idx_file.write('\n')
    expr_file.write('\t'.join(l))
    expr_file.write("\n")

expr_file.close()
idx_file.close()
