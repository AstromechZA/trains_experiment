from validoot import validates, positive, typ


class Way(object):
    """
    An OSM Way object
    """

    def __init__(self, wid, nodes, tags):
        self.id = wid
        self.nodes = nodes
        self.tags = tags

    def __repr__(self):
        return "Way({!r},{!r},{!r})".format(self.id, self.nodes, self.tags)

    def __str__(self):
        return repr(self)

    def __eq__(self, other):
        return self.id == other.id

    def __contains__(self, item):
        return item in self.nodes

    @property
    def id(self):
        return self.id

    @validates(positive)
    @id.setter
    def id(self, value):
        self.id = value

    @property
    def nodes(self):
        return self.nodes

    @validates(typ(list))
    @nodes.setter
    def nodes(self, value):
        self.nodes = value

    @property
    def tags(self):
        return self.tags

    @validates(typ(dict))
    @tags.setter
    def tags(self, value):
        self.tags = value

    @classmethod
    def from_dict(cls, obj):
        if 'type' in obj and obj['type'] != 'way':
            raise ValueError("Object has incorrect type '%s'" % obj['type'])

        return Way(obj['id'], obj['nodes'], obj['tags'])