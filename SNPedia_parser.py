# -*- coding: utf-8 -*-
import os
import re
import mwparserfromhell
import dbconnection
class PageParser(object):
    def __init__(self,dir_genotype,dir_snp):
       # self.files_snp = self.AllFiles(dir_snp)
        self.files_genotype = self.AllFiles(dir_genotype)

    def AllFiles(self,filepath):
        for root,dirs,files in os.walk(filepath):
            return files

    def ReadFile_genotype(self,file):
        f = open('./Rs_genotype/%s'%file,'rb')
        content = f.read()
        return content
    
    def ReadFile_snp(self,file):
      #  f = open('./Rs/Rs10178458','rb')
        f = open('./Rs/%s'%file,'rb')
        content = f.read()
        return content  
        
    def GrepContent_genotype(self):
        rounds = 1
        for file in self.files_genotype:
            geno = {}
            geno['repute']= None
            geno['summary']= None
            text = self.ReadFile_genotype(file)
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
                continue
            
            if not geno.get('magnitude', ''): 
                geno['magnitude'] = 0
            else:
                try:
                    geno['magnitude'] = float(geno['magnitude'])
                except ValueError:
                    geno['magnitude'] = 0
                    
            if geno.get('allele1',''):
                geno['allele'] = geno.get('allele1', '') + ';' + geno.get('allele2', '')
            else: geno['allele'] = '-;-'
            #else: print('no allele %s'%rsid)
            rs_id = 'Rs'+geno['rsid'].lstrip()
            
            if not os.path.isfile('./Rs/%s'%rs_id): continue
            
            self.Combination(geno)
            if rounds % 10 == 0 : print ('%s %s complete'%(rounds,geno['rsid']))
            rounds += 1
            
    def GrepContent_snp(self,rs_id):
        rs = {}
        rs['pmid'] = []
        rs['omim_id'] = []
        rs['gene'] = None
        rs['summary_snp'] = None
        text = self.ReadFile_snp(rs_id)
        wikicode = mwparserfromhell.parse(text)
        template = wikicode.filter_templates()
        length = len(template)
        for i in range (length):
            t = template[i]
            if t.name.strip() == 'Rsnum':
                for key in ['rsid','Gene', 'Chromosome', 'position', 'Orientation']:
                    try:
                        value = t.get(key)
                        value = value.strip().split('=')[-1]
                    except ValueError:
                        continue
                    else:
                        rs[key.lower()] = value
                for key in ['Summary']:
                    try:
                        value = t.get(key)
                        value = value.strip().split('=')[-1]
                    except ValueError:
                        continue
                    else:
                        rs['summary_snp'] = value                
            if t.name.strip() == 'PMID Auto':
                for key in ['PMID']:
                    try:
                        value = t.get(key)
                        value = value.strip().split('=')[-1]
                    except ValueError:
                        continue
                    else:
                        rs[key.lower()].append(value)
                        
            if t.name.strip() == 'omim':
                for key in ['id']:
                    try:
                        value = t.get(key)
                        value = value.strip().split('=')[-1]
                    except ValueError:
                        continue
                    else:
                        rs['omim_id'].append(value)
        return(rs)
            
    def Combination(self,geno):
        result = {}
        result['rsid'] = None
        result['repute'] = None
        result['summary_genotype'] = None
        result['allele'] = None
        result['magnitude'] = None
        result['gene'] = None
        result['omim_id'] = None
        result['chromosome'] = None
        result['position'] = None
        result['orientation'] = None
        result['summary_snp'] = None
        result['pmid'] = None
        rs_id = 'Rs'+geno['rsid'].lstrip()
        rs = self.GrepContent_snp(rs_id)
        result['rsid'] = rs_id
        if 'repute' in geno :
            result['repute'] = geno['repute']
        if 'summary' in geno :
            result['summary_genotype'] = geno['summary']
        if 'allele' in geno :
            result['allele'] = geno['allele']
        if 'magnitude' in geno :
            result['magnitude'] = geno['magnitude']        
        if 'position' in rs :
            result['position'] = rs['position']
        if 'chromosome' in rs :
            result['chromosome'] = rs['chromosome']
        if 'orientation' in rs :
            result['orientation'] = rs['orientation']
        if 'gene' in rs :
            result['gene'] = rs['gene']
        if 'pmid' in rs and rs['pmid'] != [] :
            result['pmid'] = str(rs['pmid'])
        if 'omim_id' in rs and rs['omim_id'] != []:
            result['omim_id'] = str(rs['omim_id']) 
        if 'summary_snp' in rs :
            result['summary_snp'] = rs['summary_snp']
        self.OutPutDB(result)
        
    def OutPutDB(self,result):
 #       print(result['rsid'],result['allele'],result['repute'],result['magnitude'],result['gene'],result['chromosome'],result['position'],result['orientation'],result['summary_snp'],result['summary_genotype'],result['pmid'],result['omim_id'])
        dbconnection.insertdata(result['rsid'],result['allele'],result['repute'],result['magnitude'],result['gene'],result['chromosome'],result['position'],result['orientation'],result['summary_snp'],result['summary_genotype'],result['pmid'],result['omim_id'])
        
if __name__=='__main__':
    dir_genotype="D:\\tianguyuan\snpedia_wiki\Rs_genotype"
    dir_snp="D:\\tianguyuan\snpedia_wiki\Rs"
    a = PageParser(dir_genotype, dir_snp)
    geno = a.GrepContent_genotype()
