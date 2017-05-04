# -*- coding: utf-8 -*-
# using python2
from wikitools import wiki, category, page
import sys
import os
import time
startTime = time.time()
def getcontent(title):
    site = wiki.Wiki("http://wiki.chinahpo.org/api.php?")
    pagehandle = page.Page(site, title)     #title is the name of each SNP
    snp_page = pagehandle.getWikiText()     #Wiki page parse
    #print snp_page.encode('u8')
    open('./Rs_genotype/%s' %title,'w+').write(snp_page)    # write into file
    
if __name__=='__main__':
    item = []
    i = 0
    if os.path.exists("./Rs_genotype"): pass       
    else:
        os.mkdir("Rs_genotype")
    file = open("SNP_Genotype_Rs.txt", "r")
    while 1:                           # read from ID list from the  previous collected list
        line = file.readline().rstrip('\n')
        line = line.rstrip()
        item.append(line)
        if not line:
            break
        pass    
  
    file.close
    item_id = item[:100]   # choose part of SNP
    
    for name in item_id:
        if os.path.exists("./Rs_genotype/%s"%name):
            continue        
        i += 1
        getcontent(name)
        print "%s loaded" %(name)
        finishTime = time.time()
        processingTime = finishTime - startTime         
        print "No.1 complete %s set using %d seconds"%(i,processingTime)       
        time.sleep(0.2)