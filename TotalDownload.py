'''
Created on Jun 8, 2011

Downloads the sequences/patents from five different sources: PatentLens, NCBI, the Google USPTO patent full-text database, the PSIPS bulk listing, and the USPTO full-text database. 

@author: melissafrechette
'''

from urllib import urlencode
from urllib2 import urlopen
import gzip, subprocess, sys, re, os
from StringIO import StringIO
from BeautifulSoup import BeautifulSoup
import zipfile26
import divideGoogleFile
from StringIO import StringIO

numsSet = set()
status = 0
space = re.compile('\s')

#Load in the file if there is one.
try:
    setDoc = open("/m/canvas1/mfrechet/patentNumbers.txt")
except:
    print "No previous document."
else:
    print "Loading status and patent numbers"
    status = None
    for line in setDoc.readLines():
        if status == None:
            status = space.sub('', str(line))
            print "Last run left off at: " + str(status)
        else:
            numsSet.add(space.sub('', str(line)))
    setDoc.close()

lensSet = set()

patNum = re.compile("[Uu][Ss]\s*([0-9][0-9]*)")
antiComma = re.compile(",")


#*** Code for reading and downloading sequences from PatentLens***

#If we ran a full time, or this is the first run
if int(status) == 0 or int(status) == 5:

    print "Starting PatentLens download"

    # Create a file and write the compressed file from PatentLens to it.  This will overwrite any old file in that location.
    zippedFile = open('/m/canvas1/mfrechet/PatentLensZippedFileTotal.gz', 'w')

    #Loop in case the page is down.  Ten tries seems like a good number.
    i = 0
    while True:
        try:
            zippedFile.write(urlopen('http://www.patentlens.net/sequence/US_B/nt-inClaims.fsa.gz').read())
        except:
            if i < 10:
                i = i + 1
            else:
                sys.exit("URL failed to open after ten tries.")
        else:
            break

    zippedFile.close()

    # Create a file and unzip the previously downloaded file into it.  This will overwrite any old file in that location.
    zippedFile = open('/m/canvas1/mfrechet/PatentLensZippedFileTotal.gz')
    file = open('/m/canvas1/mfrechet/PatentLensFileTotal.fsa', 'w')
    unzippedFile = gzip.GzipFile(fileobj=zippedFile)


    while True:
        line = unzippedFile.readline()

        #Look for patent numbers.
        num = patNum.search(line)
        if num is not None:
            #Check that it isn't aready there, this shouldn't be necessary, but is
            #here just in case.  Make sure to remove any commas.
            if antiComma.sub('', str(num.group(1))) not in numsSet:
                numsSet.add(antiComma.sub('', str(num.group(1))))
                lensSet.add(antiComma.sub('', str(num.group(1))))
        
        if line == '':
            break
        file.write(line)
    zippedFile.close()
    file.close()

    print "finished PatentLens Download"
    


#*** Code for downloading sequences from the NCBI database ***

