'''
This script retrives and saves patent files with both "SEQ ID" and "SEQUENCE LISTING" in their specifications from the USPTO database.

@author: melissafrechette
'''

from BeautifulSoup import BeautifulSoup
from urllib import urlopen
import sys
import re


baseAddress = 'http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=0&f=S&l=50&d=PTXT&OS=SPEC%2F"SEQUENCE+LISTING"+AND+SPEC%2F"SEQ+ID"&RS=SPEC%2F"SEQUENCE+LISTING"+AND+SPEC%2F"SEQ+ID"&Query=SPEC%2F"SEQUENCE+LISTING"+AND+SPEC%2F"SEQ+ID"&TD=39721&Srch1=("SEQUENCE+LISTING".BSUM.+or+"SEQUENCE+LISTING".DETD.+or+"SEQUENCE+LISTING".DRWD.)&Srch2=("SEQ+ID".BSUM.+or+"SEQ+ID".DETD.+or+"SEQ+ID".DRWD.)&Conj1=AND&NextList'

#The initial address to retrieve information from
address = baseAddress + '1' + '=Next+50+Hits'

i = 0

#Sometimes the page doesn't open correctly, keep trying
while True:

    print "tyring to open page"
    page = urlopen(address)

    toParse = BeautifulSoup(page)

    proceed = False

    # the part of the xml we want
    try:
        total = int((toParse.contents[0].contents[3].contents[8].contents[5].contents[0]))

        #page failed to open.  Try again
    except Exception:
        if i < 200:
            i = i + 1
        else:
            sys.exit("Initial page failed to open after 200 tries")
        

    #Page opened, move on out of this loop
    else:
        break

print total


list = []

# These regular expressions are used to retrieve the patent numbers from the xml results
pattern1 = re.compile('[0-9],[0-9][0-9][0-9],[0-9][0-9][0-9]</A></TD>')
pattern2= re.compile('[0-9],[0-9][0-9][0-9],[0-9][0-9][0-9]')

# retrieve patent addresses in increments of 50
for inc in xrange(1, int(total), 50):
    address = baseAddress + str(inc) + '=Next+50+Hits'
    i = 0

    # Try to open the page with the next set of 50.  GIve it 200 tries before giving up.
    while True:
        try:
            page = urlopen(address)
        except:
            if i < 200:
                i = i + 1
            else:
                sys.exit("List page failed to open after 200 tries")
        else:
            break
        
    print "set of 50"

    #Add the patent id number to the list of patent id number
    lines = re.findall(pattern1 ,page.read())
    ids = []
    for line in lines:
        ids.extend(re.findall(pattern2 ,line))
    list.extend(ids)
    print list
                
print "done fetching ids"

# open the url and retrieve the patent to save
for patent in list:
    i = 0
    while True:
        try:
            toSave = urlopen(' http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO1&Sect2=HITOFF&d=PALL&p=1&u=%2Fnetahtml%2FPTO%2Fsrchnum.htm&r=1&f=G&l=50&s1=7956242.PN.&OS=PN/7956242&RS=PN/' + str(patent))
        except:
            if i < 200:
                i = i + 1
            else:
                sys.exit("Patent failed to open after 200 tries")
        else:
            break

    #Save the patent
    logfile = open('/m/canvas1/mfrechet/PatentsToExtractFrom/'+str(patent)+'.txt', 'w')
    logfile.write(toSave.Read())
    logfile.close()

print "done"
