import sys
import os.path
import heapq
import math

#Header names and index numbers
COLNAMES = {
    'CMTE_ID':0,
    'NAME':7,
    'ZIP_CODE':10,
    'TRANSACTION_DT':13,
    'TRANSACTION_AMT':14,
    'OTHER_ID':15
} 



class Percentile:
    """
    This is a Percentile class. 
    We create two heaps `MinHeap` and `MaxHeap`. Let's say we are evaluating for 30
    percentile.  `MaxHeap` would contain elements smaller than or equal to 30
    percentile value.  `MinHeap` would contain all the elements greater than 30
    percentile value.  Now we insert values according to the size of the heap for
    that iteration.
    """
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
            #Calculate the size of Maxheap
            maxheapsize=int(math.ceil(self.percentile/100.0*(self.count+1)));
            
            if(len(self.maxheap)==maxheapsize and len(self.minheap)<(self.count-maxheapsize+1)):
                    #Update MinHeap based on location of MinHeap top-element vs. new-number vs. MaxHeap top-element
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
                    #Update MaxHeap based on location of MinHeap top-element vs. new-number vs. MaxHeap top-element
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
    #Wrtie to repeat_donors.txt
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
        #Sanity checks for percentile value and file
        try:
            PERCENTILE = float(c[0]);
        except ValueError:
            print "ERROR:Use Correct value for percentile.txt"
            exit(1)
        if (not((PERCENTILE>0) and (PERCENTILE<=100))):
            print "ERROR:Use value between (0,100] for percentile"
            exit(1)
  
    with open(ITCONTFILE) as f:
        REPEAT_DONOR_DICT={} ## REPEAT DONOR dictionary
        NAME_ZIP_to_YEAR_COUNT={} #NAME and ZIP code dictionary used to identify donor.
        for line in f:
            row = line.rstrip('\n')
            row = row.split('|')
            #Checking Data Specifications based  on FEC specifications
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
            
            #Remove rows with OTHER_ID having finite values
            if (len(row[COLNAMES['OTHER_ID']])!=0):
                continue
            
            #Truncate ZIP_CODE to 5 digits
            ZIP_CODE=row[COLNAMES['ZIP_CODE']][0:5]
            
            CMTE_ID=row[COLNAMES['CMTE_ID']]
            NAME=row[COLNAMES['NAME']]
            
            #Converting TRANSACTION_DT to year format
            TRANSACTION_DT=int(row[COLNAMES['TRANSACTION_DT']][4:10])
            
            TRANSACTION_AMT=float(row[COLNAMES['TRANSACTION_AMT']])
            
            #Creating a key with NAME and ZIP_CODE to search in NAME_ZIP_to_YEAR_COUNT hashtable
            NAME_ZIP_CODE_KEY=(NAME,ZIP_CODE)
            if NAME_ZIP_CODE_KEY in NAME_ZIP_to_YEAR_COUNT:
                #Increment Counter if found in NAME_ZIP_to_YEAR_COUNT hastable
                NAME_ZIP_to_YEAR_COUNT[NAME_ZIP_CODE_KEY][1]=NAME_ZIP_to_YEAR_COUNT[NAME_ZIP_CODE_KEY][1]+1
                
                #Reset repeat_donor if the repeat donor appears for an older calendar year
                if (TRANSACTION_DT<NAME_ZIP_to_YEAR_COUNT[NAME_ZIP_CODE_KEY][0]):
                    NAME_ZIP_to_YEAR_COUNT[NAME_ZIP_CODE_KEY]=[TRANSACTION_DT,1]

                #If NAME and ZIP_CODE key has appeared earlier we have detected a repeat donor 
                if (NAME_ZIP_to_YEAR_COUNT[NAME_ZIP_CODE_KEY][1]>1):
                    CMTE_ID_ZIP_CODE_KEY=(CMTE_ID,ZIP_CODE)
                    
                    #Search based on CMTE_D and ZIP_CODE in REPEAT DONOR dictionary
                    if CMTE_ID_ZIP_CODE_KEY in REPEAT_DONOR_DICT:
                        #Update Percentile object and REPEAT_DONOR_DICT entries
                        
                        REPEAT_DONOR_DICT[CMTE_ID_ZIP_CODE_KEY][6]=REPEAT_DONOR_DICT[CMTE_ID_ZIP_CODE_KEY][6]+TRANSACTION_AMT
                        REPEAT_DONOR_DICT[CMTE_ID_ZIP_CODE_KEY][5]=REPEAT_DONOR_DICT[CMTE_ID_ZIP_CODE_KEY][5]+1
                        returned_percentile=round(REPEAT_DONOR_DICT[CMTE_ID_ZIP_CODE_KEY][3].updateheaps(TRANSACTION_AMT))
                        REPEAT_DONOR_DICT[CMTE_ID_ZIP_CODE_KEY][4]=returned_percentile
                        dictprinter(FILE_OBJ_REPEAT_DONORS,REPEAT_DONOR_DICT[CMTE_ID_ZIP_CODE_KEY])                               
                    else:
                        #Create a new Percentile object and insert CMTE_ID,ZIP_CODE,
                        #TRANSACTION_DT,pointer-to-percentile-object,returned-value-of-percentile,
                        #count,running total donation in REPEAT_DONOR_DICT based on the key.
                        
                        x = Percentile(PERCENTILE)
                        returned_percentile=round(x.updateheaps(TRANSACTION_AMT))
                        REPEAT_DONOR_DICT[CMTE_ID_ZIP_CODE_KEY]=[CMTE_ID,ZIP_CODE,TRANSACTION_DT,x,returned_percentile,1,TRANSACTION_AMT]
                        dictprinter(FILE_OBJ_REPEAT_DONORS,REPEAT_DONOR_DICT[CMTE_ID_ZIP_CODE_KEY])
            else:
                NAME_ZIP_to_YEAR_COUNT[NAME_ZIP_CODE_KEY]=[TRANSACTION_DT,1]
                    
    FILE_OBJ_REPEAT_DONORS.close()
    pass


if __name__ == "__main__":
    main(sys.argv)
