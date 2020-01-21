#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SunrieSunset.py: compute the tims of sunrise and sunset for a given day of the
year, at a given location on Earth. Times are provided in UT.

Created on Sun Dec 22 14:29:46 2019

@author: Paul
"""
import matplotlib.pyplot as plt

import AstroEphemerisFunctions.py as ephem

####### CONSTANTS #######
ecc = 0.016713       # Sun's orbital eccentricity 1990.0
m = 282.768422       # Sun's ecliptic longitude at perigee 1990.0
r0 = 149598500.0     # Solar orbit semi-major axis (km)
theta_0 = 0.533128   # Sun's angular diameter at r = r0 (degrees)


####### USER INPUTS #######
date_day = 27.0
date_mon = 'Jul'
date_year = 1988
epoch = 1990


####### MAIN DISPATCHER #######
#JD = ComputeJulianDate(date_mon, date_day, date_year)
#EclipticLon = ComputeEclipticLongAtEpoch(epoch)
#SunLon = ComputeSunLonAtPerigee(epoch)
#ecc = ComputeEarthSunOrbitEccentricity(epoch)

# STEP 1: Convert the Month string to a month number 1-12:
date_mon_num = ephem.GetMonthNumber(date_mon)

# STEP 2: Count the number of days that have elapsed since the start of
# date_year
day_number = ephem.FindDaysSinceYearStart(date_day, date_mon_num, date_year)

# STEP 3: Count number of days since Jan 1st of the epoch year up to the
# date: day, month, year
days_since_epoch = ephem.FindDaysSinceEpoch(epoch, date_year, day_number)

# STEP 4: Compute the mean solar anomaly (in radians)
mean_solar_anomaly = ephem.ComputeMeanSolarAnomaly(epoch, days_since_epoch)

# STEP 5: Solve Kepler's Equation for 
E = ephem.SolveKeplersEquation(mean_solar_anomaly)


