#*** Code for downloading proteitn sequences from the NCBI database ***
from BeautifulSoup import BeautifulSoup
from urllib import urlencode
from urllib2 import urlopen
import sys

print "Starting..."

# the base address
base = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?'

# the query
q = {
'db': 'nucleotide',
'term': 'srcdb+genbank[prop]+"gbdiv pat"[Properties]'
}


address = base + urlencode(q)

print 'ADDRESS:', address

i = 0

#Use beutifulSoup to retrieve the total number of entries
while True:

    #in case of error on the other end
    try:
        page= urlopen(address).read()
    except:
        if i < 200:
            i = i+1
        else:
            sys.exit( "Page failed to open on the initial open after 200 tries.  Try running again later.")
    else:
        break
    
toParse = BeautifulSoup(page)
total = int(toParse.contents[4].contents[0].contents[0])

print total, "sequences"


retMax = 500

# Get the results in batches of retMax
for retStart in xrange(0, total, retMax):

    print str(retStart) + " out of " + str(total)
    i = 0
    
    while True:

        try:
            page = urlopen(address + "&retstart="+str(retStart)+"&retmax="+str(retMax))
        except:

            if i < 200:
                i = i+1
            else:
                sys.exit("Failed to open the page to retrieve the sequence ids after 200 tries")

        else:
            break

    toParse = BeautifulSoup(page)
    
    # Every other result is a blank line.  The if statement skips the blank lines.
    skip = True
    ids=""
    #find the sequences
    try:
        for index in xrange(len(toParse.contents[4].contents[3])):
            if not skip:
                ids = ids + str(toParse.contents[4].contents[3].contents[index].contents[0])
                ids = ids +","
                skip = True
            else:
                skip = False

    except:
        toParse.prettify()
            

    i = 0

    #Write the sequences to file in batches of 500
    while True:

        try:
            sequence = urlopen("http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucleotide&id="+str(ids)+"s&rettype=fasta")
        except:
            if i < 200:
                i = i + 1
            else:
                sys.exit('Failed to retrieve the sequence after 200 tries.')
        else:
            break
        
    logfile = open('/m/canvas1/mfrechet/Sequences/sequence_' + str(retStart) +"_through_"+ str(retStart+index/2) + '.txt', 'w')
    logfile.write(sequence.read())
    logfile.close()
    
print "done"
