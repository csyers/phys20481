import csv
import math
import matplotlib.pyplot as plt
from numpy import array
import numpy as np
import time

with open("V1432_AQL_TC_V2.txt") as f:
    reader = csv.reader(f)
    headers = reader.next()
    data = {}
    for h in headers:
        data[h] = []
    for row in reader:
        for h, v in zip(headers,row):
            data[h].append(v)

    # magnitudes - numpy array of all magnitude measurements 
    magnitudes = array([float(i) for i in data["MAG"]])

    # xvals - numpy array 1-792 for the x values of the measurements
    xvals = array(list(range(1,len(magnitudes)+1)))

    # time - numpy array for timestamps
    d = array([float(i) for i in data["DATE"]])

    ut = (d%1-.5)*24

    #time_strings = [str(math.floor(t)) + ":" + str(t%1*60)for t in ut]
    
    times = []

    for t in ut:
        hours = str(int(math.floor(t)))
        minute_float = t%1*60
        minutes = str(int(math.floor(minute_float)))
        seconds = str(int(minute_float%1*60))
        times.append(hours + ":" + minutes + ":" + seconds)

    time_objects = []

    for t in times:
        time_objects.append(time.strptime(t,"%H:%M:%S"))    
    
    time_strings = []
    for t in time_objects:
        time_strings.append(time.strftime('%H:%M:%S',t))
    # yerrs - numpy array of the measured magnitude errors
    yerrs = array([float(i) for i in data["MAGERR"]])

    # fit a polynomial with degree 11
    z = np.polyfit(xvals, magnitudes, 11)

    # get the scalar function of thepolynomial
    p = np.poly1d(z)
    #model = LomScargleFast().fit(t, magnitudes, yerrs)
    #periods, power = model.periodogram_auto(myquist_factor=100)

    #fig, ax = plt.subplots()
    #ax.plot(periods,power)
    #ax.set(xlim=(02,1.4),ylim=(0,0.8),xlabel = 'period(days)',ylabel='Lomb-Scargle Power');

    # plot everythin
    fig, ax = plt.subplots()
    #plt.errorbar(xvals, magnitudes, yerr= yerrs)
    ax.scatter(ut,magnitudes)
    ax.invert_yaxis()
    plt.xlabel("Time (UT)")
    plt.ylabel("Magnitude")
    #plt.plot( xvals, p(xvals), '-')
    start, end = ax.get_xlim()
    #plt.xticks(ut,time_strings, rotation='vertical')
    ax.xaxis.set_ticks(np.arange(start,end,.2))
    plt.subplots_adjust(bottom=0.20)
    #ax.xaxis.set_major_formatter(matplotlib.ticker.FormatStrFormatter())
    #plot.set_xlabel("Time (UT)")
    #:wqplot.set_ylabel("Magnitude")
    plt.show()

