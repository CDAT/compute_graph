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
        for index, operator, step in zip(range(len(operators)), operators, v["derivation"]):
            self.assertEqual("arithmetic", step["attribute_values"]["node_type"])
            self.assertEqual(operator, step["attribute_values"]["operator"])
            if index > 0:
                self.assertEqual(index - 1, step["attribute_values"]["left_value"])
                self.assertEqual("left_value", step["dependent_attributes"][0])

    def test_loadjson(self):
        blob = """{
    "derivation": [
        {
            "dependent_attributes": [],
            "attribute_values": {
                "node_type": "arithmetic",
                "operator": "/",
                "left_value": 11,
                "right_value": 5
            }
        }
    ]
}"""
        obj = compute_graph.loadjson(blob)
        self.assertEqual(obj.derive(), 2)
