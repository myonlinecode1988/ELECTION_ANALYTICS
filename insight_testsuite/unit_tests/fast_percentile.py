import math
import matplotlib.pyplot as plt
import numpy as np
import heapq
import random
import datetime
for sim in range(0,10):
    random.seed(sim)
    numlist=random.sample(range(1, 30), 20)+random.sample(range(1, 30), 20);
    OUT=[]
    minheap=[]
    maxheap=[]
    OUT2=[]
    #Lets find 30th Percentile
    start_time = datetime.datetime.now()
    for i in xrange(0,len(numlist)):
        sortedList=sorted(numlist[0:i+1])
        OrdinalRank=math.ceil(30.0/100*(i+1))
        OUT.append(sortedList[int(OrdinalRank-1)]);
        ##print i,OrdinalRank,sortedList[int(OrdinalRank-1)],sortedList
    end_time = datetime.datetime.now()
    duration_percenttile1=(end_time-start_time).total_seconds();
    
        
    
    

    start_time = datetime.datetime.now()
    for i in xrange(0,len(numlist)):
            num = numlist[i]
            if (i==0):
                    zeronum=num
                    #print  num
                    OUT2.append(num)
            if (i==1):
                    firstnum=num
                    #print min(zeronum,firstnum)
                    OUT2.append(min(zeronum,firstnum))
                    heapq.heappush(minheap,max(zeronum,firstnum))#Store larger number
                    heapq.heappush(maxheap,-min(zeronum,firstnum))#store smaller numbers
            if (i>1):
                    #Heap has same size
                    maxheapsize=int(math.ceil(30.0/100*(i+1)));
                    #print "MAXHeap size should be=",maxheapsize,"currently is",len(maxheap),i
                    #print "MINHeap size should be=",i-maxheapsize+1,"currently is",len(minheap)
                    #print "MINHEAP",minheap
                    #print "MAXHEAP",maxheap
    
                    if(len(maxheap)==maxheapsize and len(minheap)<(i-maxheapsize+1)):
                            #print "Balanced Heaps"
                            maxheaptopelement=-1*heapq.heappop(maxheap)
                            minheaptopelement=heapq.heappop(minheap)
                            #print "Balanced:Three nums in question",num,maxheaptopelement,minheaptopelement
                            #Three cases
                            if (num<maxheaptopelement):
                                    heapq.heappush(maxheap,-1*num)
                                    heapq.heappush(minheap,maxheaptopelement)
                                    heapq.heappush(minheap,minheaptopelement)
                                    OUT2.append(-1*(heapq.nsmallest(1,maxheap)[0]))
                            if (num>=maxheaptopelement and num<minheaptopelement):
                                    heapq.heappush(maxheap,-1*maxheaptopelement)
                                    heapq.heappush(minheap,num)
                                    heapq.heappush(minheap,minheaptopelement)
                                    OUT2.append(-1*(heapq.nsmallest(1,maxheap)[0]))
                            if (num>=minheaptopelement):
                                    heapq.heappush(minheap,num)
                                    heapq.heappush(minheap,minheaptopelement)
                                    heapq.heappush(maxheap,-1*maxheaptopelement)
                                    OUT2.append(-1*(heapq.nsmallest(1,maxheap)[0]))
                    else:
                            maxheaptopelement=-1*heapq.heappop(maxheap)
                            minheaptopelement=heapq.heappop(minheap)
                            if (num<maxheaptopelement):
                                    heapq.heappush(maxheap,-1*num)
                                    heapq.heappush(maxheap,-1*maxheaptopelement)
                                    heapq.heappush(minheap,minheaptopelement)
                                    OUT2.append(-1*(heapq.nsmallest(1,maxheap)[0]))
                            if (num>=maxheaptopelement and num<minheaptopelement):
                                    heapq.heappush(maxheap,-1*maxheaptopelement)
                                    heapq.heappush(maxheap,-1*num)
                                    heapq.heappush(minheap,minheaptopelement)
                                    OUT2.append(-1*(heapq.nsmallest(1,maxheap)[0]))
                            if (num>=minheaptopelement):
                                    heapq.heappush(minheap,num)
                                    heapq.heappush(maxheap,-1*maxheaptopelement)
                                    heapq.heappush(maxheap,-1*minheaptopelement)
                                    OUT2.append(-1*(heapq.nsmallest(1,maxheap)[0]))
    end_time = datetime.datetime.now()
    duration_percenttile2=(end_time-start_time).total_seconds();
    if ((OUT==OUT2)==False):
    	print "ERROR:UNIT TEST FAILED.Percentile not evaluated correctly"
        break;
    else:
        print "SUCESS:Percentile Match. Dual-Heap-Percentile implementation is" ,round(duration_percenttile2/duration_percenttile1,2),"times faster than naive implemntation" 
        

    
