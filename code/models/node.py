from validoot import validates, positive, typ

from .location import Location


class Node(Location):
    """
    An OSM Node
    """

    def __init__(self, nid, latitude, longitude, tags):
        super(Node, self).__init__(latitude, longitude)
        self.id = nid
        self.tags = tags

    def __repr__(self):
        return "Node({!r},{!r},{!r},{!r})".format(self.id, self.latitude, self.longitude, self.tags)

    def __str__(self):
        return repr(self)

    def __eq__(self, other):
        return self.id == other.id

    @property
    def id(self):
        return self.id

    @validates(positive)
    @id.setter
    def id(self, value):
        self.id = value

    @property
    def tags(self):
        return self.tags

    @validates(typ(dict))
    @tags.setter
    def tags(self, value):
        self.tags = value

    @classmethod
    def from_dict(cls, obj):
        if 'type' in obj and obj['type'] != 'node':
            raise ValueError("Object has incorrect type '%s'" % obj['type'])

        return Node(obj['id'], obj['lat'], obj['lon'], obj.get('tags', []))