import json
from typing import List

from GraphAlgoInterface import GraphAlgoInterface
from DiGraph import DiGraph, Node
from GraphInterface import GraphInterface
from queue import PriorityQueue
from GUI import GUI


class Stack:
    def __init__(self):
        self._stack = []

    def add(self, data):
        self._stack.append(data)

    def peek(self):
        return self._stack[-1]

    def pop(self):
        return self._stack.pop(-1)

    def is_empty(self):
        return len(self._stack) == 0


def perms(source: List[int], connected_nodes: List[bool]):
    if len(source) == 0:
        return []

    if len(source) == 1:
        return [source]

    ret = []

    for i in range(len(source)):
        current = source[i]
        if connected_nodes[i] is False and len(source) == len(connected_nodes):
            continue
        rec = source[:i] + source[i + 1:]

        for p in perms(rec, connected_nodes):
            ret.append([current] + p)

    return ret


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, graph=DiGraph()):
        self._graph = graph

    def get_graph(self) -> GraphInterface:
        return self._graph

    def get_digraph(self) -> DiGraph:
        return self._graph

    def load_from_json(self, file_name: str) -> bool:
        self._graph = DiGraph()

        try:
            with open(file_name, 'r') as file:
                load = json.load(file)
                nodes_list = load["Nodes"]
                for node_dict in nodes_list:
                    if "pos" in node_dict:
                        pos = node_dict["pos"]
                        self._graph.add_node(node_dict["id"], (float(pos.split(",")[0]), float(pos.split(",")[1])))
                    else:
                        self._graph.add_node(node_dict["id"])

                edges_list = load["Edges"]
                for edge_dict in edges_list:
                    self._graph.add_edge(edge_dict["src"], edge_dict["dest"], edge_dict["w"])

            return True
        except OSError:
            print("ERROR: couldn't open file.")
            return False

    def save_to_json(self, file_name: str) -> bool:
        edges = []

        nodes = []
        v = self._graph.get_all_v()
        for node_key in v:
            current_node = v[node_key]
            current_pos = current_node.get_pos()

            current_edges = self._graph.all_out_edges_of_node(node_key)
            for edge in current_edges.values():
                edges.append({"src": edge.get_src(), "w": edge.get_weight(), "dest": edge.get_dest()})

            if current_pos is not None:
                nodes.append(
                    {"pos": str(current_pos[0]) + "," + str(current_pos[1]) + ",0.0", "id": current_node.get_id()})
            else:
                nodes.append({"id": current_node.get_id()})

        json_dict = {"Edges": edges, "Nodes": nodes}
        json_str = json.dumps(json_dict, indent=3)
        try:
            with open(file_name, "w") as file:
                file.write(json_str)
            return True
        except OSError:
            print("ERROR: couldn't write file.")
            return True

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        ret = self.dijkstra(id1, id2)
        return self._graph.get_node(id2).get_dist(), ret

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        ret = []
        floyd = self.floyd()
        connected_nodes = []
        for i in range(len(node_lst)):
            connected_nodes.append(True)

        for i in range(len(node_lst)):
            for j in range(len(node_lst)):
                if floyd[node_lst[i]][node_lst[j]] == float('inf'):
                    connected_nodes[i] = False
                    break
        chosen_dist = float('inf')
        chosen_perm = []
        ran = range(len(node_lst) - 1)
        all_perms = perms(node_lst, connected_nodes)
        for perm_index in range(len(all_perms)):
            current_dist = 0
            for i in ran:
                current_dist += floyd[all_perms[perm_index][i]][all_perms[perm_index][i + 1]]
            if current_dist < chosen_dist:
                chosen_dist = current_dist
                chosen_perm = all_perms[perm_index]

        for i in ran:
            path=self.shortest_path(chosen_perm[i], chosen_perm[i + 1])[1]
            if len(ret)>0 and ret[-1]== path[0]:
                ret.pop(-1)
            ret+=path

        return (ret, chosen_dist)

    def centerPoint(self) -> (int, float):
        if self._graph.v_size() < 1:
            return -1, float('inf')

        floyd = self.floyd()
        for i in range(self._graph.v_size()):
            for j in range(self._graph.v_size()):
                if floyd[i][j] == float('inf'):
                    return None, float('inf')

        eccentricity = []
        for i in range(self._graph.v_size()):
            eccentricity.append(float('-inf'))

        for i in range(self._graph.v_size()):
            for j in range(self._graph.v_size()):
                if i != j and floyd[i][j] > eccentricity[i] and floyd[i][j] != float('inf'):
                    eccentricity[i] = floyd[i][j]

        min_index = 0
        for i in range(self._graph.v_size()):
            if eccentricity[i] < eccentricity[min_index]:
                min_index = i

        return min_index, eccentricity[min_index]

    def plot_graph(self) -> None:
        gu = GUI(self)

    def dijkstra(self, src: int, dest: int):
        self._graph.get_node(src).set_dist(0)  # dist[source] <- 0

        pq = PriorityQueue()  # create vertex priority queue Q
        prev = {}

        node_dict = self._graph.get_all_v()

        for node_key in node_dict:
            current_node = self._graph.get_node(node_key)
            if node_key != src:
                current_node.set_dist(float('inf'))

            prev[node_key]=None

            pq.put((current_node.get_dist(), current_node))

        while not pq.empty():
            u_tuple = pq.get()
            u = u_tuple[1]

            u_neighbours = self._graph.all_out_edges_of_node(u.get_id())
            for neighbour_key in u_neighbours:
                v = self._graph.get_node(neighbour_key)
                alt = u.get_dist() + self._graph.get_edge(u.get_id(), v.get_id()).get_weight()
                if alt < v.get_dist():
                    v.set_dist(alt)
                    prev[neighbour_key] = u
                    pq.put((alt, v))

        st = Stack()
        current_target = self._graph.get_node(dest)
        if prev[dest] is not None or src == current_target.get_id():
            while current_target is not None:
                st.add(current_target)
                current_target = prev[current_target.get_id()]

        node_list = []
        while not st.is_empty():
            node_list.append(st.pop().get_id())

        return node_list

    def floyd(self):
        ret = []
        for i in range(self._graph.v_size()):
            ar = []
            for j in range(self._graph.v_size()):
                ar.append(float('inf'))

            ret.append(ar)

        nodes = self._graph.get_all_v()
        for node_key in nodes:
            current_edges = nodes[node_key].get_edges_out()
            for edge_key in current_edges:
                ret[node_key][edge_key] = current_edges[edge_key].get_weight()

        for i in range(self._graph.v_size()):
            ret[i][i] = 0

        for i in range(self._graph.v_size()):
            for j in range(self._graph.v_size()):
                for k in range(self._graph.v_size()):
                    if ret[j][k] > ret[j][i] + ret[i][k]:
                        ret[j][k] = ret[j][i] + ret[i][k]

        return ret
