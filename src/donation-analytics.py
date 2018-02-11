import sys
import os.path
import heapq
import math

COLNAMES = {
    'CMTE_ID':0,
    'NAME':7,
    'ZIP_CODE':10,
    'TRANSACTION_DT':13,
    'TRANSACTION_AMT':14,
    'OTHER_ID':15
} 



class Percentile:
    def __init__(self,percentile):
        self.minheap=[]
        self.maxheap=[]
        self.num=0
        self.count=0
        self.percentile=percentile
        
    def updateheaps(self,num):
        if (self.count==0):
            self.count=self.count+1
            self.num=num
            return num
        elif (self.count==1):
            heapq.heappush(self.minheap,max(self.num,num))
            heapq.heappush(self.maxheap,-min(self.num,num))
            self.count=self.count+1
            return min(self.num,num)  
        else:
            maxheapsize=int(math.ceil(self.percentile/100.0*(self.count+1)));
            if(len(self.maxheap)==maxheapsize and len(self.minheap)<(self.count-maxheapsize+1)):
                    maxheaptopelement=-1*heapq.heappop(self.maxheap)
                    minheaptopelement=heapq.heappop(self.minheap)
                    if (num<maxheaptopelement):
                            heapq.heappush(self.maxheap,-1*num)
                            heapq.heappush(self.minheap,maxheaptopelement)
                            heapq.heappush(self.minheap,minheaptopelement)
                            self.count=self.count+1
                            return -1*(heapq.nsmallest(1,self.maxheap)[0])
                    if (num>=maxheaptopelement and num<minheaptopelement):
                            heapq.heappush(self.maxheap,-1*maxheaptopelement)
                            heapq.heappush(self.minheap,num)
                            heapq.heappush(self.minheap,minheaptopelement)
                            self.count=self.count+1
                            return -1*(heapq.nsmallest(1,self.maxheap)[0])
                    if (num>=minheaptopelement):
                            heapq.heappush(self.minheap,num)
                            heapq.heappush(self.minheap,minheaptopelement)
                            heapq.heappush(self.maxheap,-1*maxheaptopelement)
                            self.count=self.count+1
                            return -1*(heapq.nsmallest(1,self.maxheap)[0])
            else:
                    maxheaptopelement=-1*heapq.heappop(self.maxheap)
                    minheaptopelement=heapq.heappop(self.minheap)
                    if (num<maxheaptopelement):
                            heapq.heappush(self.maxheap,-1*num)
                            heapq.heappush(self.maxheap,-1*maxheaptopelement)
                            heapq.heappush(self.minheap,minheaptopelement)
                            self.count=self.count+1
                            return -1*(heapq.nsmallest(1,self.maxheap)[0])
                    if (num>=maxheaptopelement and num<minheaptopelement):
                            heapq.heappush(self.maxheap,-1*maxheaptopelement)
                            heapq.heappush(self.maxheap,-1*num)
                            heapq.heappush(self.minheap,minheaptopelement)
                            self.count=self.count+1
                            return -1*(heapq.nsmallest(1,self.maxheap)[0])                         
                    if (num>=minheaptopelement):
                            heapq.heappush(self.minheap,num)
                            heapq.heappush(self.maxheap,-1*maxheaptopelement)
                            heapq.heappush(self.maxheap,-1*minheaptopelement)
                            self.count=self.count+1
                            return -1*(heapq.nsmallest(1,self.maxheap)[0])


def dictprinter(FILE_OBJ_REPEAT_DONORS,a):
    FILE_OBJ_REPEAT_DONORS.write(a[0]+"|"+a[1]+"|"+str(int(a[2]))+"|"+str(int(round((a[4]))))+"|"+str(int(a[6]))+"|"+str(int(a[5]))+"\n")