#If we failed somewhere in this section last time or are going through routinely
if int(status) <= 1:
    print "Starting NCBI download"

    # the base address
    base = 'http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?'

    # the query
    q = {
    'db': 'nucleotide',
    'term': 'srcdb+genbank[prop]+"gbdiv pat"[Properties]'
    }

    address = base + urlencode(q)

    i = 0

    #Use BeautifulSoup to retrieve the total number of entries
    while True:

        #in case of error on the other end
        try:
            page= urlopen(address).read()
        except:
            if i < 200:
                i = i+1
            else:
                print "NCBI failed.  Writing status and sequences to file"
                setDoc = open("/m/canvas1/mfrechet/patentNumbers.txt")
                setDoc.write("1\n")
                for each in numsSet:
                    setDoc.write(each + "\n")
                setDoc.close()
                sys.exit( "Page failed to open on the initial open after 200 tries.  Try running again later.")
        else:
            break
    
    toParse = BeautifulSoup(page)
    total = int(toParse.contents[4].contents[0].contents[0])

    print total, "sequences"


    retMax = 500

    # Get the results in batches of retMax
    for retStart in xrange(0, total, retMax):

        i = 0
    
        while True:

            try:
                page = urlopen(address + "&retstart="+str(retStart)+"&retmax="+str(retMax))
            except:

                if i < 200:
                    i = i+1
                else:
                    print "NCBI failed.  Writing status and sequences to file"
                    setDoc = open("/m/canvas1/mfrechet/patentNumbers.txt")
                    setDoc.write("1\n")
                    for each in numsSet:
                        setDoc.write(each + "\n")
                    setDoc.close()
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
                    print "NCBI failed.  Writing status and sequences to file"
                    setDoc = open("/m/canvas1/mfrechet/patentNumbers.txt")
                    setDoc.write("1\n")
                    for each in numsSet:
                        setDoc.write(each + "\n")
                    setDoc.close()
                    sys.exit('Failed to retrieve the sequence after 200 tries.')
            else:
                break

        #This will hold the relevant sequences from this batch.
        logfile = open('/m/canvas1/mfrechet/SequencesTotal/relSeqsFrom_' + str(retStart) +"_through_"+ str(retStart+index/2) + '.txt', 'w')

        #Test changes start here
        logfile.write(sequence.read())
        logfile.close()
    
        #Remember to change this if US extraction changes.
        #seq = ''
        #newSet = set()
        #seqs = set()

        # Add in all the sequences that are not from patents already covered, and
        #record their patent numbers
        
        #for line in sequence.readlines():
         #   if line.startswith('>'):
                #If the sequence is not empty
          #      if seq != '':
           #         num = None
            #        num = patNum.search(oldLine)
             #       if num is not None:
              #          if antiComma.sub('', str(num.group(1))) not in numsSet:
               #             newSet.add(antiComma.sub('', str(num.group(1))))
                #            seqs.add(seq)
              #  seq = line
               # oldLine = line
           # else:
            #    seq = seq + line

        #Add in the last sequence if it fits the criteria
      #  num = None
      #  num = patNum.search(oldLine)
      #  if num is not None:
       #     if antiComma.sub('', str(num.group(1))) not in numsSet:
        #        newSet.add(antiComma.sub('', str(num.group(1))))
         #       seqs.add(seq)

        #Add the new patent numbers to the list
       # numsSet = numsSet.union(newSet)

       # for each in seqs:
        #    logfile.write(each + os.linesep) 
      #  logfile.close()
    
    print "finished NCBI download"
    sys.exit("finished NCBI download;test complete")

#***This script retrieves the nucleotide sequences in the claims of patents in the Google Patents USPTO Bulk Downloads: Patent Grant Full Text database.  These are limited to patents added in the year 2000 and later.***

#If we failed somewhere in this section last time or we're going through routinely
if int(status) <= 2:

    print "Starting Google bulk sequence download"

    #The page listing all of the patent files

    address ='http://www.google.com/googlebooks/uspto-patents-grants-text.html'

    #Making sure the page opens
    i = 0
    while True:

        try:
            page = urlopen(address)
        except:
            if i < 10:
                i = i + 1
            else:
                print "Google failed.  Writing status and sequences to file"
                setDoc = open("/m/canvas1/mfrechet/patentNumbers.txt")
                setDoc.write("2\n")
                for each in numsSet:
                    setDoc.write(each + "\n")
                setDoc.close()
                sys.exit("Page failed to open after ten tries")
        else:
            break

    toParse = BeautifulSoup(page)

    refs = []
    excluder = re.compile("ipg|pg")

    # Find the sections containing the links to all of the files to download
    start = toParse.find(name='h3', attrs={"id" : "2000"})
    siblings = start.findPreviousSiblings('a')

    # Remove those files not in any of the correct formats
    for each in siblings:
        if excluder.search(str(each('href'))):
            siblings.remove(each)

    #Make a list of the links
    for ahref in siblings:
        refs.append(str(ahref['href']))
     ##   print "appended one"

    for each in refs:
        i = 0
        while True:
            try:
                zippedFile = zipfile26.ZipFile(StringIO(urlopen(each).read()), 'r')
            except:
                if i < 10:
                    i = i + 1
                else:
                    print "Google failed.  Writing status and sequences to file"
                    setDoc = open("/m/canvas1/mfrechet/patentNumbers.txt")
                    setDoc.write("2\n")
                    for each in numsSet:
                        setDoc.write(each + "\n")
                    setDoc.close()
                    sys.exit("Page failed to open after ten tries")
            else:
                break

        #Divide the files and keep only the ones we want.
        divideGoogleFile.Divider(zippedFile, numsSet)

        
    print "finished Google Download"


