class LCG:
    def __init__(self, seed, a, c, m):
        self.seed = seed
        self.a = a
        self.c = c
        self.m = m

    def rand(self):
        self.seed = (self.a * self.seed + self.c) % self.m
        return self.seed / self.m
    