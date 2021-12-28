import unittest
from DiGraph import DiGraph
from GraphAlgo import GraphAlgo


class MyTestCase(unittest.TestCase):

    def test_get_graph(self):
        graph1 = GraphAlgo()
        graph1.load_from_json("A0.json")
        graph2 = GraphAlgo()
        graph2.load_from_json("A1.json")

        self.assertNotEqual(graph1.get_graph(), graph2.get_graph())

    def test_load_from_json(self):
        graph = GraphAlgo()
        graph.load_from_json("A0.json")

        graph1 = GraphAlgo()
        graph1.load_from_json("A1.json")

        self.assertNotEqual(graph, graph1)

    def test_save_to_json(self):
        graph = GraphAlgo()

        graph.load_from_json("A0.json")
        graph.save_to_json("testing.json")
        graph.load_from_json("testing.json")

        get1 = graph.get_digraph()
        get2 = graph.get_digraph()

        self.assertCountEqual(get1.get_all_v(), get2.get_all_v())
        self.assertCountEqual(get1.get_all_v(), get2.get_all_v())

    def test_centerPoint(self):
        graph = GraphAlgo()

        graph.load_from_json("A0.json")
        self.assertCountEqual(graph.centerPoint(), (7, 6.806805834715163))

        graph.load_from_json("A1.json")
        self.assertCountEqual(graph.centerPoint(), (8, 9.925289024973141))

        graph.load_from_json("A2.json")
        self.assertCountEqual(graph.centerPoint(), (0, 7.819910602212574))

        graph.load_from_json("A4.json")
        self.assertCountEqual(graph.centerPoint(), (6, 8.071366078651435))

        graph.load_from_json("A5.json")
        self.assertCountEqual(graph.centerPoint(), (40, 9.291743173960954))

    def test_TSP(self):
        g = DiGraph()  # creates an empty directed graph
        for n in range(5):
            g.add_node(n)
        g.add_edge(0, 1, 1)
        g.add_edge(0, 4, 5)
        g.add_edge(1, 0, 1.1)
        g.add_edge(1, 2, 1.3)
        g.add_edge(1, 3, 1.9)
        g.add_edge(2, 3, 1.1)
        g.add_edge(3, 4, 2.1)
        g.add_edge(4, 2, .5)

        g_algo = GraphAlgo(g)

        print(g_algo.centerPoint())
        print(g_algo.TSP([1, 2, 4]))

    def test_shortest_path(self):
        graph = GraphAlgo()
        graph.load_from_json("A1.json")
        correct = [15, 16, 0, 1]
        wrong = [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
        correct_w = 1.8726071511162605 + 1.4418017651347552 + 1.232037506070033
        wrong_w = 1.635946027210021 + 1.3207562671517605 + 1.823489852982211 + 1.0666986438224981 + 1.3784147388591739 \
                  + 1.5815006562559664 + 1.9855087252581762 + 1.2817370911337442 + 1.5786081900467002 \
                  + 1.4964304236123005 + 1.5855912911662344 + 1.8418222744214585 + 1.440561778177153 \
                  + 1.5784991011275615

        self.assertEqual(graph.shortest_path(15, 1), (correct_w, correct))
        self.assertNotEqual(graph.shortest_path(15, 1), (wrong_w, wrong))


if __name__ == '_main_':
    unittest.main()
