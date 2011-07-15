#Eliminates duplicate sequences, and add each original sequence to the set seqs

import sys

seqs = set()

try:
    fh = open('results.txt')
except:
    sys.exit("failed to open file")
    
oldline = none
add = False
seq = ''
for line in fh:
    if line.startswith('>'):
        #If the seqeuence is not already in the set, add it                 
        if seq not in seqs and seq:
            #If it is a US sequence                                          
            if 'US' in oldline:
                if oldline:
                    seqs.add(seq)
                    seq = ""
            oldline = line
    else:
        seq = seq + line
seqs.add(seq)

for seq in seqs:
    print seq
