'''
Created on Jun 8, 2011

@author: melissafrechette
'''

from urllib import urlopen
import gzip
import os

#logfile = open('/Users/melissafrechette/Documents/workspace/Patents/PatenLensSequences/sequences.txt', 'w')
#logfile.write(urlopen('http://www.patentlens.net/sequence/US_A/nt-inClaims.fsa.gz'))
#logfile.close()
zippedFile = urlopen('http://www.patentlens.net/sequence/US_A/nt-inClaims.fsa.gz')
#files = zipfile.ZipFile(fh)
#for fileName in files.nameList():
#    output = open(fileName, 'wb;')

#fh = open('foo.zip', 'rb')
#z = zipfile.ZipFile(fh)
#for name in z.namelist():
#    outfile = open(name, 'wb')
#    outfile.write(z.read(name))
#    outfile.close()
print("got this far")
    
file = gzip.open(zippedFile.read())
#file = gzip.open("/Users/melissafrechette/Downloads/nt-inClaims.fsa.gz", "rb")
print("opened")

output = open("/m/canvas1/mfrechet/nt-inClaims.fsa", 'w')
output.write(str(file.read()))
file.close()
output.close()

#for name in files:
 #   print("1")
  #  output = open(os.path.join(os.path.expanduser("~"), str(name)))
   # print("2")
    #output.write(files.read(name))
  #  print("writing a file")
   # output.close()
print("finished")
    