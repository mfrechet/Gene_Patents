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



<<<<<<< HEAD
file = gzip.GzipFile(fileobj=StringIO(zippedFile.read()))
=======
file = gzip.GzipFile(fileobj=zippedFile.read())
>>>>>>> 0ccbda6bca0f19eec3d40a6588bf23b020cf183f

#file = gzip.open("/Users/melissafrechette/Downloads/nt-inClaims.fsa.gz", "rb")
print("opened")

<<<<<<< HEAD
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

=======
output = open("/m/canvas1/mfrechet/nt-inClaims.fsa", 'w')
output.write(str(file.read()))
>>>>>>> 0ccbda6bca0f19eec3d40a6588bf23b020cf183f
output.close()

print("finished")
    
