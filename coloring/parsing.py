import networkx as nx
def get_input(file_location):
    input_data_file = open(file_location, 'r')
    input_data = ''.join(input_data_file.readlines())
    input_data_file.close()
    return input_data
    
def parse_input(input_data):
    G = nx.Graph()
    lines = input_data.split('\n')
    first_line = lines[0].split()
    edge_count = int(first_line[1])
    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))
    G.add_edges_from(edges)
    return G