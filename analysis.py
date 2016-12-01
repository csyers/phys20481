import csv
import matplotlib.pyplot as plt
from numpy import array
import numpy as np

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

    # yerrs - numpy array of the measured magnitude errors
    yerrs = array([float(i) for i in data["MAGERR"]])


    plt.figure()
    plt.errorbar(xvals, magnitudes, yerr= yerrs)
    plt.gca().invert_yaxis()
    plt.show()
