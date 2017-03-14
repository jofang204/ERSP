import sys
import re
import stepminer

def parse(fname):
    for l in open(fname):
        yield str(l)               

data = parse('./GSE9576-expr.txt')
thr_file = parse('./GSE9576-thr.txt')
info_file = open("GSE9576-info.txt","w")

next(data)

values = {}

header = ["AffyID", "name", "thr", "mean", "mean-thr", "perc", "min", "max", "sd", "thrNum", "hi", "int", "lo"]
info_file.write("\t".join([str(s) for s in header]))
info_file.write("\n")
# thr_file.write("\n")
idx = 0
for line in data:
	thr_line = next(thr_file).split('\t')

	arr = []

	line = line.split("\t")
	probeid = line[0]
	name = line[1].split(": ")[0]
	value_line = [float(s) for s in line[2:]]

	# values[probeid] = sorted([float(s) for s in value_line]);
	# fit_dict = stepminer.fitstep(values[probeid])
	#AffyID
	arr.append(probeid)
	#name
	arr.append(name)
	#thr
	thr = float(thr_line[1])
	arr.append(thr)
	#mean
	mean = stepminer.meanf(value_line)
	arr.append(mean)
	#mean-thr
	arr.append(mean - thr)
	#perc 
	# if (mean < thr):
	# 	#dividing number of values between threshold and mean by number of values below threshold
	# 	#it's negative because mean is below threshhold
	# 	perc = 0 - sum((i > mean) and (i < thr) for i in values[probeid])/(sum((i<thr) for i in values[probeid]))
	# if (mean > thr):
	# 	perc = sum((i > mean) and (i < thr) for i in values[probeid])/(sum((i<thr) for i in values[probeid]))

	# (# samples below threshold - # samples below mean) / total number of samples
	perc = (sum((i<thr) for i in value_line) - sum((i<mean) for i in value_line)) / len(value_line)

	arr.append(perc)
	#min
	arr.append(min(value_line))
	#max
	arr.append(max(value_line))
	#sd
	sd = stepminer.stdevf(value_line)
	arr.append(sd)
	#thrNum
	thrNum = sum(i > thr for i in value_line)
	arr.append(thrNum)
	#hi
	hi = sum(i > (thr + 0.5) for i in value_line)
	arr.append(hi)
	#int 
	intermediate = sum((i < (thr + 0.5)) and (i > (thr-0.5)) for i in value_line)
	arr.append(intermediate)
	#lo
	lo = sum(i < (thr - 0.5) for i in value_line)
	arr.append(lo)

	idx +=1
	info_file.write("\t".join([str(s) for s in arr]))
	info_file.write("\n")


info_file.close()