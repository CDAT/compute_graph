import json
from .node import ComputeNode


def dumpjson(node):
    """
    Takes in a node, returns the JSON string of the derivation tree.
    """
    sorted_nodes = node.dependencies()
    serialized_nodes = []
    for n in node.dependencies():
        s = {
            "dependent_attributes": list(n.__deps__),
            "attribute_values": {}
        }
        for d in n.__deps__:
            dep = n.__attrs__[d]
            i = sorted_nodes.index(dep)
            s["attribute_values"][d] = i
        for a in n.__attrs__:
            if a not in n.__deps__:
                s["attribute_values"][a] = n.__attrs__[a]
        serialized_nodes.append(s)
    return json.dumps({"derivation": s})


def loadjson(jsonstring):
    """
    Takes in a JSON string, returns the root node of the derivation tree.
    """
    serialization = json.loads(jsonstring)
    nodes = []
    for n in serialization["derivation"]:
        node = ComputeNode()
        deps = n["dependent_attributes"]
        for a, v in n["attribute_values"].iteritems():
            if a in deps:
                v = nodes[v]
            setattr(node, a, v)
        nodes.append(node)
    return nodes[-1]
