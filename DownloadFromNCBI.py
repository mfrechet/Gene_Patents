#*** Code for downloading proteitn sequences from the NCBI database ***
from BeautifulSoup import BeautifulSoup
import urllib
import urllib2

print "Starting..."

address = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=nucleotide&term=srcdb+genbank[prop]+"gbdiv pat"[Properties]'
page= urllib.urlopen(address).read()
toParse = BeautifulSoup(page)

total = int(toParse.contents[4].contents[0].contents[0])

print str(total) + " sequences"

retMax = 500

# Get the results in batches of 50
for retStart in xrange(0, total, retMax):

    print str(retStart) + " out of " + str(total)

    page = urllib.urlopen(address + "&retstart="+str(retStart)+"&retmax="+str(retMax))
    toParse = BeautifulSoup(page)
    
    # Every other result is a blank line.  THe if statement skips the blank lines.
    skip = True
    ids=""
    #find the sequences
    for index in xrange(len(toParse.contents[4].contents[3])):
        if skip == False:
            ids =ids + str(toParse.contents[4].contents[3].contents[index].contents[0])
            ids = ids +","
            skip = True
        else:
            skip = False
            
    sequence = urllib.urlopen("http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=nucleotide&id="+str(ids)+"s&rettype=fasta")
    logfile = open('/home/mfrechet/Sequences/sequence_' + str(retStart) +"_through_"+ str(retStart+index/2) + '.txt', 'w')
    logfile.write(sequence.read())
    logfile.close()
    
print "done"
