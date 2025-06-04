from collections import defaultdict

class Graph:
    def __init__(self, vertices):
        self.V = vertices  # Վերցերի քանակը
        self.adj_list = defaultdict(list)  # Կիցության ցուցակ (Adjacency list) ներկայացում

    def add_edge(self, u, v):
        # Ավելացնել չուղղորդված կող u և v գագաթների միջև
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)

    def _dfs(self, v, visited, component):
        # Օժանդակ ֆունկցիա՝ խորության առաջին որոնման (DFS) համար
        visited[v] = True
        component.append(v)
        for neighbor in self.adj_list[v]:
            if not visited[neighbor]:
                self._dfs(neighbor, visited, component)

    def find_connected_components(self):
        # Գտնել բոլոր կապակցված բաղադրիչները
        visited = {v: False for v in range(self.V)}
        connected_components = []

        for v in range(self.V):
            if not visited[v]:
                component = []
                self._dfs(v, visited, component)
                connected_components.append(component)

        return connected_components

    def is_connected(self):
        # Ստուգել՝ արդյոք գրաֆը կապակցվա՞ծ է (միայն մեկ կապակցված բաղադրիչ)
        connected_components = self.find_connected_components()
        return len(connected_components) == 1

    def find_bridges(self):
        """Գտնել բոլոր կամուրջները (կտրող կողերը) գրաֆում։"""
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

                    # Ստուգել՝ արդյոք v-ով սկսվող ենթածառը կապ ունի u-ի նախնիներից մեկի հետ
                    low_value[u] = min(low_value[u], low_value[v])

                    # Եթե v-ից հասանելի ամենացածր գագաթը ավելի բարձր է, քան u-ի հայտնաբերման ժամանակը, ապա u-v-ը կամուրջ է
                    if low_value[v] > discovery_time[u]:
                        bridges.append((u, v))
                
                elif v != parent[u]:
                    # Թարմացնել u-ի low արժեքը՝ նախնիների համար
                    low_value[u] = min(low_value[u], discovery_time[v])

        for i in range(self.V):
            if not visited[i]:
                _dfs_bridge(i)
                
        return bridges


# Օրինակ օգտագործում
if __name__ == "__main__":
    # Օրինակ 1: Պարզ կապակցված գրաֆ
    print("Օրինակ 1: Պարզ կապակցված գրաֆ")
    g1 = Graph(4)
    g1.add_edge(0, 1)
    g1.add_edge(1, 2)
    g1.add_edge(2, 3)

    print("Կապակցված բաղադրիչներ:", g1.find_connected_components())
    print("Գրաֆը կապակցված է? :", g1.is_connected())
    print("Կամուրջներ:", g1.find_bridges())
    print()

    # Օրինակ 2: Գրաֆ կամուրջներով
    print("Օրինակ 2: Գրաֆ կամուրջներով")
    g2 = Graph(5)
    g2.add_edge(0, 1)
    g2.add_edge(1, 2)
    g2.add_edge(2, 0) 
    g2.add_edge(1, 3)
    g2.add_edge(3, 4)

    print("Կապակցված բաղադրիչներ:", g2.find_connected_components())
    print("Գրաֆը կապակցված է? :", g2.is_connected())
    print("Կամուրջներ:", g2.find_bridges())
