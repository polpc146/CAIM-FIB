from igraph import Graph
import matplotlib.pyplot as plt


def task1():
    n = 14
    d = n/4
    probs = [10**(-i/d) for i in range(n, -1, -1)]

    clusteringCoeff = -1
    averageSpath = -1

    listacc = []
    listasp = []

    for i in range(0, len(probs)):
        wsGraph = Graph.Watts_Strogatz(1, 6000, 4, probs[i])
        coef = wsGraph.transitivity_undirected()
        asp = wsGraph.average_path_length()
        if(clusteringCoeff == -1):
            clusteringCoeff = coef
        if(averageSpath == -1):
            averageSpath = asp
        listacc.append(coef/clusteringCoeff)
        listasp.append(asp/averageSpath)

    plt.plot(probs, listacc, 'ys', probs, listasp, 'ro')
    plt.xlabel('Prob')
    plt.xscale('log')
    plt.show()


if __name__ == "__main__":
    task1()
