import weakref


class ComputeNode(object):

    __slots__ = ('__deps__', '__cache__', '__attrs__', '__deps__')

    def __init__(self, **attrs):
        self.__attrs__ = attrs
        self.__deps__ = set()
        for a, v in attrs.iteritems():
            if isNode(v):
                self.__deps__.add(a)
        self.__cache__ = lambda: None

    def __setattr__(self, name, value):
        if name in self.__slots__:
            super(ComputeNode, self).__setattr__(name, value)
        else:
            if name in self.__attrs__:
                if isNode(value):
                    self.__deps__.add(name)
                elif isNode(self.__attrs__[name]):
                    self.__deps__.remove(name)
            self.__attrs__[name] = value

    def __getattr__(self, attribute):
        return self.__attrs__[attribute]

    def dependencies(self):
        """
        Return a topologically sorted list of nodes that make up the derivation
        of this node.
        """
        nodes = [self]
        deps = []
        while nodes:
            d = nodes.pop(0)
            deps.append(d)
            for a in d.__deps__:
                n = d.__attrs__[a]
                if n not in deps and n not in nodes:
                    nodes.append(n)
        return deps[::-1]


def isNode(v):
    return isinstance(v, ComputeNode)
