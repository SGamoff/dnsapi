from enum import Enum


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((x.name, x.value) for x in cls)


class ZoneTypes(ChoiceEnum):
    FWD = 'forward'
    RVS = 'reverse'


class ServerTypes(ChoiceEnum):
    BIND9 = 'bind9'
