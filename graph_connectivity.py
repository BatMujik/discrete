import sys
import locale

# Set up console encoding
sys.stdout.reconfigure(encoding='utf-8')

# Existing imports
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import random

class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.adj_list = defaultdict(list)

    def add_edge(self, u, v):
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)

    def _dfs(self, v, visited, component):
        visited[v] = True
        component.append(v)
        for neighbor in self.adj_list[v]:
            if not visited[neighbor]:
                self._dfs(neighbor, visited, component)

    def find_connected_components(self):
        visited = {v: False for v in range(self.V)}
        connected_components = []
        for v in range(self.V):
            if not visited[v]:
                component = []
                self._dfs(v, visited, component)
                connected_components.append(component)
        return connected_components

    def is_connected(self):
        return len(self.find_connected_components()) == 1

    def find_bridges(self):
        visited = {v: False for v in range(self.V)}
        discovery_time = {v: float("inf") for v in range(self.V)}
        low_value = {v: float("inf") for v in range(self.V)}
        parent = {v: -1 for v in range(self.V)}
        bridges = []
        time = 0

        def _dfs_bridge(u):
            nonlocal time
            visited[u] = True
            discovery_time[u] = low_value[u] = time
            time += 1
            for v in self.adj_list[u]:
                if not visited[v]:
                    parent[v] = u
                    _dfs_bridge(v)
                    low_value[u] = min(low_value[u], low_value[v])
                    if low_value[v] > discovery_time[u]:
                        bridges.append((u, v))
                elif v != parent[u]:
                    low_value[u] = min(low_value[u], discovery_time[v])

        for i in range(self.V):
            if not visited[i]:
                _dfs_bridge(i)
        return bridges

    def visualize(self):
        G = nx.Graph()
        for u in self.adj_list:
            for v in self.adj_list[u]:
                G.add_edge(u, v)

        components = self.find_connected_components()
        bridges = self.find_bridges()

        pos = nx.kamada_kawai_layout(G)  # Better layout algorithm
        colors = {}
        edge_colors = []

        # Pastel color palette for components
        pastel_colors = [
            "#C9BDF9", "#EAB8B8", '#9999FF', '#FFFF99', 
            "#A2A097", '#99FFFF', '#FFB366', '#99FF66'
        ]

        # Color each component
        for i, component in enumerate(components):
            c = pastel_colors[i % len(pastel_colors)]
            for node in component:
                colors[node] = c

        # Highlight bridges
        for u, v in G.edges():
            if (u, v) in bridges or (v, u) in bridges:
                edge_colors.append("#C8A2CA")  # Bright red for bridges
            else:
                edge_colors.append('#666666')  # Darker grey for normal edges

        node_colors = [colors[n] for n in G.nodes()]

        plt.figure(figsize=(12, 8))
        
        # Draw edge shadows
        nx.draw_networkx_edges(G, pos, edge_color="#A7A7A7", width=6, alpha=0.5)
        
        
        nx.draw_networkx_nodes(G, pos, node_color="#A374AA", node_size=1000, alpha=0.3)
        

        nx.draw(G, pos,
                with_labels=True,
                node_color=node_colors,
                edge_color=edge_colors,
                node_size=3000,
                font_size=12,
                font_weight='bold',
                font_color='black',
                width=2,         
                alpha=0.9)

        plt.title("Գրաֆի վիզուալիզացիա",
                 fontsize=16, pad=20)
        
        plt.tight_layout()
        plt.show()


# Example usage
if __name__ == "__main__":
    try:
        # Example 1: Disconnected graph with multiple components
        print("\nՕրինակ 1: Անկապակցված գրաֆ բազմաթիվ բաղադրիչներով", flush=True)
        g1 = Graph(10)
        g1.add_edge(0, 1)
        g1.add_edge(1, 2)
        g1.add_edge(2, 3)
        g1.add_edge(4, 5)
        g1.add_edge(6, 7)
        g1.add_edge(7, 8)
        g1.add_edge(8, 9)
        
        print("Կապակցված բաղադրիչներ:", g1.find_connected_components())
        print("Կապակցվա՞ծ է:", g1.is_connected())
        print("Կամուրջներ:", g1.find_bridges())
        g1.visualize()

        # Example 2: Connected graph with bridges
        print("\nՕրինակ 2: Կապակցված գրաֆ կամուրջներով", flush=True)
        g2 = Graph(6)
        g2.add_edge(0, 1)
        g2.add_edge(1, 2)
        g2.add_edge(2, 3)
        g2.add_edge(3, 4)
        g2.add_edge(4, 5)
        
        print("Կապակցված բաղադրիչներ:", g2.find_connected_components())
        print("Կապակցվա՞ծ է:", g2.is_connected())
        print("Կամուրջներ:", g2.find_bridges())
        g2.visualize()

        # Example 3: Cyclic graph without bridges
        print("\nՕրինակ 3: Ցիկլային գրաֆ առանց կամուրջների", flush=True)
        g3 = Graph(5)
        g3.add_edge(0, 1)
        g3.add_edge(1, 2)
        g3.add_edge(2, 3)
        g3.add_edge(3, 4)
        g3.add_edge(4, 0)  # Creates a cycle
        
        print("Կապակցված բաղադրիչներ:", g3.find_connected_components())
        print("Կապակցվա՞ծ է:", g3.is_connected())
        print("Կամուրջներ:", g3.find_bridges())
        g3.visualize()
    except UnicodeEncodeError:
        # Fallback to English if console doesn't support Armenian
        print("\nExample 1: Disconnected graph with multiple components")
        g1 = Graph(10)
        g1.add_edge(0, 1)
        g1.add_edge(1, 2)
        g1.add_edge(2, 3)
        g1.add_edge(4, 5)
        g1.add_edge(6, 7)
        g1.add_edge(7, 8)
        g1.add_edge(8, 9)
        
        print("Connected components:", g1.find_connected_components())
        print("Is connected?", g1.is_connected())
        print("Bridges:", g1.find_bridges())
        g1.visualize()

        print("\nExample 2: Connected graph with bridges")
        g2 = Graph(6)
        g2.add_edge(0, 1)
        g2.add_edge(1, 2)
        g2.add_edge(2, 3)
        g2.add_edge(3, 4)
        g2.add_edge(4, 5)
        
        print("Connected components:", g2.find_connected_components())
        print("Is connected?", g2.is_connected())
        print("Bridges:", g2.find_bridges())
        g2.visualize()

        print("\nExample 3: Cyclic graph without bridges")
        g3 = Graph(5)
        g3.add_edge(0, 1)
        g3.add_edge(1, 2)
        g3.add_edge(2, 3)
        g3.add_edge(3, 4)
        g3.add_edge(4, 0)  # Creates a cycle
        
        print("Connected components:", g3.find_connected_components())
        print("Is connected?", g3.is_connected())
        print("Bridges:", g3.find_bridges())
        g3.visualize()
