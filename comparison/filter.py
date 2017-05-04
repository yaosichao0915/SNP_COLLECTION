import vcf
import csv
import codecs
class Comparison(object):
    def __init__(self):
        pass
    def read_files(self):
        vcf_reader1 = vcf.Reader(open('12468218.vcf','r'))
        vcf_reader2 = vcf.Reader(open('58033616.vcf','r'))  
        return (vcf_reader1,vcf_reader2)

    def diff_ALT(self):  
        vcf_reader1,vcf_reader2 = self.read_files()
        for record1 in vcf_reader1:
            ref1[record1.ID]=record1.ALT    
        for record2 in vcf_reader2:
            if record2.ID in ref1.keys():
                if ref1[record2.ID]!=record2.ALT: print (record2.ID)

    def diff_id(self):
        vcf_reader1,vcf_reader2 = self.read_files()
        for record1 in vcf_reader1:
            ref1[record1.ID]=1
        for record2 in vcf_reader2:
            if record2.ID not in ref1.keys():
                print(record2.ID)

    def diff_allele(self):
        i = 0
        vcf_reader1,vcf_reader2 = self.read_files()
        for record1 in vcf_reader1:
            for sample1 in record1.samples:
                if record1.FILTER == []:
                    record1.FILTER = 'pass'
                if record1.FILTER == ['NOCALL']:
                    record1.FILTER = 'NOCALL' 
                self.addtwodimdict(Alt,record1.ID,'GT',sample1['GT'])
                self.addtwodimdict(Alt,record1.ID,'FILTER',record1.FILTER)
                #Alt[record1.ID]['GT'] = sample1['GT']
                #Alt[record1.ID]['FILTER'] = record1.FILTER

        for record2 in vcf_reader2:
            for sample2 in record2.samples:
                if record2.ID in Alt.keys():
                    if Alt[record2.ID]['GT']!= sample2['GT']:
                        i+=1
                        #f = open("allele1.txt", "a+")    #output to txt
                        #f.write("%s ; %s ; %s ; %s ; %s ; %s \n" %(record2.ID,record2,record2.FILTER,sample2,Alt[record2.ID]['FILTER'],Alt[record2.ID]['GT']) )   
                        #f.close 
                        if record2.FILTER == [] : record2.FILTER = 'pass'
                        if record2.FILTER == ['NOCALL']:record2.FILTER = 'NOCALL'                        
                       # print (sample2['GT'])
                        self.makeOutput(record2.ID,record2,record2.FILTER,str(sample2['GT']),Alt[record2.ID]['FILTER'],str(Alt[record2.ID]['GT']))
    def makeOutput(self,a,b,c,d,e,f):   
                       
        with open('2.txt', 'a+') as writer:         
        #    writer.write(codecs.BOM_UTF8)
            writer.write('%s;%s;%s;%s;%s;%s\n' %(a,b,c,d,e,f) )  
            writer.close()    
    def addtwodimdict(self, thedict, key_a, key_b, val):
        if key_a in thedict:
            thedict[key_a].update({key_b: val})
        else:
            thedict.update({key_a:{key_b: val}})
    
if __name__=="__main__":    
    ref1 = {}
    ref2 = {}   
    Alt = {}
    a = Comparison()
    #  a.diff_id() 
    # a.diff_ALT()
    a.diff_allele()
