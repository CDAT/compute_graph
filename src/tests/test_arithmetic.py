import unittest
import compute_graph


class TestArithmeticOperationNode(unittest.TestCase):
    def test_value_counts(self):
        # Test 0 values
        with self.assertRaises(ValueError):
            operation_node = compute_graph.ArithmeticOperation("-")

        # Test 1 value for binary operators
        with self.assertRaises(ValueError):
            operation_node = compute_graph.ArithmeticOperation("|", 1)

        # Test 2 values for unary operator
        with self.assertRaises(ValueError):
            operation_node = compute_graph.ArithmeticOperation("not", 1, 2)

        # Test more than 2 values for binary operator
        with self.assertRaises(ValueError):
            operation_node = compute_graph.ArithmeticOperation(">=", 1, 2, 3)

        # Test more than 2 values for unary operator
        with self.assertRaises(ValueError):
            operation_node = compute_graph.ArithmeticOperation("not", 1, 2, 3)

        # Test 2 values for binary
        operation_node = compute_graph.ArithmeticOperation(">=", 2, 3)
        # Test 1 value for unary
        operation_node = compute_graph.ArithmeticOperation("not", False)

    def test_int_computations(self):
        left_value, right_value = 1, 2
        unary_results = [-1, -2, False]
        binary_results = [3, -1, 3, 0, 0, 4, 1, 2, 1, 3, 0, False, True, False, True, True, False]
        self.assertEqual(len(unary_results), len(compute_graph.arithmetic.unary_operators))

        for op, result in zip(compute_graph.arithmetic.unary_operators, unary_results):
            node = compute_graph.ArithmeticOperation(op, left_value)
            self.assertEqual(node.derive(), result)

        self.assertEqual(len(binary_results), len(compute_graph.arithmetic.binary_operators))
        for op, result in zip(compute_graph.arithmetic.binary_operators, binary_results):
            node = compute_graph.ArithmeticOperation(op, left_value, right_value)
            self.assertEqual(node.derive(), result)
