# -*- coding: utf-8 -*-
import os
import httplib2
import time
import lxml
from bs4 import BeautifulSoup
import requests
startTime = time.time()

class PageScraper(object):
    def __init__(self,url):       
        self.url = url

    def getURL(self):
        try:
            html = self.getHTML(self.url)
            soup = BeautifulSoup(html, 'lxml')
            div_1= soup.body.find('div',attrs={'class':'mw-category-generated'})
            div_2 = div_1.find_all('a')           
            for link in div_2:
                if (link.text == "next page" ): return(link['href'])   # parse the next page link for the benefit of linking to next page
        except AttributeError:
            return None   

    def getHTML(self,url):
        try:
            http=httplib2.Http()
            response,content=http.request(url,'GET')
            return content
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout):
            print ('connect error')
            return None

    def getTotal(self):
        try:
            html = self.getHTML(self.url)
            soup = BeautifulSoup(html, 'lxml')
            div_1= soup.body.find('div',attrs={'class':'mw-category-group'})   #get all href link in this section which of all are category item
            div_2 = div_1.find_all('li')
            for link in div_2:
                self.makeOutput(link.a.text)
        except AttributeError:
            return None   


    def makeOutput(self,snp_id):   
        a = time.strftime('%Y-%m-%d',time.localtime(time.time()))
        f = open("D:/tianguyuan/SNP_Rs.txt", "a+")    #output to txt
        f.write("%s \n" %snp_id)    
        f.close
  

if __name__=='__main__':

    url = "https://www.snpedia.com/index.php?title=Category:Is_a_snp&pagefrom=Rs993804#mw-pages"
    startTime = time.time()
    for i in range (1):
        a = PageScraper(url)
        url = a.joinURL()
        print(url)
        a.getTotal()
        time.sleep(2)
