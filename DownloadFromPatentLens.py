'''
Created on Jun 8, 2011

@author: melissafrechette
'''

from urllib2 import urlopen
import gzip
import os
from StringIO import StringIO

zippedFile = urlopen('http://www.patentlens.net/sequence/US_A/nt-inClaims.fsa.gz')


print("got this far")



file = gzip.GzipFile(fileobj=StringIO(zippedFile.read()))

#file = gzip.open("/Users/melissafrechette/Downloads/nt-inClaims.fsa.gz", "rb")
print("opened")

print (file.read())

output = open("/m/canvas1/mfrechet/nt-inClaims.fsa", 'w')

seq =''

for line in file.readlines():

    if line.startswith('>'):

        #If the sequence is not already in the set add it
        if seq not in seqs and seq:
            seqs.add(seq)
            seq = ""
    else:
        seq = seq + line
seqs.add(seq)

for seq in seqs:
    output.write(seq)

output.close()

print("finished")
    
