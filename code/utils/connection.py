

class Connection(object):
    """
    Connection documentation
    """

    def __init__(self, i1, i2):
        self.frm = i1
        self.to = i2

    def __hash__(self):
        return hash(repr(self))

    def __repr__(self):
        return "{} -> {}".format(self.frm, self.to)

    def __eq__(self, other):
        return self.frm == other.frm and self.to == other.to