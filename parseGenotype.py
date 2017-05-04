# -*- coding: utf-8 -*-
import os
import mwparserfromhell
class PageParser(object):
    def __init__(self,dir):
        self.files = self.AllFiles(dir)

    def AllFiles(self,filepath):
        for root,dirs,files in os.walk(dir):
            return files

    def ReadFile(self,file):
        f = open('./Rs_genotype/%s'%file,'rb')
        content = f.read()
        return content

    def GrepContent(self):
        for file in self.files[10:60]:
            text = self.ReadFile(file)
            wikicode = mwparserfromhell.parse(text)
            ts = wikicode.filter_templates()
            if not ts:
                return {}
            t = ts[0]
    
            geno = {}
            if t.name.strip() == 'Genotype':
                for key in ['rsid', 'allele1','allele2', 'magnitude', 'repute', 'summary']:
                    try:
                        value = t.get(key)
                        value = value.strip().split('=')[-1]
                    except ValueError:
                        continue
                    else:
                        geno[key.lower()] = value
    
            if not geno.get('rsid', ''):
                return {}
    
            if not geno.get('magnitude', ''): 
                geno['magnitude'] = 0
            else:
                try:
                    geno['magnitude'] = float(geno['magnitude'])
                except ValueError:
                    geno['magnitude'] = 0
                    
            if geno['allele1']:
                geno['allele'] = geno.get('allele1', '') + geno.get('allele2', '')
            else: print('no allele %s'%rsid)

            print(geno)
 

if __name__=='__main__':
    dir="D:\\tianguyuan\snpedia_wiki\Rs_genotype"
    a = PageParser(dir)
    geno = a.GrepContent()
  #  print(geno)