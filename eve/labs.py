class Calculator:
    def __init__(self):
        self.cache = dict()

    def add(self, x, y):
        if not self.cache.get("add"):
            self.cache["add"] = list()
            z = x + y
            self.cache["add"].append((x, y, z))
            return z
        else:
            for a , b , c in self.cache["add"]:
                if (x == a) and (y == b):
                    return c
                    break
            else:
                z = x + y
                self.cache["add"].append((x, y, z))
                return z

    def subtract(self, x, y):
        if not self.cache.get("subtract"):
            self.cache["subtract"] = list()
            z = x - y
            self.cache["subtract"].append((x, y, z))
            return z
        else:
            for a , b , c in self.cache["subtract"]:
                if (x == a) and (y == b):
                    return c
                    break
            else:
                z = x - y
                self.cache["subtract"].append((x, y, z))
                return z


c = Calculator()
assert hasattr(c, 'cache')
assert c.cache == {}


assert c.add(2, 8) == 10
assert c.cache == {
    'add': [
        (2, 8, 10)
    ]
}

assert c.subtract(7, 2) == 5
assert c.cache == {
    'add': [
        (2, 8, 10)
    ],
    'subtract': [
        (7, 2, 5)
    ]
}

assert c.subtract(11, 7) == 4
assert c.cache == {
    'add': [
        (2, 8, 10)
    ],
    'subtract': [
        (7, 2, 5),
        (11, 7, 4)
    ]
}

# Repeated operation. Should be cached
assert c.add(2, 8) == 10
assert c.cache == {
    'add': [
        (2, 8, 10)
    ],
    'subtract': [
        (7, 2, 5),
        (11, 7, 4)
    ]
}
