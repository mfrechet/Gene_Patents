# Separates the Google patents
# saves those files with sequence listings.
# takes a file

import sys, os, re
import zipfile26

class Divider:

    def __init__(self, argv, seqs):

        fil = argv.infolist()[0]
        file = argv.open(fil)

        baseFilePath = "/m/canvas1/mfrechet/GoogleFiles/"
        i = 0
        remove = True
        save = open(baseFilePath + str(fil) + str(i) + ".txt", 'w')
        divider = re.compile("<!DOCTYPE us-patent-grant|<!DOCTYPE PATDOC SYSTEM")
        seqListing = re.compile("<!DOCTYPE sequence-cwu|<SEQLST-US ID") 
        patNum = re.compile("<B110><DNUM><PDAT>[0-9]([0-9],?[0-9][0-9][0-9],?[0-9][0-9][0-9])</PDAT></DNUM></B110>")
        patNum2 = re.compile("<doc-number>[0-9]([0-9],?[0-9][0-9][0-9],?[0-9][0-9][0-9])</doc-number>")

        newSeqs = set()
        antiComma = re.compile(',')

        #Read every line
        for line in file.readlines():

            #If either is true, assign it to num
            if patNum.search(line) is not None or patNum2.search(line) is not None:
                num = patNum.search(line) | patNum2.search(line)

            #When starting a new patent
            if divider.search(line) is not None:

                #If there already was one being processed, close it and delete it
                #if it does not meet the conditions.
                if save is not None:
                    save.close()

                    #Rename
                    if num is not None:
                        os.rename(baseFilePath +str(fil) + str(i) + ".txt", baseFilePath + str(num.group(1)) + str(i) + ".txt")

                        #add patent num
                        if antiComma.sub('', str(num.group(1))) not in seqs:
                            newSeqs.add('', antiComma.sub(str(num.group(1))))
                            
                    
                    #remove the extra files
                    if remove:

                        if num is not None:
                            os.remove(baseFilePath + str(num.group(1)) + str(i) + ".txt")
                            #We don't really want this patent number
                            if antiComma.sub('', num.group(1)) in newSeqs:
                                newSeqs.remove(antiComma.sub('', str(num.group(1))))
                        else:
                            os.remove(baseFilePath + str(num.group(1)) + str(i) + ".txt")
                    num = None


                i+=1
                save = open(baseFilePath + str(fil) + str(i) +".txt", "w")
                save.write(line)
                remove = True

            #Look for the Sequence listing start
            else:
                #If we have found the sequence listing
                if seqListing.search(line) is not None:
                        remove = False
                save.write(line)
                
        save.close()
        
         #Rename
        if num is not None:
            os.rename(baseFilePath + str(fil) + str(i) + ".txt", baseFilePath + str(num.group(1)) + str(i) + ".txt")

            #add patent num
            if antiComma.sub('', str(num.group(1))) not in seqs:
                newSeqs.add(antiComma.sub('', str(num.group(1))))
        
        #Remove the last file if it needs removing
        if remove:

            if num is not None:
                os.remove(baseFilePath + str(num.group(1)) + str(i) + ".txt")
                #We don't really want this patent num
                if num.group(1) in newSeqs:
                    newSeqs.remove(num.group(1))
            else:
                os.remove(baseFilePath + str(fil) + str(i) + ".txt")

        seqs = seqs.union(newSeqs)
