# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 17:49:42 2020

@author: haywoojr
"""
import json
from pathlib import Path
import os
import binascii
import pandas as pd

#for importing the config file
path = Path(__file__).parent / "config.json"
#print(path)
with path.open() as config_file:
    config_data = json.load(config_file)

#get root directory
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SQL_DIR_PATH = os.path.join(ROOT_DIR,'SQL_scripts')

#for importing the needed modules
from ImageShifts import getImageShifts
from sqler import sqljob

import datetime

#some definitions
#get the patient list
def getPatientList(options, sql_dir_path):
    queryFile=sqljob.getQueryFromFile(sql_dir_path, 'getPatientList.sql')
    queryString=queryFile.format(strtdate=options['strtdate'],enddate=options['enddate'],
                                 activityName=options['activityName'],machineId=options['machineId'])
    patientList=sqljob.getSqlResults(queryString, options['server'], options['db'], 
                                     options['uid'], options['pwd'])
    return patientList

#get patient plan#
def getPatientPlan(options,sql_dir_path):
    queryFile=sqljob.getQueryFromFile(sql_dir_path, 'getPatientPlan.sql')
    queryString=queryFile.format(strtdate=options['strtdate'],enddate=options['enddate'],
                                 patientId=options['patientId'])
    planList=sqljob.getSqlResults(queryString, options['server'], options['db'], 
                                     options['uid'], options['pwd'])
    return planList

#get images list
def getImagesList(options,sql_dir_path):
    queryFile=sqljob.getQueryFromFile(sql_dir_path, 'getPatientImages.sql')
    queryString=queryFile.format(strtdate=options['strtdate'],enddate=options['enddate'],
                                 patientId=options['patientId'])
    ImageList=sqljob.getSqlResults(queryString, options['server'], options['db'], 
                                     options['uid'], options['pwd'])
    return ImageList

def doTheWork(patientList,strtdate,enddate,server,db,username,password,returnList):
    
    for row in patientList:
        ptId=row[0]
        options={'strtdate':strtdate,'enddate':enddate,'patientId':ptId,
              'server':server,'db':db,'uid':username,'pwd':password}
        ptPlan=getPatientPlan(options,SQL_DIR_PATH)
        #need to go through all of these but just choose the first one for now 
        #as most CBCT patients only have one plan
        iso_X=ptPlan[0][8]
        iso_Y=ptPlan[0][9]
        iso_Z=ptPlan[0][10]
        course=ptPlan[0][3]
        planName=ptPlan[0][2]
        #get the images for this patient for this day
        ptImages=getImagesList(options,SQL_DIR_PATH)
        if(len(ptImages)):
            imgDate=datetime.datetime.strptime(ptImages[0][15], '%Y-%m-%d %H:%M:%S.%f0')
            date=imgDate.strftime('%m/%d/%y')
            #return ptImages
            #need to do more to make sure these images are for this plan but as
            #above most CBST patients only have one plan and one CBCT

            # query returns binary value here not hex representation code expects hex
            transHex=binascii.b2a_hex(ptImages[0][5])
            #return transHex
            #print(transHex)
            vrt_shift,lng_shift,lat_shift,ipitch,iroll,irot=getImageShifts.getImageShifts(
                transHex,iso_X,iso_Y,iso_Z)
            #convert to cm
            vrt_shift/=10.0
            lng_shift/=10.0
            lat_shift/=10.0
            print('{strtdate}, {ptId}, {course:16}, {plan:16}, VRT {vrt:6.1f} '
                  'LNG {lng:6.1f} LAT {lat:6.1f} PITCH {pitch:6.1f} ROLL {roll:6.1f} '
                  'ROT {rot:6.1f}'.format(
                  vrt=vrt_shift,lng=lng_shift,lat=lat_shift,pitch=ipitch,roll=iroll,
                  rot=irot,strtdate=date,ptId=ptId,course=course,plan=planName))
            returnList.append([date,ptId,course,planName,vrt_shift,lng_shift,
                              lat_shift,ipitch,iroll,irot])
    #return shiftList
        #else patient didn't really have 3D Imaging but was scheduled as such

#set the daterange
# n=datetime.datetime(2020,12,1)
# strtdate=n.strftime("%m/%d/%y")

# n=datetime.datetime(2020,12,2)
# enddate=n.strftime("%m/%d/%y")

mysql=config_data['mysql']
server=mysql['server']
db=mysql['db']
uid=mysql['username']
pwd=mysql['password']
# plan_options={'strtdate':strtdate,'enddate':enddate,'patientId':'PATIDNUM',
#               'server':server,'db':db,'uid':uid,'pwd':pwd}

# img_options={'strtdate':strtdate,'enddate':enddate,'patientId':'PATIDNUM',
#              'server':server,'db':db,'uid':uid,'pwd':pwd}
#array to hold data
shiftList=[]
#set date range with business day range from pandas
dateRange=pd.bdate_range(start='11/5/2020', end='11/6/2020')
for d in dateRange:  
    strtdate=d
    enddate=d+pd.Timedelta(1,unit='D')
    pt_options={'strtdate':strtdate,'enddate':enddate,'activityName':'Daily Treatment - CBCT',
         'machineId':'Clinac iX','server':server,'db':db,'uid':uid,'pwd':pwd}

    ptList=getPatientList(pt_options,SQL_DIR_PATH)
  
    doTheWork(ptList, strtdate, enddate, server, db, uid, pwd,shiftList)

fields=['Date','PatientId','Course','PlanName','VRT','LNG','LAT','PITCH','ROLL','ROT']

# with open('H:/PythonModules/Shifts.csv','w') as f:
#     for row in shiftList:
#         writeString="""{strtdate},{ptId},{course:16},{plan:16},{vrt:6.1f},{lng:6.1f},{lat:6.1f},{pitch:6.1f},{roll:6.1f},{rot:6.1f}\n""".format(
#                   vrt=row[4],lng=row[5],lat=row[6],pitch=row[7],roll=row[8],
#                   rot=row[9],strtdate=row[0],ptId=row[1],course=row[2].replace(',',''),plan=row[3].replace(',',''))
#         f.write(writeString)