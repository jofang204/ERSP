
# ERSP SAHOO
# updated 02.27.17
# Description: Take in a soft file and writes the expr, idx, ih, survival files

import sys
import re

def parse(fname):
    for l in open(fname):
        yield str(l)              

data = parse('./GSE9576_family.soft')

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

    #find GSE id
    elif "!Sample_series_id" in line:
        series_id = line.replace("!Sample_series_id = ", "")
        series_id = series_id.strip("\n")
        survival_info["series"].append(series_id)
    
    # finds clinical header
    elif '!Sample_title' in line:
        c_header = line.strip('!Sample_title = ')
        c_header = c_header.strip('\n')
        clinical_header.append(c_header)
        continue

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
        temp_values.append(list[1])

        # keep track of correct order of probe ids that appear in soft file
        if GSM_id_order == True:
            id_order.append(list[0])

    #get the channel index
    if "!Sample_channel_count" in line:

        temp = line.strip("!Sample_channel_count = ")
        channel_num = temp.strip("\n")
        channel = "_ch"+channel_num
    
        #lines after are with _ch#
        while True:
            l = data.next()
            
            #break out when line does not contain _ch#
            if not channel in l:
                header_added = True
                break
            
            #get the header/key
            l = l.split(" = ")
            titles = l[0].replace("!Sample_","")
            titles = titles.replace(channel, "")
            title = titles.replace("_", " ")
            
            #if : exists in the second part, the substring before : is header
            #and after is the value
            if ":" in l[1]:
                titles = l[1].split(": ")
                title = titles[0]
                l[1] = titles[1]
            
            #if header has not been added, add to dictionary, check its type (char or number)
            #and append to the prefix list
            if header_added == False:
                try:
                    n = int(l[1])
                    survival_header_pre.append("n ")
                except ValueError:
                    survival_header_pre.append("c ")
                survival_header_list.append(title)
                survival_info[title] = [l[1].strip("\n")]
            else:
                #append if key already defined
                survival_info[title].append(l[1].strip("\n"))

# opens files for writing 
expr_file = open("GSE9576-expr.txt", 'w+') 
idx_file = open("GSE9576-idx.txt", 'w')
survival = open("GSE9576-survival.txt", "w")
ih_file = open("GSE9576-ih.txt", 'w')

#### EXPR, IH, and IDX WRITING ####
# writes header to expression file
expr_header = "ProbeID" + '\t' + 'Name' + '\t' + '\t'.join([str(i) for i in sampleID])
expr_file.write(expr_header)
expr_file.write('\n')

# writes header to idx file
idx_header = "ProbeID" + '\t' + 'Ptr' + '\t' + "Name" + '\t' + "Description" + '\n'
idx_file.write(idx_header)


# write to expr and idx file
for i in xrange(len(id_order)):
    
    name = id_order[i]
    
    # write idx file, record file pointer
    idx_file.write('\t'.join([name, str(expr_file.tell()), gene_description[name].split(":")[0], gene_description[name].split(":")[1]]))

    # write probe id and description to expression file
    expr_file.write('\t'.join([name, gene_description[name]]))

    # writes each expr value from each GSM
    for element in sampleID.items():
        values = element[1]
        expr_file.write('\t')
        expr_file.write(str(values[i]))

    expr_file.write('\n')
    idx_file.write('\n')

expr_file.close()
idx_file.close()

## IH WRITING ##
ih_header = "ArrayID" + '\t' + "ArrayHeader" + '\t' + "ClinicalHeader"
ih_file.write(ih_header)
ih_file.write('\n')

# write ih file 
counter = 0
for element in GSM_order:
    ih_file.write('\t'.join([element, array_header[counter], clinical_header[counter]]))
    ih_file.write('\n')
    counter += 1

ih_file.close()

### SURVIVAL WRITING ###
i = 0
length = len(survival_header_list)
survival_header = ""

#write header
for i in range(length):
    #no tab after the last header
    if i == length-1:
        survival_header = survival_header + survival_header_pre[i] + survival_header_list[i]
    else:
        survival_header = survival_header + survival_header_pre[i] + survival_header_list[i] + "\t"
survival_header = survival_header + "\n"
survival.write(survival_header)

#write body
i = 0
length = len(survival_info["ArrayId"])
for i in range(length):
    #a line
    aTuple = []
    for t in survival_header_list:
        #if no value is added to the column, append empty string
        if len(survival_info[t]) == 0:
            aTuple.append("")
        #else append to dictionary
        else:
            aTuple.append(survival_info[t][i])
    #write a line
    survival.write("\t".join([str(s) for s in aTuple]))
    survival.write("\n")
    
survival.close() 

