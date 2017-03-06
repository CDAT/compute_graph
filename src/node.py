import weakref
import derivation


class ComputeNode(object):

    __slots__ = ('__deps__', '__cache__', '__attrs__', '__deps__', 'node_params', 'node_type')

    def __init__(self, **attrs):
        self.__attrs__ = attrs
        self.__deps__ = set()
        for a, v in attrs.iteritems():
            if isNode(v):
                self.__deps__.add(a)
        self.__cache__ = lambda: None
        self.node_params = {}
        self.node_type = 'compute_node'

    def __setattr__(self, name, value):
        if name in self.__slots__:
            super(ComputeNode, self).__setattr__(name, value)
        else:
            if isinstance(value, (list, tuple, dict)):
                # Upgrade to a container node
                value = ContainerNode(value)
            if isNode(value):
                deps = value.dependencies()
                if self in deps:
                    raise ValueError("Setting %s's %s to %s creates a cycle in the derivation graph." % (self, name, value))
                self.__deps__.add(name)
            if name in self.__attrs__:
                if not isNode(value) and isNode(self.__attrs__[name]):
                    self.__deps__.remove(name)
            self.__attrs__[name] = value

    def __getattr__(self, attribute):
        return self.__attrs__[attribute]

    def cache(self, value):
        try:
            self.__cache__ = weakref.ref(value)
        except:
            self.__cache__ = lambda: value

    def dependencies(self):
        """
        Return a topologically sorted list of nodes that make up the derivation
        of this node.
        """

        # Build a list of nodes in the graph in the "deps" list
        nodes = [self]
        deps = []

        dep_graph = {}
        roots = []

        while nodes:
            d = nodes.pop(0)
            if len(d.__deps__) == 0:
                roots.append(d)
            deps.append(d)
            for a in d.__deps__:
                n = d.__attrs__[a]
                # Invert the dependencies
                dep_list = dep_graph.get(id(n), [])
                dep_list.append(d)
                dep_graph[id(n)] = dep_list
                if n not in deps and n not in nodes:
                    nodes.append(n)

        dependencies = []
        while roots:
            n = roots.pop()
            node_id = id(n)
            dependencies.append(n)
            if node_id in dep_graph:
                for child in dep_graph[node_id]:
                    # Remove this one
                    parent_count = len(child.__deps__) - 1
                    for a in child.__deps__:
                        p = id(child.__attrs__[a])
                        if p != node_id and p not in dep_graph:
                            parent_count -= 1
                    if parent_count == 0:
                        roots.append(child)

                del dep_graph[node_id]

        return dependencies[:-1]

    def __repr__(self):
        args = ["{key}={value}".format(key=key, value=repr(value)) for key, value in self.__attrs__.iteritems()]
        return "ComputeNode({args})".format(args=", ".join(args))

    def derive(self):
        """
        Calculates the value of this node based on the derivation tree.

        This is syntactic sugar for the derive_value function.
        """
        return derivation.derive_value(self)


# We hide this in here for internal use only. If someone really wants to dig
# into this, it's available, but it should be handled automagically by the
# library.

CONTAINER_TYPE = "container_node"


@derivation.register_computation(CONTAINER_TYPE)
def compute_container(attributes):
    if attributes["container_type"] == "dict":
        attrs = {k: v for k, v in attributes.iteritems() if k != "container_type"}
        return attrs
    elif attributes["container_type"] in ("list", "tuple"):
        vals = []
        for i in range(attributes["container_length"]):
            vals.append(attributes["array_%d" % i])
        if attributes["container_type"] == "tuple":
            return tuple(vals)
        return vals


class ContainerNode(ComputeNode):
    def __init__(self, container):
        super(ContainerNode, self).__init__()
        self.node_type = CONTAINER_TYPE
        # We can split the container apart into internal storage on this object
        # Really big containers will become less compact in JSON, but only mildly.
        if isinstance(container, dict):
            self.container_type = "dict"
            for k, v in container.iteritems():
                setattr(self, k, v)
        elif isinstance(container, list):
            self.container_type = "list"
            self.container_length = len(container)
            for ind, v in enumerate(container):
                setattr(self, "array_%d" % ind, v)
        elif isinstance(container, tuple):
            self.container_type = "tuple"
            self.container_length = len(container)
            for ind, v in enumerate(container):
                setattr(self, "array_%d" % ind, v)


def isNode(v):
    return isinstance(v, ComputeNode)
