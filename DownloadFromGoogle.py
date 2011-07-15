'''
Created on Jun 13, 2011

@author: melissafrechette
'''
from urllib import urlopen
from BeautifulSoup import BeautifulSoup, SoupStrainer
import zipfile
import tarfile
from StringIO import StringIO
import re

address ='http://www.google.com/googlebooks/uspto-patents-grants-text.html'

page = urlopen(address)
toParse = BeautifulSoup(page)

refs = []

start = toParse.find(name='h3', attrs={"id" : "2000"})
siblings = start.findPreviousSiblings('a')

for ahref in siblings:
    refs.append(str(ahref['href']))
    print "appended one"

sequences = open('/m/canvas1/mfrechet/GoogleSequences.txt', 'w')
sequences.write("")
sequences = open('/m/canvas1/mfrechet/GoogleSequences.txt', 'a')

for each in refs:
    print "started searching"

    
    doc = zipfile.ZipFile(StringIO(urlopen(each).read()))
<<<<<<< HEAD
    list = doc.namelist()

    print list
=======
    list = doc.infolist()
>>>>>>> 0ccbda6bca0f19eec3d40a6588bf23b020cf183f
    
    for name in list:
        
        file = doc.read(name)
        string = StringIO(file)
        write = False
        skip = False

<<<<<<< HEAD
        listing = SoupStrainer('SEQUENCE LISTING')
=======
        listing = SoupStrainer(text = re.compile('SEQUENCE LISTING'))
>>>>>>> 0ccbda6bca0f19eec3d40a6588bf23b020cf183f
        soup = BeautifulSoup(file, parseOnlyThese=listing)

        print soup.prettify()
#        if "SEQUENCE LISTING" in file:
 #           print "found SEQUENCE LISTING"
  #          for line in string.readlines():
   #             print "checking for SEQ ID"
#
 #               if skip:
  #                  write = True
#
 #               if write:
  #                  sequences.write("> Sequence \n"+str(line)+"\n")
   #                 print "wrote one"
    #                skip = False
     #               write = True

     #            else:
       #             if "SEQ ID" in line:
        #                skip = True
                
sequences.close()

print "done"
    
