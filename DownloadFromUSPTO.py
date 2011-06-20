from BeautifulSoup import BeautifulSoup
from urllib import urlopen

baseAddress = 'http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=0&f=S&l=50&d=PTXT&OS=SPEC%2F"SEQUENCE+LISTING"+AND+SPEC%2F"SEQ+ID"&RS=SPEC%2F"SEQUENCE+LISTING"+AND+SPEC%2F"SEQ+ID"&Query=SPEC%2F"SEQUENCE+LISTING"+AND+SPEC%2F"SEQ+ID"&TD=39721&Srch1=("SEQUENCE+LISTING".BSUM.+or+"SEQUENCE+LISTING".DETD.+or+"SEQUENCE+LISTING".DRWD.)&Srch2=("SEQ+ID".BSUM.+or+"SEQ+ID".DETD.+or+"SEQ+ID".DRWD.)&Conj1=AND&NextList'

#The initial address to retrieve information from
address = baseAddress + '1' + '=Next+50+Hits'

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
        print "failed"

    #Page opened, move on out of this loop
    else:
        "suceeded"
        break

print total


list = []

# retrieve patent addresses in increments of 50
for inc in xrange(1, int(total), 50):
    address = baseAddress + str(inc) + '=Next+50+Hits'
    page = urlopen(address)
    toParse = BeautifulSoup(page)
    print "set of 50"

    #only lines 2-52 are actaully patents
    for patent in range (2,52):

        #make sure we aren't past the end
        if patent+inc-2 <= total:

            #add the end of the patent's url to the list of end of patent urls
            try:
                print "add to list"
                list.append((toParse.contents[0].contents[3].contents[9].contents[12].contents[patent].contents[2].contents[0].contents[0]))
                print str(patent+inc-2)
            except:
                print "blank line"

# open the url and retrieve the patent to save
for patent in list:
    "saving..."
    toSave = urlopen(' http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO1&Sect2=HITOFF&d=PALL&p=1&u=%2Fnetahtml%2FPTO%2Fsrchnum.htm&r=1&f=G&l=50&s1=7956242.PN.&OS=PN/7956242&RS=PN/' + str(patent))
    logfile = open('/m/canvas1/mfrechet/PatentsToExtractFrom')
    logfile.write(toSave.Read())
    logfile.close()

print "done"
