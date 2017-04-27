import sys
import math
import re
import os

def parse(fname):
    for l in open(fname):
        yield str(l) 

def unwanted(fname, platform):
    unwantedGSM = []
    data = parse(fname)
    for line in data:
        if '^SAMPLE' in line:
            GSM = line.replace('^SAMPLE = ','')
            GSM = GSM.strip('\n')
            while not '!Sample_platform_id' in line:
                line = data.next()
            GPL = line.replace('!Sample_platform_id = ','')
            GPL = GPL.strip('\n')
            if not platform in GPL:
                unwantedGSM.append(GSM)
    return unwantedGSM

def goThrough(GPL):
    fNames = []
    softFiles = []
    allUnwanted = []
    rootDir = os.getcwd()
    rootDir = rootDir + '/soft/' + GPL
    for files in os.walk(rootDir):
        softFiles = files[2]
    for fName in softFiles:
        if 'soft' in fName:
            dFile = rootDir + '/' + fName
            fNames.append(dFile)
    for f in fNames:
        li = unwanted(f, GPL)
        for l in li:
            allUnwanted.append(l)
    return allUnwanted

print '\n'.join(goThrough(sys.argv[1]))
