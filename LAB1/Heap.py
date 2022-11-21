"""
.. module:: CountWords
CountWords
*************
:Description: CountWords
    Generates a list with the counts and the words in the 'text' field of the documents in an index
:Authors: bejar

:Version:
:Created on: 04/07/2017 11:58
"""


import csv
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter  # useful for `logit` scale
import math
from scipy.optimize import curve_fit
import argparse



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', default=None, required=True, help='Index')
    parser.add_argument('--n', default=None, required=True, help='Choose output n*')
    args = parser.parse_args()
    n = args.n
    index = args.index
    diff = []
    total = []
    
    for i in range(1,int(n)+1): 
        countFile = index + str(i) + ".csv"
        with open(countFile) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            final = False
            a = 0
            for row in readCSV:
                if(row[0] == "--------------------"):
                    final = True
                elif final == True:
                    total.append(int(row[0])) # cogemos el num total de palabras
                    diff.append(a)
                else:
                    a = a + (int(row[0]))
    

    

    def HeapFunction(x, k, b):
        return k*(x**b)

    popt, pcov = curve_fit(HeapFunction, diff, total, bounds=([0.01, 0.01
                                                               ],[1000000.0, 2.0]))
    plt.xscale('log')
    plt.yscale('log')
    plt.plot(diff, total,"r", label="data")
    plt.plot(diff, HeapFunction(diff, *popt), "b--", label="fit")
    plt.ylabel("different words")
    plt.xlabel("words")

    print(popt)
    plt.show()
