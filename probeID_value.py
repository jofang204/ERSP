import re


def parse(fname):
    for l in open(fname):
        yield str(l)
        
data = parse('./GSE9576_family.soft')

inTable = False

# empty dictionary that maps sample to a list of expr values 
expr_vals = {}

# empty array
empty = [] 

# contains lists of valyes (an array of array)
info = [] 

# stores all values for a sample 
temp = []

sampleID = ''

for line in data:
	if '^SAMPLE' in line:
		sampleID = line.strip('^SAMPLE = ')
		expr_vals.update({sampleID : empty})

	elif '!sample_table_begin' in line:
		line = data.next()
		inTable = True
		#temp = []
		continue
	elif '!sample_table_end' in line:
		print temp
		print '\n'
		
		inTable = False
	
	if inTable == True:
		list = re.split(r'\t+', line.rstrip('\t'))
		temp.append (list[1])

	#if inTable == True: 
	#	if '!sample_table_end' in line:
			#info.append(temp)
			#print temp
	#		print "hi"
	#		print temp[0]
	#		expr_vals.update({sampleID : temp})
	#		inTable = False	
	#	else:
	#		list = re.split(r'\t+', line.rstrip('\t'))
	#		temp.append (list[1])
	#	continue

	#if '!sample_table_begin' in line:
	#	inTable = True
		# skip line
	#	line = data.next()
	#else:
	#	continue

#for i in expr_vals:
#	print i