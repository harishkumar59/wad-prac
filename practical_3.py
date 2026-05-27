#pip install networkx numpy scipy

#create virtual environment 


import networkx as nx

# Create Directed Graph
G = nx.DiGraph()

# Add pages (nodes)
G.add_nodes_from(['page1', 'page2', 'page3', 'page4'])

# Add links between pages (edges)
G.add_edges_from([
    ('page1', 'page2'),
    ('page1', 'page3'),
    ('page2', 'page3'),
    ('page3', 'page1'),
    ('page3', 'page4'),
    ('page4', 'page2')
])

# Calculate PageRank
pr = nx.pagerank(G, alpha=0.85)

# Random Walk probabilities
rw = nx.pagerank(G)

# Print Random Walk probabilities
print("Random Walk Probabilities:")
print("Page1 =", rw['page1'])
print("Page2 =", rw['page2'])
print("Page3 =", rw['page3'])
print("Page4 =", rw['page4'])

# Print PageRank values
print("\nPageRank Values:")
print("Page1 =", pr['page1'])
print("Page2 =", pr['page2'])
print("Page3 =", pr['page3'])
print("Page4 =", pr['page4'])