def main(argv):
    #Reading filename from commandline location
    ITCONTFILE=sys.argv[1]
    PERCENTILEFILE=sys.argv[2]
    REPEAT_DONORS_FILE=sys.argv[3]
    
    
    #Check whether itcont.txt & percentile.txt files exist
    if (not os.path.isfile(ITCONTFILE)):
    	print "ERROR:itcont.txt does not exist.Check Path"
    	exit(1)
    if (not os.path.isfile(PERCENTILEFILE)):
    	print "ERROR:percentile.txt does not exist.Check Path"
    	exit(1)
    
    
    #Create repeat_donors.txt
    FILE_OBJ_REPEAT_DONORS=open(REPEAT_DONORS_FILE,"w+");
    
    with open(PERCENTILEFILE) as f:
        c=f.readlines()
    PERCENTILE = float(c[0]);
  
    with open(ITCONTFILE) as f:
        REPEAT_DONOR_DICT={}
        CMTE_ID_ZIP_DICT={}
        for line in f:
            row = line.rstrip('\n')
            row = row.split('|')
            #Checking Data Specifications based  on https://classic.fec.gov/finance/disclosure/metadata/DataDictionaryContributionsbyIndividuals.shtml
            #Sanity Check 1:Skip row if it does not have 21 data items 
            if(len(row)!=21):
                continue
            #Sanity Check 2:Skip row if CMTE_ID is not 9 characters
            if (len(row[COLNAMES['CMTE_ID']])!=9):
                continue
            #Sanity Check 3:Skip row if ZIP_CODE is not 9 characters
            if (len(row[COLNAMES['ZIP_CODE']])!=9):
                continue
            #Sanity Check 4:Skip row if TRANSACTION_DT is not 8 characters
            if (len(row[COLNAMES['TRANSACTION_DT']])!=8):
                continue          
            #Sanity Check 5:Skip row if TRANSACTION_AMT is not a number
            try:
                float(row[COLNAMES['TRANSACTION_AMT']])
            except ValueError:
                continue
            
            #Remove rows with OTHER_ID  having finite values to remove non-individual 
            if (len(row[COLNAMES['OTHER_ID']])!=0):
                continue
            
            CMTE_ID=row[COLNAMES['CMTE_ID']]
            NAME=row[COLNAMES['NAME']]

            #Truncate ZIP_CODE to 5 digits
            ZIP_CODE=row[COLNAMES['ZIP_CODE']][0:5]
            #Converting TRANSACTION_DT to year format
            TRANSACTION_DT=int(row[COLNAMES['TRANSACTION_DT']][4:10])
            TRANSACTION_AMT=float(row[COLNAMES['TRANSACTION_AMT']])
            
            key=(NAME,ZIP_CODE)
            if key in CMTE_ID_ZIP_DICT:    
                CMTE_ID_ZIP_DICT[key][1]=CMTE_ID_ZIP_DICT[key][1]+1
                ##Out-of-order case
                if (TRANSACTION_DT<CMTE_ID_ZIP_DICT[key][0]):
                    CMTE_ID_ZIP_DICT[key]=[TRANSACTION_DT,1]

                if (CMTE_ID_ZIP_DICT[key][1]>1):
                    key2=(CMTE_ID,ZIP_CODE)
                    if key2 in REPEAT_DONOR_DICT:
                        REPEAT_DONOR_DICT[key2][6]=REPEAT_DONOR_DICT[key2][6]+TRANSACTION_AMT
                        perc=round(REPEAT_DONOR_DICT[key2][3].updateheaps(TRANSACTION_AMT))
                        REPEAT_DONOR_DICT[key2][5]=REPEAT_DONOR_DICT[key2][5]+1
                        dictprinter(FILE_OBJ_REPEAT_DONORS,REPEAT_DONOR_DICT[key2])                               
                    else:
                        x = Percentile(PERCENTILE)
                        perc=x.updateheaps(TRANSACTION_AMT)
                        runnumtotal=1
                        runamttotal=TRANSACTION_AMT;
                        REPEAT_DONOR_DICT[key2]=[CMTE_ID,ZIP_CODE,TRANSACTION_DT,x,perc,runnumtotal,runamttotal]
                        dictprinter(FILE_OBJ_REPEAT_DONORS,REPEAT_DONOR_DICT[key2])
            else:
                CMTE_ID_ZIP_DICT[key]=[TRANSACTION_DT,1]
                    
    FILE_OBJ_REPEAT_DONORS.close()
    pass


if __name__ == "__main__":
    main(sys.argv)
