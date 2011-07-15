

from BeautifulSoup import BeautifulSoup, SoupStrainer
import re

file = open("/m/canvas1/mfrechet/toProcess.xml", "rb")
save = open("/m/canvas1/mfrechet/toProcess2.xml", 'w')

write = 20
for each in file:
    
   if re.search('<entry>5&#x2032;', each):
#        save.write(each)
#         write =  write +
print each

#   if re.search('SEQ ID',each):
#        write = 0

save.close()

file.close()
                        
