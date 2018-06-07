import unittest
import compute_graph


class TestRawValueNode(unittest.TestCase):
    def test_value_checking(self):
        node_str = compute_graph.RawValueNode("string")
        node_int = compute_graph.RawValueNode(1)
        node_float = compute_graph.RawValueNode(3.14159)
        node_list = compute_graph.RawValueNode([1, 2, "hi", 4.5, {"test": "this"}])
        node_dict = compute_graph.RawValueNode({"this": "is", "my": "boomstick"})
        with self.assertRaises(ValueError):
            node_obj = compute_graph.RawValueNode(node_str)

    def test_compute(self):
        values = ["string", 1, 3.14159, [1, 2, "hi", 4.5, {"test": "this"}], {"this": "is", "my": "boomstick"}]
        for v in values:
            n = compute_graph.RawValueNode(v)
            self.assertEqual(v, compute_graph.derive_value(n))
