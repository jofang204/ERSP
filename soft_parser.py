# ERSP SAHOO
# updated 02.21.17
# Description: Take in a soft file and writes the expression file

import sys
import re

def parse(fname):
    for l in open(fname):
        yield str(l)              

data = parse('./GSE9576_family.soft')

descripFlag = False
sampleFlag = False

gene_title = "Gene Title"
gene_symbol = "Gene Symbol"
title_ind = 0
symbol = 0

# dictionaries that stores data
gene_description = {}   # probeid : "symbol: title"
sampleID = {}   # sampleid: [values]
fileptr = {}    # probeid: fileptr

# probe ids
probe_id = []

# stroes expr values for each sample
temp_values = []

#list of headers of channel info/columns
survivalHeaderList = ["ArrayId", "time", "status", "series"]

#prefix/type of input of the column
survivalHeaderPre = ["", "", "", "c "]

#declare channel vairables
channelNum = ""
channel = ""

#whether keys has been added to the dictionary
headerAdded = False

#initialize survival info dictionary
survival_info = {}
survival_info["ArrayId"] = []
survival_info["time"] = []
survival_info["status"] = []
survival_info["series"] = []

# gets each probe id and its description 
for line in data:

    # gets sample id, initialize sampleID dict
    if '^SAMPLE' in line:
        id_string = line.strip('^SAMPLE = ')
        id_string = id_string.strip('\n')
        sampleID.update({id_string : []})
        fileptr[id_string] = []
        survival_info["ArrayId"].append(id_string)
        continue

    #get the channel index
    if "!Sample_channel_count" in line:

        temp = line.strip("!Sample_channel_count = ")
        channelNum = temp.strip("\n")
        channel = "_ch"+channelNum
    
        #lines after are with _ch#
        while True:
            l = data.next()
            
            #break out when line does not contain _ch#
            if not channel in l:
                headerAdded = True
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
            if headerAdded == False:
                try:
                    n = int(l[1])
                    survivalHeaderPre.append("n ")
                except ValueError:
                    survivalHeaderPre.append("c ")
                survivalHeaderList.append(title)
                survival_info[title] = [l[1].strip("\n")]
            else:
                #append if key already defined
                survival_info[title].append(l[1].strip("\n"))

    # gets gene descriptions indices
    if '!platform_table_begin\n' in line:
        line = data.next().split('\t')
        title_ind = line.index(gene_title)
        symbol_ind = line.index(gene_symbol)
        descripFlag = True
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
        sampleID.update({id_string : temp_values})

        #find GSE id
    elif "!Sample_series_id" in line:
        series_id = line.replace("!Sample_series_id = ", "")
        series_id = series_id.strip("\n")
        survival_info["series"].append(series_id)
            
    # grabs the probe id/gene's description
    if descripFlag == True:
        line2 = line.split("\t")
        probeid = line2[0]
        probe_id.append(probeid)
        geneTitle = line2[title_ind]
        geneSymbol = line2[symbol_ind]

        #set name or descirption to --- if there is none
        if geneTitle == "":
            geneTitle = "---"
        if geneSymbol == "":
            geneSymbol = "---"

        gene_description[probeid] = geneSymbol + ": " + geneTitle
    
    # grabs the expression value
    if sampleFlag == True:
        list = re.split(r'\t+', line.rstrip('\t'))
        temp_values.append (list[1])

# opens files for writing 
expr_file = open("GSE9576-expr.txt", 'w+') 
idx_file = open("GSE9576-idx.txt", 'w')
survival = open("GSE9576-survival.txt", "w")

### SURVIVAL WRITING ###
i = 0
length = len(survivalHeaderList)
survivalHeader = ""

#write header
for i in range(length):
    #no tab after the last header
    if i == length-1:
        survivalHeader = survivalHeader + survivalHeaderPre[i] + survivalHeaderList[i]
    else:
        survivalHeader = survivalHeader + survivalHeaderPre[i] + survivalHeaderList[i] + "\t"
survivalHeader = survivalHeader + "\n"
survival.write(survivalHeader)

#write body
i = 0
length = len(survival_info["ArrayId"])
for i in range(length):
    #a line
    aTuple = []
    for t in survivalHeaderList:
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

#### EXPR and IDX WRITING ####
# writes header to expression file
expr_header = "ProbeID" + '\t' + 'Name' + '\t' + '\t'.join([str(i) for i in sampleID])
expr_file.write(expr_header)
expr_file.write('\n')

# writes header to idx file
idx_header = "ProbeID" + '\t' + 'Ptr' + '\t' + "Name" + '\t' + "Description" + '\n'
idx_file.write(idx_header)

i = 0
# write to idx and expr file
for id in probe_id:
    
    # write idx file, record file pointer
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

idx_file.close()
expr_file.close()