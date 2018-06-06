import json
from .node import ComputeNode


def dumpjson(node):
    """
    Takes in a node, returns the JSON string of the derivation tree.
    """
    sorted_nodes = node.dependencies() + [node]
    serialized_nodes = []
    for n in sorted_nodes:
        s = {
            "dependent_attributes": list(n.__deps__),
            "attribute_values": {},
            "node_params": n.node_params,
            "node_type": n.node_type
        }
        for d in n.__deps__:
            dep = n.__attrs__[d]
            i = sorted_nodes.index(dep)
            s["attribute_values"][d] = i
        for a in n.__attrs__:
            if a not in n.__deps__:
                s["attribute_values"][a] = n.__attrs__[a]
        serialized_nodes.append(s)

    return json.dumps({"derivation": serialized_nodes})


def loadjson(jsonstring):
    """
    Takes in a JSON string, returns the root node of the derivation tree.
    """
    serialization = json.loads(jsonstring)
    nodes = []
    for _n in serialization["derivation"]:
        node = ComputeNode()
        deps = _n["dependent_attributes"]
        for a, v in _n["attribute_values"].iteritems():
            if a in deps:
                v = nodes[v]
            setattr(node, a, v)
        node.node_params = _n["node_params"]
        node.node_type = _n["node_type"]
        nodes.append(node)
    return nodes[-1]
