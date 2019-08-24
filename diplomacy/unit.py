class Unit(object):
    """A unit that is placed in a diplomacy map"""

    def __init__(self, owner: str, type: str):
        self.owner = owner
        self.type = type

    def serialize(self):
        """Serialize this Unit as a dict for JSON"""
        return self.__dict__

    @classmethod
    def from_dict(cls, dict_):
        return cls(dict_['owner'], dict_['type'])
