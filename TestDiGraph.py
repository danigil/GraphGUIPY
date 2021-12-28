import unittest
from GraphAlgo import GraphAlgo


class MyTestCase(unittest.TestCase):

    def test_v_size(self):
        graph = GraphAlgo()

        graph.load_from_json("A0.json")
        self.assertEqual(graph.get_graph().v_size(), 11)

        graph.load_from_json("A1.json")
        self.assertEqual(graph.get_graph().v_size(), 17)

        graph.load_from_json("A2.json")
        self.assertEqual(graph.get_graph().v_size(), 31)

        graph.load_from_json("A3.json")
        self.assertEqual(graph.get_graph().v_size(), 49)

        graph.load_from_json("A4.json")
        self.assertEqual(graph.get_graph().v_size(), 40)

        graph.load_from_json("A5.json")
        self.assertEqual(graph.get_graph().v_size(), 48)

    def test_e_size(self):
        graph = GraphAlgo()

        graph.load_from_json("A0.json")
        self.assertEqual(graph.get_graph().e_size(), 22)

        graph.load_from_json("A1.json")
        self.assertEqual(graph.get_graph().e_size(), 36)

        graph.load_from_json("A2.json")
        self.assertEqual(graph.get_graph().e_size(), 80)

        graph.load_from_json("A3.json")
        self.assertEqual(graph.get_graph().e_size(), 136)

        graph.load_from_json("A4.json")
        self.assertEqual(graph.get_graph().e_size(), 102)

        graph.load_from_json("A5.json")
        self.assertEqual(graph.get_graph().e_size(), 166)

    def test_get_all_v(self):
        graph = GraphAlgo()
        graph.load_from_json("A0.json")
        d = {0: (35.18753053591606, 32.10378225882353), 1: (35.18958953510896, 32.10785303529412),
             2: (35.19341035835351, 32.10610841680672), 3: (35.197528356739305, 32.1053088),
             4: (35.2016888087167, 32.10601755126051), 5: (35.20582803389831, 32.10625380168067),
             6: (35.20792948668281, 32.10470908739496), 7: (35.20746249717514, 32.10254648739496),
             8: (35.20319591121872, 32.1031462), 9: (35.19597880064568, 32.10154696638656),
             10: (35.18910131880549, 32.103618700840336)}
        self.assertNotEqual(graph.get_graph().get_all_v().values(), d.values())

        vals = graph.get_graph().get_all_v().values()
        dict_of = {}

        for i in vals:
            dict_of[i.get_id()] = i.get_pos()

        self.assertEqual(dict_of, d)

    def test_all_in_edges_of_node(self):
        graph = GraphAlgo()
        graph.load_from_json("A0.json")

        get_g = graph.get_graph()
        di = {1: 1.8884659521433524, 10: 1.1761238717867548}

        self.assertCountEqual(get_g.all_in_edges_of_node(0), di)

    def test_all_out_edges_of_node(self):
        graph = GraphAlgo()
        graph.load_from_json("A0.json")
        di = {1: 1.4004465106761335, 10: 1.4620268165085584}

        self.assertCountEqual(graph.get_graph().all_out_edges_of_node(0), di)

    def test_get_mc(self):
        graph = GraphAlgo()
        graph.load_from_json("A0.json")
        graph.get_graph().add_node(11, (35.19351649233253, 32.1061811092437))

        self.assertEqual(graph.get_graph().get_mc(), 34)

    def test_add_edge(self):
        graph = GraphAlgo()
        graph.load_from_json("A0.json")

        self.assertNotEqual(graph.get_graph().add_edge(0, 2, 1.4195069847291193), False)
        self.assertEqual(graph.get_graph().add_edge(0, 1, 1.4004465106761335), False)

    def test_add_node(self):
        graph = GraphAlgo()
        graph.load_from_json("A0.json")

        self.assertEqual(graph.get_graph().add_node(11, (35.19351649233253, 32.1061811092437)), True)
        self.assertEqual(graph.get_graph().add_node(0, (35.18753053591606, 32.10378225882353)), False)

    def test_remove_node(self):
        graph = GraphAlgo()
        graph.load_from_json("A0.json")

        self.assertEqual(graph.get_graph().remove_node(0), True)

    def test_remove_edge(self):
        graph = GraphAlgo()
        graph.load_from_json("A0.json")

        self.assertEqual(graph.get_graph().remove_edge(0, 1), True)
        self.assertEqual(graph.get_graph().remove_edge(0, 2), False)


def suite():
    suite = unittest.TestSuite()
    suite.addTest('test_v_size')
    suite.addTest('test_e_size')
    suite.addTest('test_get_all_v')
    suite.addTest('test_all_in_edges_of_node')
    suite.addTest('test_all_out_edges_of_node')
    suite.addTest('test_get_mc')
    suite.addTest('test_add_edge')
    suite.addTest('test_add_node')
    suite.addTest('test_remove_node')
    suite.addTest('test_remove_edge')
    return suite


if __name__ == '_main_':
    unittest.main()
