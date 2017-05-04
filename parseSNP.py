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
        #print (self.files)
        f = open('./Rs/%s'%file,'rb')
        content = f.read()
        return content
    
    def GrepContent(self):
        for file in self.files[:10]:
            rs = {}
            rs['pmid'] = []
            rs['omim_id'] = []
            text = self.ReadFile(file)
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
                                    
            print(rs)

if __name__=='__main__':
    dir="D:\\tianguyuan\snpedia_wiki\Rs"
    a = PageParser(dir)
    rs = a.GrepContent()
    