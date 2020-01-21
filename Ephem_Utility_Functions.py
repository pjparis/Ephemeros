#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 17:21:40 2019

@author: Paul
"""

import numpy as np


#######  FUNCTION DEFS #######


def ComputeJulianDate(mon, day, year):
    '''
    converts user-supplied day, month, and year to Julian Date/Day
    '''
    month_num = GetMonthNumber(mon)
    if(month_num == 1) or (month_num == 2):
        year = year-1
        month = month_num+12
    else:
        month = month_num

    if year >= 1582:     # Gregorian Calendar
        A = int(year/100)
        B = 2-A+int(A/4)
    else:
        B=0

    if year < 0:         # BC dates
        C = int((365.25*year)-0.75)
    else:
        C = int(365.25*year)

    D = int(30.6001*(month+1))
    
    return(B+C+D+day+1720994.5)
    
    
def ComputeEclipticLongAtEpoch(epoch):
    '''
    Computes the Sun's eclipic longitude from the user-supplied epoch (year)
    -(360*int(Lo/360))
    '''
    T = (ComputeJulianDate('Jan', 0.0, epoch)-2415020.0)/36525
    Lo = 279.6966678+(36000.76892*T)+(0.0003025*T**2)

    # if N is out of range (0-360 degrees) add or subtract 360 until it is
    while(Lo<0.0) or (Lo>360.0):
        if(Lo<0):
            Lo=Lo+360.0
        if(Lo>360.0):
            Lo=Lo-360.0
            
    return(Lo)
                                                                                                                           

def ComputeSunLonAtPerigee(epoch):
    '''
    Computes the Sun's longitude at orbit perigee for a user-supplied
    epoch (year)
    '''
    T = (ComputeJulianDate('Jan', 0.0, epoch)-2415020.0)/36525
    
    return(281.2208444 +1.719175*T + 0.000452778*T**2)
    

def ComputeEarthSunOrbitEccentricity(epoch):
    '''
    Computes the Sun's (well, it's the Earth's actually) orbit eccentricity
    for a user-supplied epoch (year)
    '''
    T = (ComputeJulianDate('Jan', 0.0, epoch)-2415020.0)/36525
    
    return(0.01675104 - 0.0000418*T - 0.000000126*T**2)
    
    
def GetMonthNumber(m):
    '''
    Given the month as an abreviated 3 character string, return to the caller
    the analogous month number (e.g., Jan=1, Feb=2, Mar=3...)
    '''
    month_dict = {'Jan':1, 'Feb':2, 'Mar':3, 'Apr':4, 'May':5, 'Jun':6,
                  'Jul':7, 'Aug':8, 'Sep':9, 'Oct':10, 'Nov':11, 'Dec':12}
    return(month_dict.get(m))
    
    
def IsYearALeapYear(y):
    '''
    determines whether the current year is a leap year and informs the user via
    a boolean reply
    '''
    if(y % 4 == 0):
        return(True)
    else:
        return(False)
        

def FindDaysSinceYearStart(date_day, month_number, year):
    '''
    returns the number of days that have elapsed for the current year from 
    January 1st (mid-night December 31st) up to the current day or the day in 
    which you wish to compute sunrise and set times. The difference between
    leap and ordinary years are accounted for in the reply...
    '''
    days_2_year_start_ord = {1:0, 2:31, 3:59, 4:90, 5:120, 6:151, 7:181, 8:212,
                         9:243, 10:273, 11:304, 12:334}
    days_2_year_start_lep = {1:0, 2:31, 3:60, 4:91, 5:121, 6:152, 7:182, 8:213,
                         9:244, 10:274, 11:305, 12:335}
    
    if IsYearALeapYear(year) == True:
        return(days_2_year_start_lep.get(month_number) + date_day)
    else:
        return(days_2_year_start_ord.get(month_number) + date_day)
    

def FindDaysSinceEpoch_retired(epoch, year, day_number):
    '''
    returns the number of days that have elapsed since the first day of the 
    user-defined epoch. The function computes the number of days by first
    computing the offset between the current year and the user-specified datum
    or epoch year. So, for instance, if the user enters 2020 for the epoch, 
    then offsets provided in the epoch_offsets dictionary are used to find the
    number of days that have elapsed between the epoch and the beginning of
    the current year. This result is then added to the already computed day_
    number to yield, and return the number of days since between the first
    day of the epoch and the day for which you will compute sunrise and set
    times.
    '''
    epoch_offset = {-10:-3653, -9:-3287, -8:-2922, -7:-2557, -6:-2192, -5:-1826,
                    -4:-1461, -3:-1096, -2:-731, -1:-365, 0:0, 1:365, 2:730,
                    3:1096, 4:1461, 5:1826, 6:2191, 7:2557, 8:2922, 9:3287,
                    10:3652}
    epoch_yr_offset = year-epoch
    offset = epoch_offset.get(epoch_yr_offset)

    if offset == None:
        return('Difference between current year and epoch can not be > 10 yrs')
    else:
       return(offset+day_number)


def FindDaysSinceEpoch(epoch, year, day_number):
    '''
    Computes the number days from January 1st of the epoch year (beginning at
    midnight December 30th/January 1st) to midnight at the very beginning of
    the day in which a sunrise and set calc are sought. Leap years handled.
    '''
    y = epoch
    days = 0
    
    while(y != year):
        if(epoch > year):
            y = y-1 
            if(IsYearALeapYear(y)) == True:
                days = days - 366
            else:
                days = days - 365
        
        if(epoch < year):
            if(IsYearALeapYear(y)) == True:
                days = days + 366
            else:
                days = days + 365
            y = y+1

        if(epoch == year):
            y = year
            days = 0
        
    return(days+day_number)


def ComputeMeanSolarAnomaly(epoch, days_since_epoch):
    '''
    '''
    mel = ComputeEclipticLongAtEpoch(epoch)
    lsp = ComputeSunLonAtPerigee(epoch)
    
    N = (360.0/365.242191)*days_since_epoch
   
    # if N is out of range (0-360 degrees) add or subtract 360 until it is
    while(N<0.0) or (N>360.0):
        if(N<0):
            N=N+360.0
        if(N>360.0):
            N=N-360.0
    
    M = N+mel-lsp

    while(M<0) or (M>360.0):
        if(M<0.0):
            M=M+360
        if(M>360.0):
            M=M-360
            
    return((M*np.pi)/180.0)
    

def SolveKeplersEquation(M):
    '''
    '''
    return()
