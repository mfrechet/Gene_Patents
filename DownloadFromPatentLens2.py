'''
Created on Jun 8, 2011

Downloads a file containing the nucleotide sequences in the claims of USPTO Grants from PatentLens.

@author: melissafrechette
'''

from urllib2 import urlopen
import gzip

# Create a file and write the compressed file from the PatentLens to it.  This will overwrite any old file in that location.
zippedFile = open('/m/canvas1/mfrechet/PatentLensZippedFile.gz', 'w')
zippedFile.write(urlopen('http://www.patentlens.net/sequence/US_A/nt-inClaims.fsa.gz').read())
zippedFile.close()

# Create a file and unzip the previously downloaded file into it.  This will overwrite any old file in that location.
zippedFile = open('/m/canvas1/mfrechet/PatentLensZippedFile.gz')
file = open('/m/canvas1/mfrechet/PatentLensFile.fsa', 'w')
unzippedFile = gzip.GzipFile(zipfile, 'rb')
while True:
    line = unzippedFile.readline()
    if line == '':
        break
    file.write(line)
    print "Wrote: " + str(line)
zippedFile.close()

print("finished")
    
