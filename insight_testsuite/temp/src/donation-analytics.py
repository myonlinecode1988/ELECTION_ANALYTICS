import sys
import os.path
import pandas as pd



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


#Create MERGE_REPEATDON_INPUTDATAput file repeat_donors.txt
FILE_OBJ_REPEAT_DONORS=open(REPEAT_DONORS_FILE,"w+");


#Read itcont.txt and store in data frame.
# Importing the dataset
dataset=pd.read_csv(ITCONTFILE,header=None,sep='|',names=["CMTE_ID","AMNDT_IND",
                                                          "RPT_TP","TRANSACTION_PGI","IMAGE_NUM","TRANSACTION_TP",
                                                          "ENTITY_TP","NAME","CITY","STATE","ZIP_CODE","EMPLOYER",
                                                          "OCCUPATION","TRANSACTION_DT","TRANSACTION_AMT","OTHER_ID",
                                                          "TRAN_ID","FILE_NUM","MEMO_CD","MEMO_TEXT","SUB_ID"],dtype={'ZIP_CODE':str,'TRANSACTION_DT':str});

# Subset the dataset based on relevant column name
inputdata = dataset[['CMTE_ID','NAME','ZIP_CODE','TRANSACTION_DT','TRANSACTION_AMT','OTHER_ID']]


###PREPPROCESSING 
#Make ZIP_CODE 5 characters
inputdata.is_copy = False
inputdata.loc[:,'ZIP_CODE'] = inputdata["ZIP_CODE"].str[:5]

#Use datatime format for dates
inputdata.loc[:,'TRANSACTION_DT'] =  pd.to_datetime(inputdata['TRANSACTION_DT'], format='%m%d%Y')
inputdata.loc[:,'TRANSACTION_DT'] = inputdata['TRANSACTION_DT'].apply(lambda x: x.year)

#Remove the line where OTHER_ID is present because it means an organization donated
#Meta data description:https://classic.fec.gov/finance/disclosure/metadata/DataDictionaryContributionsbyIndividuals.shtml

inputdata = inputdata[pd.isna(inputdata['OTHER_ID'])]

#Remove OTHER_ID now 
inputdata=inputdata.drop(columns=['OTHER_ID'])


#Aggregate counts based on zip code and NAME
Count_By_ZIP_NAME=inputdata.groupby(['NAME','ZIP_CODE']).size().reset_index(name='Counts')

#Detect Repeat donors by subsetting for Counts>1
RepeatDonorDF = Count_By_ZIP_NAME[Count_By_ZIP_NAME['Counts']>1];
RepeatDonorDF=RepeatDonorDF.drop(columns=['Counts'])

#Merge Repeat Donors and inputdata
MERGE_REPEATDON_INPUTDATA=pd.merge(RepeatDonorDF, inputdata, on=['NAME','ZIP_CODE'])
#Remove NAME column
MERGE_REPEATDON_INPUTDATA=MERGE_REPEATDON_INPUTDATA.drop(columns=['NAME'])

#We query based on CMTE_ID and year(TRANSACTION_DT)
#HARDCODE#
INPUT_YEAR=2018
INPUT_CMTE_ID='C00384516'
PERCENTILE=0.3

FINAL=MERGE_REPEATDON_INPUTDATA.loc[(MERGE_REPEATDON_INPUTDATA.CMTE_ID==INPUT_CMTE_ID) & (MERGE_REPEATDON_INPUTDATA.TRANSACTION_DT==INPUT_YEAR)]
#Sort by Transanction amount
FINAL=FINAL.sort_values('TRANSACTION_AMT')
FINAL['RUNNING_TOTAL']=FINAL['TRANSACTION_AMT'].cumsum()
FINAL = FINAL.reset_index(drop=True)
FINAL['RUNNING_COUNT']=pd.Series(range(1,len(FINAL.index)+1))
FINAL['RUNNING_PERCENTILE']=FINAL['TRANSACTION_AMT'].quantile(q=0.3,interpolation="lower")

#CHANGE ORDER FOR DISPLAY
DISPLAY=FINAL[['CMTE_ID','ZIP_CODE','TRANSACTION_DT','RUNNING_PERCENTILE','RUNNING_TOTAL','RUNNING_COUNT']]
DISPLAY.to_csv(REPEAT_DONORS_FILE, sep='|',header=None,index=False)
FILE_OBJ_REPEAT_DONORS.close()


