import math
from collections import deque


def _build_adjacency_list(nodes, edges):
    adj = {name: [] for name in nodes}
    for edge in edges:
        adj[edge['from']].append(edge['to'])
    return adj


def _topological_sort(graph):
    in_degree = {u: 0 for u in graph}
    for u in graph:
        for v in graph[u]:
            in_degree[v] += 1
    queue = deque([u for u in graph if in_degree[u] == 0])
    sorted_order = []
    while queue:
        u = queue.popleft()
        sorted_order.append(u)
        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0: queue.append(v)
    if len(sorted_order) == len(graph):
        return sorted_order
    else:
        raise ValueError("Graph contains a cycle.")


def _line_intersection(p1, p2, p3, p4):
    def orientation(p, q, r):
        val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
        if val == 0: return 0
        return 1 if val > 0 else 2

    o1, o2, o3, o4 = orientation(p1, p2, p3), orientation(p1, p2, p4), orientation(p3, p4, p1), orientation(p3, p4, p2)
    if o1 != o2 and o3 != o4: return True
    return False


class ForceDirectedLayout:
    def __init__(self, nodes, edges, height, node_size=(64, 64), iterations=300,
                 k_repel=60000, k_attract=0.3, k_edge_repel=15, ideal_length=120, min_x_spacing=60):
        self._nodes = nodes
        self._edges = edges
        self._node_size = node_size
        self._iterations = iterations
        self._k_repel, self._k_attract, self._k_edge_repel = k_repel, k_attract, k_edge_repel
        self._ideal_length, self._min_x_spacing = ideal_length, min_x_spacing

        adj_list = _build_adjacency_list(nodes, edges)
        self._sorted_nodes = _topological_sort(adj_list)
        self._parents = {u: [] for u in nodes}
        for edge in edges: self._parents[edge['to']].append(edge['from'])

        self._positions = {}
        ranks = self._calculate_ranks()
        nodes_by_rank = {}
        for node, rank in ranks.items():
            if rank not in nodes_by_rank: nodes_by_rank[rank] = []
            nodes_by_rank[rank].append(node)
        for rank, nodes_in_rank in nodes_by_rank.items():
            x_pos = rank * (self._node_size[0] + self._min_x_spacing + 20) + 70
            num_in_rank = len(nodes_in_rank)
            if num_in_rank == 1:
                y_positions = [height / 2]
            else:
                total_span = (num_in_rank - 1) * (self._node_size[1] + 50)
                start_offset = -total_span / 2.0
                y_positions = [height / 2 + start_offset + i * (self._node_size[1] + 50) for i in range(num_in_rank)]
            for i, node in enumerate(nodes_in_rank):
                existing_nodes_position = nodes[node]['position'] if 'position' in nodes[node] else [0, 0]
                if existing_nodes_position == [0 , 0]:
                    self._positions[node] = [x_pos, y_positions[i]]
                else:
                    self._positions[node] = [existing_nodes_position[0], existing_nodes_position[1]]

    def _calculate_ranks(self):
        ranks = {node: 0 for node in self._nodes}
        for node in self._sorted_nodes:
            if self._parents[node]:
                ranks[node] = max(ranks[p] for p in self._parents[node]) + 1
        return ranks

    def max_iterations(self):
        return self._iterations

    def positions(self):
        return self._positions

    def get_port_position(self, node_name, port_type, port_index):
        center_x, center_y = self._positions[node_name]
        node_width, node_height = self._node_size
        if port_type == 'input':
            num_ports, x_pos = self._nodes[node_name]['inputs'], center_x - node_width / 2
        else:
            num_ports, x_pos = self._nodes[node_name]['outputs'], center_x + node_width / 2
        if num_ports <= 1: return [x_pos, center_y]
        vertical_span = node_height * 0.8
        spacing = vertical_span / (num_ports - 1)
        start_offset = -vertical_span / 2.0
        y_pos = center_y + start_offset + port_index * spacing
        return [x_pos, y_pos]

    def _calculate_forces(self):
        forces = {node: [0.0, 0.0] for node in self._nodes}
        node_list = list(self._nodes.keys())
        for i in range(len(node_list)):
            for j in range(i + 1, len(node_list)):
                node1, node2 = node_list[i], node_list[j]
                dx, dy = self._positions[node1][0] - self._positions[node2][0], self._positions[node1][1] - self._positions[node2][
                    1]
                distance = math.sqrt(dx ** 2 + dy ** 2) + 0.0001
                fy = (dy / distance) * (self._k_repel / (distance ** 2))
                forces[node1][1] += fy
                forces[node2][1] -= fy
        for edge in self._edges:
            pos1 = self.get_port_position(edge['from'], 'output', edge['from_port'])
            pos2 = self.get_port_position(edge['to'], 'input', edge['to_port'])
            dx, dy = pos1[0] - pos2[0], pos1[1] - pos2[1]
            distance = math.sqrt(dx ** 2 + dy ** 2) + 0.0001
            fy_attr = (dy / distance) * (self._k_attract * (distance - self._ideal_length))
            forces[edge['from']][1] -= fy_attr
            forces[edge['to']][1] += fy_attr
        if self._k_edge_repel > 0:
            for i in range(len(self._edges)):
                for j in range(i + 1, len(self._edges)):
                    edge1, edge2 = self._edges[i], self._edges[j]
                    if len({edge1['from'], edge1['to'], edge2['from'], edge2['to']}) < 4: continue
                    e1_p1 = self.get_port_position(edge1['from'], 'output', edge1['from_port'])
                    e1_p2 = self.get_port_position(edge1['to'], 'input', edge1['to_port'])
                    e2_p1 = self.get_port_position(edge2['from'], 'output', edge2['from_port'])
                    e2_p2 = self.get_port_position(edge2['to'], 'input', edge2['to_port'])
                    if _line_intersection(e1_p1, e1_p2, e2_p1, e2_p2):
                        mid1_y, mid2_y = (e1_p1[1] + e1_p2[1]) / 2, (e2_p1[1] + e2_p2[1]) / 2
                        force_y = self._k_edge_repel if mid1_y < mid2_y else -self._k_edge_repel
                        forces[edge1['from']][1] -= force_y
                        forces[edge1['to']][1] -= force_y
                        forces[edge2['from']][1] += force_y
                        forces[edge2['to']][1] += force_y
        return forces

    def update_layout(self, damping):
        forces = self._calculate_forces()
        for node in self._sorted_nodes:
            _, fy = forces[node]
            self._positions[node][1] += fy * damping
            max_parent_x = 0
            if self._parents[node]:
                max_parent_x = max(self._positions[p][0] for p in self._parents[node])
            self._positions[node][0] = max_parent_x + self._node_size[0] + self._min_x_spacing
