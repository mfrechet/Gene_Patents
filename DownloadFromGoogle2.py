'''
Created on Jun 13, 2011

This script retrieves the nucleotide sequences in the claims of patents in the Google Patents USPTO Bulk Downloads: Patent Grant Full Text database.  These are limited to patents added in the year 2000 and later.

@author: melissafrechette
'''
from urllib import urlopen
from BeautifulSoup import BeautifulSoup, SoupStrainer
import zipfile
import tarfile
from StringIO import StringIO
import re
import subprocess

#The page listing all of the patent files
address ='http://www.google.com/googlebooks/uspto-patents-grants-text.html'

page = urlopen(address)
toParse = BeautifulSoup(page)

refs = []

# Find the sections containing the links to all of the files to download
start = toParse.find(name='h3', attrs={"id" : "2000"})
siblings = start.findPreviousSiblings('a')

#Make a list of the links
for ahref in siblings:
    refs.append(str(ahref['href']))
    print "appended one"

# Create a new file for the patents, overwriting any file that might have been there.
sequences = open('/m/canvas1/mfrechet/GoogleSequences.txt', 'w')
sequences.write("")
sequences.close()

# Extract the sequence from the patents and write them to GoogleSequences.fsa
subprocess.call(['sh GoogleSequenceExtractor.sh ipg110104.xml >>GoogleSequences.fsa'], shell=True)
        
print "done"
    
