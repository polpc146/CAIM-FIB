from igraph import Graph
from igraph import plot
from IPython import display
from numpy import histogram, max
import matplotlib.pyplot as plt


def task2():
    g = Graph(directed=False)
    g = g.Load('./edges.txt', format='edgelist', directed=False)
    """
    print("edges: ", len(g.es()))
    print("nodes: ", len(g.vs()))
    print("diameter: ", g.diameter())
    print("transitivity: ", g.transitivity_undirected())
    print("degree distribution: ", g.degree_distribution())
    print("degree: ", g.degree())
    plot(g, layout = g.layout_kamada_kawai())
    prs = g.pagerank();
    prs = [prs[i]*500 for i in range(0,len(prs))]
    plot(g, vertex_size = prs)
    """
    com = g.community_edge_betweenness()
    comC = com.as_clustering()
    comSizes = comC.sizes()
    print(comSizes)
    print("Size of largest community:", max(comSizes))

    plt.hist(comSizes, rwidth = 0.2, color="red")
    plt.ylabel('Number of communities')
    plt.xlabel('Community size')
    plt.show()

    plot(comC, layout = g.layout_kamada_kawai(), orientation='bottom-top')
    print ('Clusters:', com.optimal_count)


if __name__ == "__main__":
    task2()
