import csv
import matplotlib.pyplot as plt
import math
from scipy.optimize import curve_fit

import argparse

# ya hemos hecho el reverse y el isalpha en el countwords


parser = argparse.ArgumentParser()
parser.add_argument('--countFile', default=None, required=True, help='Count Words File')
args = parser.parse_args()

countFile = args.countFile

values = [] # guardamos la frecuencia

with open(countFile) as csvfile:
        readCSV = csv.reader(csvfile, delimiter=',')
        for row in readCSV:
            if(row[0] == "--------------------"):
                break
            else:
                values.append(int(row[0]))

def ZipFunc(x, a, b, c):
        return c/((x+b)**a)

values = values[: 500]
xList = [(x+1) for x in range(len(values))] # rango
popt, pcov = curve_fit(ZipFunc, xList, values, bounds=([0.5, -499.0, 0.0],[1.5, 100000.0, 2000000.0]))

plt.xscale('log')
plt.yscale('log')
plt.plot(xList, values,"r", label="data")
plt.plot(xList, ZipFunc(xList, *popt), "b--", label="fit")
plt.ylabel("frequency")
plt.xlabel("rank")

print(popt)
plt.show()
