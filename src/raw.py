import json
from .node import ComputeNode
from .derivation import register_computation


@register_computation("raw")
def compute(attributes):
    return attributes["value"]


class RawValueNode(ComputeNode):
    def __init__(self, value):
        super(RawValueNode, self).__init__()
        self.node_type = "raw"
        self.node_params = {
            "value": "Raw (JSON-compatible) value provided by this node."
        }
        try:
            json.dumps(value)
        except:
            raise ValueError("RawValueNode only supports JSON compatible values; %s is not." % type(value))
        self.value = value
