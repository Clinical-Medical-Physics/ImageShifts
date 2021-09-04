# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 15:39:59 2020

@author: haywoojr
"""
import os

def getSqlResults(queryString,server,db,uid,pwd):
    #utility to make a sumpl query to the db
    #expect SQL Server driver to be installed
    import pyodbc
    
    # Create connection
    con = pyodbc.connect(driver="{SQL Server}",server=server,database=db,uid=uid,pwd=pwd)
    cur = con.cursor()
    #get list of patients with a new start or boost
    #print(queryString)
    queryResults=cur.execute(queryString)
    #convert to python list
    resultList=[]
    for row in queryResults:
        resultList.append(row)
    #close connection
    con.close()

    return resultList

def getQueryFromFile(directory, filename):
    fullname = os.path.join(directory,filename)
    with open(fullname,'r') as f:
        fileData = f.read()
    
    return fileData
    