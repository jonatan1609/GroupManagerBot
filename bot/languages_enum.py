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

    def map(self):
        return self.MAP_DICT.value.get(self.value, "")
