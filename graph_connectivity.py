from collections import defaultdict

class Graph:
    def __init__(self, vertices):
        self.V = vertices  # Number of vertices
        self.adj_list = defaultdict(list)  # Adjacency list representation

    def add_edge(self, u, v):
        # Add an undirected edge between u and v
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)

    def _dfs(self, v, visited, component):
        # Helper function for DFS traversal
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
        # Check if the graph is connected (only one connected component)
        connected_components = self.find_connected_components()
        return len(connected_components) == 1

    def find_bridges(self):
        """Find all bridges (cut edges) in the graph."""
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

                    # Check if subtree rooted with v has a connection to one of the ancestors of u
                    low_value[u] = min(low_value[u], low_value[v])

                    # If the lowest vertex reachable from subtree under v is below u in DFS tree, then u-v is a bridge
                    if low_value[v] > discovery_time[u]:
                        bridges.append((u, v))
                
                elif v != parent[u]:
                    # Update low value of u for parent function calls
                    low_value[u] = min(low_value[u], discovery_time[v])

        for i in range(self.V):
            if not visited[i]:
                _dfs_bridge(i)
                
        return bridges


# Example usage
if __name__ == "__main__":
    # Example 1: A simple connected graph
    print("Example 1: A simple connected graph")
    g1 = Graph(4)
    g1.add_edge(0, 1)
    g1.add_edge(1, 2)
    g1.add_edge(2, 3)

    print("Connected Components:", g1.find_connected_components())
    print("Is the graph connected?", g1.is_connected())
    print("Bridges:", g1.find_bridges())
    print()

    # Example 2: A graph with bridges
    print("Example 2: A graph with bridges")
    g2 = Graph(5)
    g2.add_edge(0, 1)
    g2.add_edge(1, 2)
    g2.add_edge(2, 0) 
    g2.add_edge(1, 3)
    g2.add_edge(3, 4)

    print("Connected Components:", g2.find_connected_components())
    print("Is the graph connected?", g2.is_connected())
    print("Bridges:", g2.find_bridges())
