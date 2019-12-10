import numpy
import matplotlib.pyplot

def matching_or_cset(G):
    M = max_matching(G)
    # G is now the residual graph
    # Based on the claim: The set of all nodes in X reachable from s in Gf is a constricted set
    # we can look for nodes of X reachable from s to create our constricted set by using shortest_path
    # nodes of X come first in the matrix 0 to (len(G)/2)-1
    constricted_set = []
    for i in range(1, int(len(G) / 2)):
        path = shortest_path(G, 0, i)
        if path is not None:
            constricted_set.append(i)
    if len(constricted_set) > 0:
        return False
    else:
        return True

def whats_the_capacity(G, s, t):
    return G[s][t];

def shortest_path(G,i,j):
    visited_nodes = set()
    visited_nodes.add(i)
    nodes_to_visit = []
    path = []
    nodes_to_visit.append([i])

    while len(nodes_to_visit) > 0:
        v = nodes_to_visit.pop(0)
        path = v;
        if (v[-1] == j):
            # path found
            return path

        for k in range(0,len(G[1])):
            if ((not(k in visited_nodes)) and (G[v[-1]][k] >= 1)):
                # back pointer to v
                neighbors = list(path)
                neighbors.append(k)
                visited_nodes.add(k)
                nodes_to_visit.append(neighbors)
    return None;

# 9 (a)
# implement an algorithm that computes the maximum flow in a graph G
# Note: you may represent the graph, source, sink, and edge capacities
# however you want. You may also change the inputs to the function below.
def max_flow(G, s, t, returnResidual=False):
    #Find path P from s to t
    max_flow_v = 0
    residual_G = G
    path = shortest_path(G, s, t);
    while path != None:
        min_cap = None
        for i in range(0, len(path)):
            node=path[i]
            if node == t:
                break
            nextnode=path[i+1]
            cap = whats_the_capacity(residual_G,node, nextnode);
            if min_cap == None:
                min_cap = cap
            elif cap < min_cap:
                min_cap = cap

        for i in range(0, len(path)):
            node=path[i];
            if node == t:
                break
            nextnode=path[i+1]
            residual_G[node, nextnode] -= min_cap
            residual_G[node, nextnode] = 0 if residual_G[node, nextnode] < 0 else residual_G[node, nextnode]
            residual_G[nextnode, node] += min_cap

        max_flow_v += min_cap
        path = shortest_path(residual_G, s, t)
    return max_flow_v if returnResidual==False else residual_G

def generate_graph_with_probability(n,p):
    d=n;
    r=n;
    graph = numpy.zeros((d+r+2,d+r+2))
    for x in range(1,d+1):
        graph[0][x] = 1
        for y in range(d+1,d+r+1):
            graph[x][y] = n if numpy.random.random() <= p else 0
    for x in range(d+1,d+r+1):
        graph[x][-1] = 1
    return graph;

def max_matching(G):
    t = len(G)-1
    M =[]
    matching_graph = max_flow(G,0,t,True)
    for u in range(1, t):
        for v in range(1, t):
            if matching_graph[u][v] == 1:
                M.append((v,u))
    return M;

def get_match_prob(n,p):
    matchings = 0
    sample_size = 100
    for i in range(0,sample_size):
        b_graph = generate_graph_with_probability(n,p)
        if matching_or_cset(b_graph):
            matchings += 1
    return (float(matchings) / sample_size)

def create_prob_plot(p):
    n_list = []
    match_prob_list = []
    for n in range(0,101,10):
        if n == 0:
            n = 1
        n_list.append(n)
        match_prob = get_match_prob(n,p)
        match_prob_list.append(match_prob)
    for i in range(0,len(n_list)):
        print(str(n_list[i]) + ": " + str(match_prob_list[i]))
    matplotlib.pyplot.scatter(n_list, match_prob_list)
    plot_title = "Odds of Perfect Matching given Demand Probability p = " + str(p)
    matplotlib.pyplot.title(plot_title)
    matplotlib.pyplot.xlabel('n, Buyer and Seller Set Size')
    matplotlib.pyplot.ylabel('p, Odds of Perfect Match')
    matplotlib.pyplot.savefig('odds_of_matching_30_percent.png')

if __name__ == "__main__":
    # sample_size = 100
    p = 0.3
    create_prob_plot(p)