#***This  extracts and saves the sequences from the PSIPS***

#If we failed here last time or are going through routinely.
if int(status) <= 3:
     
    print "started PSIPS download"

    base = 'http://seqdata.uspto.gov/.psipsv?pageRequest=searchByDate&start='
    startNum = 1

    # The regular expressions to use in this code
    pattern = re.compile('<td><a href="/.psipsv\?pageRequest=docDetail&start=&DocID=(.*)">')
    endPattern = re.compile('No documents are found.')
    totalPattern = re.compile('Enter Sequence ID or Range \((1-[0-9]*)\)')

    #Open the first page
    i = 0
    while True:
        #compensating for page problems. Ten tries seems good.
        try:
            page = urlopen(base+str(startNum)).read()
        except:
            if i < 10:
                i = i + 1
            else:
                print "PSIPS failed.  Writing status and sequences to file"
                setDoc = open("/m/canvas1/mfrechet/patentNumbers.txt")
                setDoc.write("3\n")
                for each in numsSet:
                    setDoc.write(each + "\n")
                setDoc.close()
                sys.exit("URL failed to open after ten tries.")
        else:
            break
    
    #The base urls
    summaryBase= "http://seqdata.uspto.gov/.psipsv?pageRequest=docDetail&start=&DocID="
    patentBase= "http://seqdata.uspto.gov/.psipsv?pageRequest=viewSequence&DocID="

    #Search through all the pages listing sequence listings
    while(re.search(endPattern, page)== None):
        address = base + str(startNum)

        # More Compensation
        i = 0
        while True:
            try:
                page = urlopen(address).read()
            except:
                if i < 10:
                    i = i + 1
                else:
                    print "PSIPS failed.  Writing status and sequences to file"
                    setDoc = open("/m/canvas1/mfrechet/patentNumbers.txt")
                    setDoc.write("3\n")
                    for each in numsSet:
                        setDoc.write(each + "\n")
                    setDoc.close()
                    sys.exit("URL failed to open after ten tries")                          
            else:
                break
                
        list=(re.finditer(pattern, page))

        #for each listed sequence listing
        for each in list:
            i = 0
            while True:
                try:
                    summary = urlopen(summaryBase + each.group(1))
                except:
                    if i < 10:
                        i = i + 1
                    else:
                        print "PSIPS failed.  Writing status and sequences to file"
                        setDoc = open("/m/canvas1/mfrechet/patentNumbers.txt")
                        setDoc.write("3\n")
                        for each in numsSet:
                            setDoc.write(each + "\n")
                        setDoc.close()
                        sys.exit("URL failed to open after ten tries")
                else:
                    break
                

            total = re.search(totalPattern, summary.read())

            #If there is at least one sequence
            if not (total == None):
                file = open('/m/canvas1/mfrechet/BulkSequencesTotal/' + str(each.group(1)) + '.xml', 'w')

                while True:
                    try:
                        file.write(urlopen(patentBase + each.group(1) + "&seqID=" + total.group(1)).read())
                    except:
                        if i < 10:
                            i = i + 1
                        else:
                            print "PSIPS failed.  Writing status and sequences to file"
                            setDoc = open("/m/canvas1/mfrechet/patentNumbers.txt")
                            setDoc.write("3\n")
                            for each in numsSet:
                                setDoc.write(each + "\n")
                            setDoc.close()
                            sys.exit("URL failed to open after ten tries")
                    else:
                        break

                file.close()
         
         
      ##  print "done one page of files"
        startNum = startNum + 10

    file.close()
    print "finished PSIPS download"



#***This retrives and saves patent files with both "SEQ ID" and "SEQUENCE LISTING" in their specifications from the USPTO.***

