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
    title=title.replace("/","&")
    open('./CHPO/%s' %title,'w+').write(snp_page)    # write into file
    
if __name__=='__main__':
    item = []
    if os.path.exists("./CHPO"): pass       
    else:
        os.mkdir("./CHPO")
#    item_id = "Abnormality_of_connective_tissue"
    item_id = ["Abnormality_of_connective_tissue","Abnormality_of_the_voice","Abnormality_of_the_nervous_system","Abnormality_of_the_breast",
               "Abnormality_of_the_eye","Abnormality_of_prenatal_development_or_birth","Neoplasm","Abnormality_of_the_endocrine_system",
               "Abnormality_of_head_and_neck","Abnormality_of_the_immune_system","Growth_abnormality","Abnormality_of_limbs","Abnormality_of_the_thoracic_cavity",
               "Abnormality_of_blood_and_blood-forming_tissues","Abnormality_of_the_musculature","Abnormality_of_the_cardiovascular_system","Abnormality_of_the_skeletal_system",
               "Abnormality_of_the_respiratory_system","Abnormality_of_the_ear","Abnormality_of_metabolism/homeostasis","Abnormality_of_the_genitourinary_system",
               "Abnormality_of_the_integument","Abnormality_of_the_digestive_system","Mode_of_inheritance","Mortality/Aging","Clinical_modifier"]
    for name in item_id:
        getcontent(name)
        print "%s loaded" %(name)
        finishTime = time.time()
        processingTime = finishTime - startTime         
        print "complete one set using %d seconds"%processingTime       
       