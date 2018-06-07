import unittest
import json
import compute_graph


class TestSerialize(unittest.TestCase):
    def test_dumpjson(self):
        div = compute_graph.ArithmeticOperation("/", 2.6, 1.3)
        mul = compute_graph.ArithmeticOperation("*", div, 2)
        sqrt = compute_graph.ArithmeticOperation("**", mul, .5)
        eq = compute_graph.ArithmeticOperation("==", sqrt, 2)
        self.assertTrue(eq.derive())
        json_blob = compute_graph.dumpjson(eq)
        v = json.loads(json_blob)
        operators = ["/", "*", "**", "=="]
        for index, operator, cur_step in zip(list(range(len(operators))), operators, v["derivation"]):
            self.assertEqual("arithmetic", cur_step["node_type"])
            self.assertEqual(operator, cur_step["attribute_values"]["operator"])
            if index > 0:
                self.assertEqual(index - 1, cur_step["attribute_values"]["left_value"])
                self.assertEqual("left_value", cur_step["dependent_attributes"][0])

    def test_loadjson(self):
        blob = """{
    "derivation": [
        {
            "dependent_attributes": [],
            "attribute_values": {
                "operator": "/",
                "left_value": 11,
                "right_value": 5
            },
            "node_type": "arithmetic",
            "node_params": {
                "operator": "Operator used for data transform",
                "left_value": "Left-hand side of a binary operator",
                "right_value": "Right-hand side of a binary operator"
            }
        },
        {
            "dependent_attributes": ["left_value"],
            "attribute_values": {
                "operator": "*",
                "left_value": 0,
                "right_value": 12
            },
            "node_type": "arithmetic",
            "node_params": {
                "operator": "Operator used for data transform",
                "left_value": "Left-hand side of a binary operator",
                "right_value": "Right-hand side of a binary operator"
            }
        }
    ]
}"""
        obj = compute_graph.loadjson(blob)
        self.assertEqual(obj.derive(), 24)
