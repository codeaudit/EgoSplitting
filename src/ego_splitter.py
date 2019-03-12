import networkx as nx
from tqdm import tqdm
import community

class EgoNetSplitter(object):

    def __init__(self, graph, resolution):
        self.graph = graph
        self.resolution = resolution

    def create_egonet(self, node):
        ego_net_minus_ego = self.graph.subgraph(self.graph.neighbors(node))
        components = {i: nodes for i, nodes in enumerate(nx.connected_components(ego_net_minus_ego))}
        new_mapping = {}
        personalities = []
        for k, v in components.items():
            personalities.append(self.index)
            for other_node in v:
                new_mapping[other_node] = self.index 
            self.index = self.index +1
        self.components[node] = new_mapping
        self.personalities[node] = personalities

    def create_egonets(self):
        self.components = {}
        self.personalities = {}
        self.index = 0
        for node in tqdm(self.graph.nodes()):
            self.create_egonet(node)

    def map_personalities(self):
        self.personality_map = {persona: node for node in self.graph.nodes() for persona in self.personalities[node]}


    def create_persona_graph(self):
        self.persona_graph_edges = [(self.components[edge[0]][edge[1]], self.components[edge[1]][edge[0]]) for edge in tqdm(self.graph.edges())]
        self.persona_graph = nx.from_edgelist(self.persona_graph_edges)

    def create_partitions(self):
        self.partitions = community.best_partition(self.persona_graph, resolution=self.resolution)
        self.overlapping_partitions = {node: [] for node in self.graph.nodes()}
        for node, membership in self.partitions.items():
            self.overlapping_partitions[self.personality_map[node]].append(membership)

