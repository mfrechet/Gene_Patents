#Eliminates duplicate sequences, and add each original sequence to the set seqs

import sys

seqs = set()
start = 0
end = 500

#Go through each file in the Sequences folder
while True:
    try:
        fh = open('/m/canvas1/mfrechet/Sequences/sequence_'+str(start)+'_through_'+str(end)+'.txt')
    except:
        for seq in seqs:
            print seq
        sys.exit(0)

    add = False
    seq = ''

    for line in fh:
        if line.startswith('>'):
            #If the seqeuence is not already in the set, add it
            if seq not in seqs and seq:
               #If it is a US sequence
               if 'US' in oldline: 
                   seqs.add(seq)
                   print seq
                   seq = ""
            oldline = line
        else:
            seq = seq + line
    seqs.add(seq)

    start = end
    end = end + 500
