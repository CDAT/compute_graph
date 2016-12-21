import weakref
import derivation


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

    def cache(self, value):
        try:
            self.__cache__ = weakref.ref(value)
        except:
            self.__cache__ = value

    def dependencies(self):
        """
        Return a topologically sorted list of nodes that make up the derivation
        of this node.
        """

        # Do a breadth-first search of the parents.
        # This will ensure that the deps list has a node without inputs at the
        # end. All of the other leaves will be interspersed through the deps
        # array, but they'll all be after the stuff that needs them.
        # So, good enough
        nodes = [self]
        deps = []
        while nodes:
            d = nodes.pop(0)
            deps.append(d)
            for a in d.__deps__:
                n = d.__attrs__[a]
                if n not in deps and n not in nodes:
                    nodes.append(n)
        # Remove self from dependencies (we're not our own dependency)
        # Flip list to be topo-sorted.
        return deps[:0:-1]

    def __repr__(self):
        args = ["{key}={value}".format(key=key, value=repr(value)) for key, value in self.__attrs__.iteritems()]
        return "ComputeNode({args})".format(args=", ".join(args))

    def derive(self):
        """
        Calculates the value of this node based on the derivation tree.

        This is syntactic sugar for the derive_value function.
        """
        return derivation.derive_value(self)


def isNode(v):
    return isinstance(v, ComputeNode)
