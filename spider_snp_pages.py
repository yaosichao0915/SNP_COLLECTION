# -*- coding: utf-8 -*-
import os
import csv
import re
import json
import httplib2
import codecs
import time
import lxml
import multiprocessing
from bs4 import BeautifulSoup
import datetime
import requests
import dbconnection
startTime = time.time()





class PageScraper(object):
    def __init__(self, item_id):
        self.item_id = item_id
        self.url = self.joinURL(item_id)
       # self.cookies = self.getCookies(shop_id)
   #     self.cookies ="BIGipServerwww.metro.cn-80=1704433725.20480.0000; ASP.NET_SessionId=43xzm0452rzm4ke4wet2wub3; TempID=Cart28b17e68-36e2-4a99-9013-04d70da9d4ca; isClearCookies=1; s_cc=true; vProductID=378756,218097; s_fid=5C1740094EBF8DAA-31FD420BAF3FED8B; s_sq=metro-cn-shop%3D%2526pid%253Dhttps%25253A%25252F%25252Fwww.metromall.cn%25252FProduct%25252FProductDetail.aspx%25253FProductID%25253D123020%2526oid%253Dfunctiononclick%252528event%252529%25257Bopenmap%252528%252529%25253B%25257D%2526oidt%253D2%2526ot%253DA; LoginLastPage=https://www.metromall.cn/Product/ProductSearch.aspx?keyword=%E5%A4%8F%E6%A1%90; PostStaID=79; _ga=GA1.2.625977379.1485455648; Hm_lvt_612cbb515a48ab6435405cba354ca6ec=1485455558,1485455648; Hm_lpvt_612cbb515a48ab6435405cba354ca6ec=1485471772; __xsptplus270=270.3.1485471747.1485471773.2%234%7C%7C%7C%7C%7C%23%23NnAjRvF147940yrjyoDRYyU_crCv0FGk%23"
    
    def joinURL(self,item_id):
        urlFirst= u'https://www.snpedia.com/index.php/'
        query = ''.join([self.item_id])
        url = ''.join([urlFirst,query])
        return url 
    
    def getHTML(self,url):
        
      #  headers = {"headers":str(self.cookies)}
        try:
            http=httplib2.Http()
            response,content=http.request(url,'GET')
            return content
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
            print ('connect error')
            return None
        
    def getTotal(self):
        gene = 0
        position = 0
        chromosome = 0
        
        try:
            html = self.getHTML(self.url)
            soup = BeautifulSoup(html, 'lxml') 
            div_1= soup.body.find('div',attrs={'id':'mw-content-text'})
            
            div_td_common = div_1.find_all('td')
            for name in div_td_common:
                    if (name.text=="Chromosome"): chromosome = name.next_sibling.text.rstrip('\n')
                    if (name.text=="Position"): position = name.next_sibling.text.rstrip('\n')
                    if (name.text=="Gene"): gene = name.next_sibling.text.rstrip('\n')
                   # print (gene)
           # print (chromesome,position)
            div_table1= div_1.find('table', attrs={'class':'sortable smwtable'})
            div_td = div_table1.find_all('td')                
            for name in div_td:
                repute = 'normal'
                    #snp.append(name.get_text().rstrip('\n'))
                if (name.a) : 
                    snp_id = name.text.rstrip('\n') 
                    gene_max = name.next_sibling.next_sibling.text.rstrip('\n')
                    if name.next_sibling.next_sibling['style'] == "border-bottom-style: groove; background: #80ff80" : repute = 'good'
                    if name.next_sibling.next_sibling['style'] == "border-bottom-style: groove; background: #ff8080" : repute = 'bad'
                    gene_content = name.next_sibling.next_sibling.next_sibling.next_sibling.text.rstrip('\n')
                    gene_content = gene_content.replace(',','')
                    gene_content = str(gene_content)
               #     print (gene_content)
                #    self.makeOutput(snp_id,gene_max,gene_content,chromosome,position,gene,repute)
                    self.Outputtodb(self.item_id,snp_id,gene_max,repute,chromosome,position,gene,gene_content,self.url)
            #self.makeOutput(snp)
           # print (snp[0],snp[1])
            
        except AttributeError:
            return None   
    

        
    def makeOutput(self,snp_id,gene_max,gene_content,chromesome,position,gene,repute):   
        a = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        with open('./results/'+self.item_id+a+'.csv', 'a+') as writer:         
       #     writer.write(codecs.BOM_UTF8)
            
            writer.write('%s,%s,%s,%s,%s,%s,%s,%s\n' %(self.item_id,snp_id,gene_max,gene_content,chromesome,position,gene,repute) )  
            writer.close()    
            
    def Outputtodb(self,item_id,snp_id,gene_max,repute,chromosome,position,gene,gene_content,url):
        t = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        dbconnection.insertdata(self.item_id,snp_id,gene_max,repute,chromosome,position,gene,gene_content,self.url)    
        
    def runScraper(self,item_name):

     #   shop_id = ["10","11","12","13","14","15"]
        for id in range(len(self.shop_id)):
            scraper1 = PageScraper(item_name) 
            scraper1.getTotal()
            finishTime = time.time()
            processingTime = finishTime - startTime         
            print ("complete one set using %d seconds"%processingTime)    


if __name__=='__main__':
    item = []
    url = "https://www.snpedia.com/index.php/Rs1815739"
    startTime = time.time()
    if os.path.exists("./results"): pass       
    else:
        os.mkdir("results")
    file = open("1.txt", "r")
    while 1:
        line = file.readline().rstrip('\n')
        line = line.rstrip()
        item.append(line)
        if not line:
            break
        pass    
   # print (item_id[3])
    file.close
    item_id = item[99:600]
   # item_id = ['Rs1012053','Rs1020101']
    print(item_id)
    
    for name in item_id:
        a = PageScraper(name)
        a.getTotal()
        print("%s loaded" %(name))
        time.sleep(1)