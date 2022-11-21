#!/usr/bin/python

from collections import namedtuple
import time
import sys
import numpy as np

class Edge:
    def __init__ (self, origin=None):
        self.origin = origin # write appropriate value
        self.weight = 1 # write appropriate value

    def __repr__(self):
        return "edge: {0} {1}".format(self.origin, self.weight)
        
    ## write rest of code that you need for this class

class Airport:
    def __init__ (self, iden=None, name=None):
        self.code = iden
        self.name = name
        self.routes = []
        self.routeHash = dict()
        self.outweight = 0   # write appropriate value
        self.index = 0

    def __repr__(self):
        return f"{self.code}\t{self.name}"

    def addRoute(self, origin):
        if origin.code in self.routeHash:
            e = self.routeHash[origin.code]
            e.weight += 1
        else:
            e = Edge(origin.code)
            self.routes.append(e)
            self.routeHash[origin.code] = e


airportList = [] # list of Airport
airportHash = dict() # hash key IATA code -> Airport
pageRank = []
airpWOoutweight = 0


def readAirports(fd):
    print("Reading Airport file from {0}".format(fd))
    airportsTxt = open(fd, "r");
    cont = 0
    for line in airportsTxt.readlines():
        a = Airport()
        try:
            temp = line.split(',')
            if len(temp[4]) != 5 : # 3 letras + comillas
                raise Exception('not an IATA code')
            a.name=temp[1][1:-1] + ", " + temp[3][1:-1]
            a.code=temp[4][1:-1]
            a.index = cont
        except Exception as inst:
            pass
        else:
            cont += 1
            airportList.append(a)
            airportHash[a.code] = a
    airportsTxt.close()
    print(f"There were {cont} Airports with IATA code")




def readRoutes(fd):
    print("Reading Routes file from {fd}")
    # write your code
    routesTxt = open(fd, "r");
    cont = 0
    for line in routesTxt.readlines():
        try:
            temp = line.split(',')
            if len(temp[2]) != 3 or len(temp[4]) != 3:
                raise Exception('not an IATA code')
            if (not temp[2] in airportHash or not temp[4] in airportHash):
                raise Exception('IATA code does not exist!')
            origin = airportHash[temp[2]]
            destiny = airportHash[temp[4]] # aeropuerto
            destiny.addRoute(origin)
            origin.outweight += 1


        except Exception as inst:
            pass
        else:
            cont += 1
    routesTxt.close()
    print(f"There were {cont} Edges with IATA code")


def sumatorio(P, airp):
    a = airportList[airp]
    suma = 0
    for j in a.routes:
        aorig = airportHash[j.origin] #tenemos el aeropuerto, sabemos su numero
        suma += P[aorig.index]*j.weight/aorig.outweight
    return suma


def checkPandQ(P, Q):
    return (abs(sum(P)-sum(Q)) < 10**(-18))


def computePageRanks():
    n = len(airportList)
    P = [1/n]*n #n veces escrito 1/n
    L = 0.9
    i = 0
    equal = False
    # aquí añadimos el peso proporcional a los nodos desconectados
    weightAirpWOOutweight = 1/n
    numOut = L*airpWOoutweight/n
    while(not equal):
        Q = [0]*n
        for airp in range(0, n):
            Q[airp] = L*sumatorio(P, airp)+(1-L)/n+weightAirpWOOutweight*numOut
        # aquí actualizamos el peso proporcional a los nodos desconectados
        weightAirpWOOutweight = (1-L)/n + weightAirpWOOutweight*numOut
        equal = checkPandQ(P, Q)
        P = Q
        i += 1
    global pageRank
    for airp in range(0, n):
        pageRank.append((P[airp], airportList[airp].name))

    return i


def outputPageRanks():
    # write your code
    sorter = lambda x: (x[0])
    for p in sorted(pageRank, key=sorter, reverse=True):
        print(p)


def main(argv=None):
    readAirports("airports.txt")
    readRoutes("routes.txt")
    global airpWOoutweight
    airpWOoutweight = len(list(filter(lambda n: n.outweight == 0, airportList)))
    time1 = time.time()
    iterations = computePageRanks()
    time2 = time.time()
    outputPageRanks()
    print("#Iterations:", iterations)
    print("Time of computePageRanks():", time2-time1)


if __name__ == "__main__":
    sys.exit(main())
