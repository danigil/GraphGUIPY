from copy import deepcopy
from GraphInterface import GraphInterface


class Node:
    def __init__(self, node_id, pos):
        self._node_id = node_id
        self._pos = pos
        self._dist = 0
        self._edges_out = {}
        self._edges_in = {}

    def __repr__(self):
        return str(self._node_id) + ": |edges out| " + str(len(self._edges_out)) + " |edges in| " + str(
            len(self._edges_in))

    def __lt__(self, other):
        return self._dist < other.get_dist()

    def get_edges_out(self) -> dict:
        return self._edges_out

    def get_edges_in(self) -> dict:
        return self._edges_in

    def get_pos(self) -> tuple:
        return self._pos

    def set_pos(self,tup):
        self._pos=tup

    def get_id(self) -> int:
        return self._node_id

    def get_dist(self) -> float:
        return self._dist

    def set_dist(self, dist: float):
        self._dist = dist


class Edge:
    def __init__(self, src, dest, weight):
        self._src = src
        self._dest = dest
        self._weight = weight

    def __repr__(self):
        return str(self._weight)

    def get_src(self) -> int:
        return self._src

    def get_dest(self) -> int:
        return self._dest

    def get_weight(self) -> int:
        return self._weight


class DiGraph(GraphInterface):
    def __init__(self):
        self._nodes = {}
        self._mc_counter = 0
        self.min_pos = [0,0]
        self.max_pos = [700,700]

    def __repr__(self):
        return "Graph: |V|=" + str(self.v_size()) + " , |E|=" + str(self.e_size())

    def v_size(self) -> int:
        return len(self._nodes)

    def e_size(self) -> int:
        count = 0
        for node_key in self._nodes:
            current_node_edges = self._nodes[node_key].get_edges_out()
            for edge_key in current_node_edges:
                count += 1
        return count

    def get_all_v(self) -> dict:
        return self._nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        return self._nodes[id1].get_edges_in()

    def all_out_edges_of_node(self, id1: int) -> dict:
        return self._nodes[id1].get_edges_out()

    def get_mc(self) -> int:
        return self._mc_counter

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        if id1 in self._nodes and id2 in self._nodes:
            if id2 not in self._nodes[id1].get_edges_out():
                self._nodes[id1].get_edges_out().update({id2: Edge(id1, id2, weight)})
                self._nodes[id2].get_edges_in().update({id1: Edge(id1, id2, weight)})
                self._mc_counter += 1
                return True
            else:
                return False
        else:
            return False

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        if node_id not in self._nodes:
            if pos is not None:
                pos_x = pos[0]
                pos_y = pos[1]
                if pos_x < self.min_pos[0] or self.v_size() == 0:
                    self.min_pos[0] = pos_x
                if pos_y < self.min_pos[1] or self.v_size() == 0:
                    self.min_pos[1] = pos_y

                if pos_x > self.max_pos[0] or self.v_size() == 0:
                    self.max_pos[0] = pos_x
                if pos_y > self.max_pos[1] or self.v_size() == 0:
                    self.max_pos[1] = pos_y
            self._nodes.update({node_id: Node(node_id, pos)})
            self._mc_counter += 1
            return True
        else:
            return False

    def remove_node(self, node_id: int) -> bool:

        if node_id in self._nodes:
            for node_key in self._nodes:
                if node_id != node_key:
                    current_node_out = self._nodes[node_key].get_edges_out()
                    current_node_out_copy = deepcopy(current_node_out)
                    for edge_key in current_node_out_copy:
                        if node_id == edge_key:
                            self.remove_edge(node_key, node_id)

                    current_node_in = self._nodes[node_key].get_edges_in()
                    current_node_in_copy = deepcopy(current_node_in)
                    for edge_key in current_node_in_copy:
                        if node_id == edge_key:
                            self.remove_edge(node_id, node_key)

            self._nodes.pop(node_id)
            self._mc_counter += 1
            return True
        else:
            return False

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        if node_id1 in self._nodes and node_id2 in self._nodes and node_id2 in self._nodes[node_id1].get_edges_out():
            self._nodes[node_id1].get_edges_out().pop(node_id2)
            self._nodes[node_id2].get_edges_in().pop(node_id1)
            self._mc_counter += 1
            return True
        else:
            return False

    def is_exist_edge(self, src: int, dest: int):
        return dest in self._nodes[src].get_edges_out()

    def is_exist_node(self, node_id: int) -> bool:
        return node_id in self._nodes

    def get_edge(self, src: int, dest: int) -> Edge:
        if src in self._nodes and dest in self._nodes and self.is_exist_edge(src, dest):
            return self._nodes[src].get_edges_out()[dest]
        else:
            return None

    def get_node(self, node_id: int) -> Node:
        return self._nodes[node_id]

