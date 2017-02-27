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
    
    
    
    

    
    
    
    
    

#Write Survival file
data = parse('./GSE9576_family.soft')

#list of headers of channel info/columns
survivalHeaderList = ["ArrayId", "time", "status"]

#prefix/type of input of the column
survivalHeaderPre = ["", "", ""]

#declare channel vairables
channelNum = ""
channel = ""

#whether keys has been added to the dictionary
headerAdded = False

#the dictionary; contains all the info
survival_info = {}
survival_info["ArrayId"] = []
survival_info["time"] = []
survival_info["status"] = []

#declare as empty
sampleID = ""
for line in data:
    
    #add GSM to ArrayId
    if "^SAMPLE" in line:
        GSM = line.split(" = ")
        if GSM[1] != sampleID:
            sampleID = GSM[1]
            survival_info["ArrayId"].append(GSM[1].strip("\n"))
            
    #get the channel index
    if "!Sample_channel_count" in line:
        temp = line.strip("!Sample_channel_count = ")
        channelNum = temp.strip("\n")
        channel = "_ch"+channelNum
        
        #lines after are with _ch#
        while True:
            l = next(data)
            
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

survival = open("survival.txt", "w")
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
    
#close file
survival.close()

