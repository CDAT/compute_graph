from .node import ComputeNode
from .derivation import register_computation

NODE_TYPE = "arithmetic"

unary_operators = ["-", "~", "not"]
binary_operators = ["+", "-", "^", "/", ">>", "<<", "%", "*", "**", "|", "&", ">", "<", ">=", "<=", "!=", "=="]


@register_computation(NODE_TYPE)
def compute(attributes):
    op = attributes["operator"]
    if "value" in attributes:
        val = attributes["value"]
        if op == "-":
            return -val
        if op == "~":
            return ~val
        if op == "not":
            return not val
        raise ValueError("Expected '%s' to be a unary operator due to presence of 'value' attribute. Operator not found." % op)
    left = attributes["left_value"]
    right = attributes["right_value"]
    if op == "+":
        return left + right
    if op == "-":
        return left - right
    if op == "^":
        return left ^ right
    if op == "/":
        return left / right
    if op == ">>":
        return left >> right
    if op == "<<":
        return left << right
    if op == "%":
        return left % right
    if op == "*":
        return left * right
    if op == "**":
        return left ** right
    if op == "|":
        return left | right
    if op == "&":
        return left & right
    if op == "+=":
        left += right
        return left
    if op == "-=":
        left -= right
        return left
    if op == "^=":
        left ^= right
        return left
    if op == "/=":
        left /= right
        return left
    if op == ">>=":
        left >>= right
        return left
    if op == "<<=":
        left <<= right
        return left
    if op == "%=":
        left %= right
        return left
    if op == "*=":
        left *= right
        return left
    if op == "**=":
        left **= right
        return left
    if op == "|=":
        left |= right
        return left
    if op == "&=":
        left &= right
        return left
    if op == ">":
        return left > right
    if op == "<":
        return left < right
    if op == ">=":
        return left >= right
    if op == "<=":
        return left <= right
    if op == "!=":
        return left != right
    if op == "==":
        return left == right
    raise ValueError("Operator '%s' not found." % op)


class ArithmeticOperation(ComputeNode):
    def __init__(self, operator, *values):
        super(ArithmeticOperation, self).__init__()

        self.node_type = NODE_TYPE
        self.node_params = {
            "value": "Value to perform unary operators upon",
            "left_value": "Left-hand side of a binary operator",
            "right_value": "Right-hand side of a binary operator",
            "operator": "Operator used for data transform"
        }

        if operator not in unary_operators and operator not in binary_operators:
            raise ValueError("Operator '%s' not recognized." % operator)

        self.operator = operator
        if len(values) == 0:
            raise ValueError("No values provided for arithmetic operation %s." % operator)
        if len(values) == 1:
            if self.operator not in unary_operators:
                raise ValueError("Only one value provided for binary operator %s." % operator)
            del self.node_params["left_value"]
            del self.node_params["right_value"]
            self.value = values[0]
        elif len(values) == 2:
            if self.operator not in binary_operators:
                raise ValueError("Too many values provided for unary operator %s." % operator)
            del self.node_params["value"]
            self.left_value, self.right_value = values
        else:
            raise ValueError("Too many values provided for operation %s." % operator)
