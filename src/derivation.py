__computation_registry__ = {}


def register_computation(node_type):
    """
    Decorator that registers handlers for a given node_type.
    """
    def register(f):
        __computation_registry__[node_type] = f
        return f

    return register


def compute(node_type, attributes):
    compute_func = __computation_registry__[node_type]
    return compute_func(attributes)


def derive_value(node):
    v = node.__cache__()
    if v is not None:
        return v
    attributes = {}
    deps = []

    for a, v in node.__attrs__.iteritems():
        if a in node.__deps__:
            attributes[a] = v.derive()
        else:
            attributes[a] = v
    v = compute(node.node_type, attributes)
    node.cache(v)
    return v
