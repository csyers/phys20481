import csv
import math
import matplotlib.pyplot as plt
from numpy import array
import numpy as np
import time

e_start = 50
e_end = 130
# e_end = 160
min_mag = -2.5*math.log(1.0 - 1/3.0, 10)

max_magnitude = 18.225

def norm(mag):
    if mag > max_magnitude:
        return max_magnitude
    else:
        return mag

def t_min(mag, time):
    mindex = mag.index(max(mag))
    return time[mindex]

with open("V1432_AQL_TC_V2.txt") as f:
    reader = csv.reader(f, delimiter=",")
    headers = next(reader, None)
    data = {}
    filtered_data = {}
    filtered_unseen = {}
    for h in headers:
        data[h] = []
        filtered_data[h] = []
        filtered_unseen[h] = []
    for row in reader:
        for h, v in zip(headers,row):
            data[h].append(v)
            if float(row[3]) <= min_mag:
                filtered_data[h].append(v)
            else:
                filtered_unseen[h].append(v)


    # magnitudes - numpy array of all magnitude measurements 
    magnitudes = array([float(i) for i in data["MAG"]])
    fmagnitudes = array([float(i) for i in filtered_data["MAG"]])
    unseen_fmagnitudes = array([float(i) for i in filtered_unseen["MAG"]])

    # xvals - numpy array 1-792 for the x values of the measurements
    xvals = array(list(range(1,len(magnitudes)+1)))

    # time - numpy array for timestamps
    d = array([float(i) for i in data["DATE"]])
    filtered_d = array([float(i) for i in filtered_data["DATE"]])
    unseen_filtered_d = array([float(i) for i in filtered_unseen["DATE"]])

    ut = (d%1-.5)*24
    fut = (filtered_d%1-.5)*24
    unseen_fut = (unseen_filtered_d%1-.5)*24

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

    
    magnitudes = [norm(i) for i in magnitudes]
    unseen_fmagnitudes = [max_magnitude for i in unseen_fmagnitudes]


    # find polyfit
    z1 = np.polyfit(fut[e_start:e_end], fmagnitudes[e_start:e_end], 5)
    p1 = np.poly1d(z1)

    fig2, ax2 = plt.subplots()
    fig2.suptitle("V1432 AQL 10/11/2016",fontsize=20, fontweight='bold')
    ax2.scatter(fut,fmagnitudes, s=10, label="Strongly Detected")
    ax2.scatter(unseen_fut, unseen_fmagnitudes, s=10, c='r', marker="o", label="Weakly Detected")
    ax2.invert_yaxis()
    ax2.plot(fut[e_start:e_end], p1(fut[e_start:e_end]), '-')
    plt.xlabel("Time (UT)")
    plt.ylabel("Magnitude")
    plt.legend(loc='upper left')
    # start, end = ax.get_xlim()
    # ax.xaxis.set_ticks(np.arange(start,end,.2))
    # plt.subplots_adjust(bottom=0.20)

    plt.show()

