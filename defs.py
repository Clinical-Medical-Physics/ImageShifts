# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 18:34:16 2020

@author: haywoojr
"""

import datetime

#generator for fridays in the year
def allFridays(year):
    d=datetime.date(year,1,1)
    d += datetime.timedelta(days = 4 - d.weekday())
    while d.year == year:
        yield d
        d += datetime.timedelta(days = 7)

def startEndDates(year,n):
    strtendList=[]
    for d in allFridays(year):
        if d <= n:
            strtendList.append((d-datetime.timedelta(days=4),d))
    return strtendList
