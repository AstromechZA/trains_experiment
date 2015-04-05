
class IndexMap(object):
    """
    IndexMap documentation
    """

    def __init__(self, starting_names):
        self.id_to_name = {}
        self.name_to_id = {}
        self.id_to_attributes = {}
        self.current_id = 0
        for n in starting_names:
            self.add(n)

    def __contains__(self, name):
        return name in self.name_to_id

    def add(self, name):
        # If the name is already known, return the existing id
        if name in self.name_to_id:
            return self.name_to_id[name]

        # Otherwise, insert it
        self.id_to_name[self.current_id] = name
        self.id_to_attributes[self.current_id] = {}
        self.name_to_id[name] = self.current_id

        # Increment id
        self.current_id += 1

        # Lol, return original id
        return self.current_id - 1

    def geti(self, name):
        return self.name_to_id[name]

    def getn(self, index):
        return self.id_to_name[index]

    def geta(self, index):
        return self.id_to_attributes[index]

    def __iter__(self):
        for i in sorted(self.id_to_name.keys()):
            yield i, self.id_to_name[i], self.id_to_attributes[i]
