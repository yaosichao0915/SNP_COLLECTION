import requests
def query(request):
    lastContinue = {'continue': ''}
    while True:
        # Clone original request
        req = request.copy()
        # Modify it with the values returned in the 'continue' section of the last result.
        req.update(lastContinue)
        # Call API
        result = requests.get('http://bots.snpedia.com/api.php?', params=req).json()
        if 'continue' not in result:
            break        
        for i in range(500):
            snp_id = result['query']["categorymembers"][i]["title"]
            makeOutput(snp_id)
        #if 'error' in result:
            #raise Error(result['error'])
        #if 'warnings' in result:
            #print(result['warnings'])
        #if 'query' in result:
            #yield result['query']
        
        lastContinue = result['continue']
def makeOutput(snp_id):   
    f = open("./SNPedia_Is_a_medical_condition.txt", "a+")             #output to txt
    f.write("%s\n" %snp_id)    
    f.close
        
if __name__=='__main__':
    request={}
    request['action'] = 'query'
    request['format'] = 'json'    
    request['list']='categorymembers'
    request['cmtitle']='Category:Is_a_snp'
    request['cmlimit']=500
 #   request = "action=query&list=categorymembers&cmtitle=Category:Is_a_snp&cmlimit=5000&generator=allpages"
    query(request)
  #  print(a)