#If we failed here last time or if we are going through routinely
if int(status) <= 4:

    baseAddress = 'http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=0&f=S&l=50&d=PTXT&OS=SPEC%2F%28%22SEQUENCE+LISTING%22+AND+%22SEQ+ID%22%29&RS=SPEC%2F%28%22SEQUENCE+LISTING%22+AND+%22SEQ+ID%22%29&Query=SPEC%2F%28%22SEQUENCE+LISTING%22+AND+%22SEQ+ID%22%29&TD=39355&Srch1=%28%28%22SEQUENCE+LISTING%22+AND+%22SEQ+ID%22%29.BSUM.+or+%28%22SEQUENCE+LISTING%22+AND+%22SEQ+ID%22%29.DETD.+or+%28%22SEQUENCE+LISTING%22+AND+%22SEQ+ID%22%29.DRWD.%29&NextList'

    #The initial address to retrieve information from
    address = baseAddress + '1' + '=Next+50+Hits'

    i = 0

    #Sometimes the page doesn't open correctly, keep trying 
    while True:
        try:
            print "tyring to open page"
            page = urlopen(address)

        #page failed to open.  Try again
        except Exception:
            if i < 200:
                i = i + 1
            else:
                print "USPTO failed.  Writing status and sequences to file"
                setDoc = open("/m/canvas1/mfrechet/patentNumbers.txt")
                setDoc.write("1\n")
                for each in numsSet:
                    setDoc.write(each + "\n")
                setDoc.close()
                sys.exit("Initial page failed to open after 200 tries")

        #Page opened, move on out of this loop
        else:
            break
                                                    
            toParse = BeautifulSoup(page)

            # the part of the xml we want
            total = int((toParse.contents[0].contents[3].contents[8].contents[5].contents[0]))

    print "Total = " +str(total)


    list = []

    # These regular expressions are used to retrieve the patent numbers from the xml results
    pattern1 = re.compile('[0-9],[0-9][0-9][0-9],[0-9][0-9][0-9]</A></TD>')
    pattern2= re.compile('[0-9],[0-9][0-9][0-9],[0-9][0-9][0-9]')

    # retrieve patent addresses in increments of 50
    for inc in xrange(1, int(total), 1):
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
                    print "USPTO failed.  Writing status and sequences to file"
                    setDoc = open("/m/canvas1/mfrechet/patentNumbers.txt")
                    setDoc.write("1\n")
                    for each in numsSet:
                        setDoc.write(each + "\n")
                    setDoc.close()
                    sys.exit("List page failed to open after 200 tries")
            else:
                break

        #Add the patent id number to the list of patent id number
        lines = re.findall(pattern1 ,page.read())
        ids = []
        for line in lines:
            ids.extend(re.findall(pattern2 ,line))

            #Make sure to include only those patents we don't already have.
            for id in ids:
                if antiComma.sub('',str(id)) not in numsSet:
                    list.append(antiComma.sub('',id))
                
    ##print "Done with " + str(inc)
    print "done fetching ids"
    print "found " + str(len(list)) + "new ids"

    # open the url and retrieve the patent to save
    for patent in list:
        i = 0
        while True:
            try:
                toSave = urlopen(' http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO1&Sect2=HITOFF&d=PALL&p=1&u=%2Fnetahtml%2FPTO%2Fsrchnum.htm&r=1&f=G&l=50&s1=' + str(patent))
            except:
                if i < 200:
                    i = i + 1
                else:
                    print "USPTO failed.  Writing status and sequences to file"
                    setDoc = open("/m/canvas1/mfrechet/patentNumbers.txt")
                    setDoc.write("1\n")
                    for each in numsSet:
                        setDoc.write(each + "\n")
                    setDoc.close()
                    sys.exit("Patent failed to open after 200 tries")
            else:
                break

        #Save the patent
        logfile = open('/m/canvas1/mfrechet/PatentsToExtractFromTotal/'+str(patent)+'.txt', 'w')
        logfile.write(toSave.read())
        logfile.close()
     ##   print "saved" + str(patent)

    print "done USPTO download"

#Write patent numbers and status to file
print "All downloads complete.  Writing sequences and staus."
file = open("/m/canvas1/mfrechet/patentNumbers.txt")
file.write("0\n")
for each in numsSet:
    file.write(each + "\n")
file.close()
                                                                                        
