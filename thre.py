import sys
import re
import stepminer

def parse(fname):
    for l in open(fname):
        yield str(l)               

data = parse('./GSE9576-expr.txt')
thr_file = open("GSE9576-thr.txt","w")

next(data)
values = {}

for line in data:
    line = line.split("\t")
    value_line = line[2:]
    probeid = line[0]
    values[probeid] = sorted([float(s) for s in value_line]);
    fit_dict = stepminer.fitstep(values[probeid])
    l = []
    l.append(probeid)
    l.append(fit_dict["threshold"])
    l.append(fit_dict["statistic"])
    l.append(fit_dict["threshold"]-0.5)
    l.append(fit_dict["threshold"]+0.5)
    thr_file.write("\t".join([str(s) for s in l]))
    thr_file.write("\n")

thr_file.close()