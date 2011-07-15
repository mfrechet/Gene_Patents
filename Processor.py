from BeautifulSoup import BeautifulSoup, SoupStrainer
import re

file = open("/m/canvas1/mfrechet/ipg110104.xml", "rb")

listing = SoupStrainer('entry', text = re.compile('SEQUENCE LISTING'))
soup = BeautifulSoup(file, parseOnlyThese = listing)
print soup.prettify()
file.close()
