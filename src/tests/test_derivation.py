import unittest
import compute_graph


class TestDerivation(unittest.TestCase):

    def test_derive(self):
        # Simple fibonacci derivation
        last_v = compute_graph.RawValueNode(1)
        v = compute_graph.RawValueNode(1)
        for _ in range(200):
            last_v, v = v, compute_graph.ArithmeticOperation("+", v, last_v)
        self.assertEqual(v.derive(), 734544867157818093234908902110449296423351)

    def test_compute_registry(self):
        node_type = "my_test_type"
        node_type_2 = "my_other_type"

        @compute_graph.register_computation(node_type)
        @compute_graph.register_computation(node_type_2)
        def do_compute(attributes):
            self.assertEqual(attributes["node_type"], node_type)

        n = compute_graph.ComputeNode(node_type=node_type)
        n.derive()

        # Make sure that registering a new handler overrides existing ones
        n2 = compute_graph.ComputeNode(node_type=node_type_2)

        @compute_graph.register_computation(node_type_2)
        def do_other_compute(attributes):
            self.assertEqual(attributes["node_type"], node_type_2)

        n2.derive()
