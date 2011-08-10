from ftplib import FTP
import re, os
from gzip import GzipFile

page = FTP("ftp.ncbi.nih.gov", "anonymous", "mfrechet@cs.umass.edu")

#file.cwd("refseq/release/complete/")

listing = page.nlst("refseq/release/complete/")
wanted = re.compile("/complete.*\.rna\.fna")

def record(args):
    toSave.write(args)

i = 0
for each in listing:
    if wanted.search(each) is not None:
        toSave = open('/m/canvas1/mfrechet/dbs/' + str(i)  + '.rna.fna.gz', 'w')
        page.retrbinary("RETR " + str(each), record)
        toSave.close()
        i = i + 1

toSave = open('/m/canvas1/mfrechet/blastDirectory.rna.fna', 'w')
for file in os.listdir('/m/canvas1/mfrechet/dbs/'):
    unzipFile = GzipFile(file)
    toSave.write(unzipFile.read())
toSave.close()
