import csv
import matplotlib.pyplot as plt
from numpy import array
with open("V1432_AQL_TC_V2.txt") as f:
    reader = csv.reader(f)
    headers = reader.next()
    data = {}
    for h in headers:
        data[h] = []
    for row in reader:
        for h, v in zip(headers,row):
            data[h].append(v)
    
    magnitudes = array(data["MAG"])

    plt.plot(magnitudes)
    plt.gca().invert_yaxis()
    plt.show()
