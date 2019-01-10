#!/usr/bin/env python3
import datetime, calendar
def solve(a,b):
    count = 0
    for year in range(a,b+1):
        for month in range(1,12+1):
            daycount = 0
            for day in range(1,calendar.monthrange(year, month)[1]+1):
                mydate = datetime.datetime(year, month, day)
                if int(mydate.strftime('%w')) in [0,5,6]: # in Sunday, Friday, Saturday
                    daycount+=1
            if daycount>=(5*3): # Five Fridays,Saturdays, Sundays
                count+=1
                if 'startmonth' not in vars():
                    startmonth = month
                endmonth = month 

    return (calendar.month_abbr[startmonth], calendar.month_abbr[endmonth], count)

print(solve(1800,2500))
