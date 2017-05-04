# -*- coding: utf-8 -*-
import requests
def query(request):
    
    # Clone original request
    
    # Modify it with the values returned in the 'continue' section of the last result.
    
    # Call API
    result = requests.get('http://bots.snpedia.com/api.php?', params=request).json()       
    for i in range(500):
        snp_id = result['query']["categorymembers"][i+374]["title"]
        makeOutput(snp_id)
    #if 'error' in result:
        #raise Error(result['error'])
    #if 'warnings' in result:
        #print(result['warnings'])
    #if 'query' in result:
        #yield result['query']
        
def makeOutput(snp_id):   
    f = open("./SNPedia_Is_a_medical_condition.txt", "a+")             #output to txt
    f.write("%s\n" %snp_id)    
    f.close
        
if __name__=='__main__':
    request={}
    request['action'] = 'query'
    request['format'] = 'json'    
    request['list']='categorymembers'
    request['cmtitle']='Category:Is_a_medical_condition'
    request['cmlimit']=500
 #   request = "action=query&list=categorymembers&cmtitle=Category:Is_a_snp&cmlimit=5000&generator=allpages"
    query(request)
  #  print(a)

