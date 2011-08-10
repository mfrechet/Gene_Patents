import os
from gzip import GzipFile

toSave = open('/m/canvas1/mfrechet/blastDirectory.rna.fna', 'w')
for file in os.listdir('/m/canvas1/mfrechet/dbs/'):
   unzipFile = GzipFile('/m/canvas1/mfrechet/dbs/' + str(file))
   toSave.write(unzipFile.read())
toSave.close()
