import enum


class Meta(enum.EnumMeta):
    def __getattribute__(self, name):
        obj = super().__getattribute__(name)
        if isinstance(obj, enum.Enum) and obj.value.__hash__:
            return obj.map()
        return obj


class LanguagesEnum(enum.Enum, metaclass=Meta):
    EN = enum.auto()
    HE = enum.auto()

    MAP_DICT = {HE: "hebrew", EN: "english"}

    def map(self=None):
        if not self:
            return [obj.map().title() for obj in tuple(LanguagesEnum._member_map_.values())[:-1]]
        return self.MAP_DICT.value.get(self.value, "")
