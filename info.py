import sys
import re
import stepminer

def parse(fname):
    for l in open(fname):
        yield str(l)               

data = parse('./GSE9576-expr.txt')
info_file = open("GSE9576-info.txt","w")

next(data)
arr = []
values = {}

header = ["AffyID", "name", "thr", "mean", "mean-thr", "perc", "min", "max", "sd", "thrNum", "hi", "int", "lo"]
info_file.write("\t".join([str(s) for s in header]))
# thr_file.write("\n")
for line in data:
    line = line.split("\t")
    probeid = line[0]
    name = line[1]
    value_line = line[2:]
    
    values[probeid] = sorted([float(s) for s in value_line]);
    fit_dict = stepminer.fitstep(values[probeid])
    #AffyID
    arr.append(probeid)
    #name
    arr.append(name)
    #thr
    thr = fit_dict["threshold"]
    arr.append(thr)
    #mean
    mean = stepminer.meanf(values[probeid])
    arr.append(mean)
    #mean-thr
    arr.append(mean - thr)
    #perc 
    if (mean < thr):
    	#dividing number of values between threshold and mean by number of values below threshold
    	#it's negative because mean is below threshhold
    	perc = 0 - sum((i > mean) and (i < thr) for i in values[probeid])/(sum((i<thr) for i in values[probeid]))
    if (mean > thr):
    	perc = sum((i > mean) and (i < thr) for i in values[probeid])/(sum((i<thr) for i in values[probeid]))
    arr.append(perc)
    #min
    arr.append(min(values[probeid]))
    #max
    arr.append(max(values[probeid]))
    #sd
    sd = stepminer.stdevf(values[probeid])
    arr.append(sd)
    #thrNum
    thrNum = sum(i > thr for i in values[probeid])
    arr.append(thrNum)
    #hi
    hi = sum(i > (thr + 0.5) for i in values[probeid])
    arr.append(hi)
    #int 
    intermediate = sum((i < (thr + 0.5)) and (i > (thr-0.5)) for i in values[probeid])
    arr.append(intermediate)
    #lo
    lo = sum(i < (thr - 0.5) for i in values[probeid])
    arr.append(lo)
    info_file.write("\t".join([str(s) for s in arr]))
    info_file.write("\n")

info_file.close()