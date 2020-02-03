#-*- coding:utf-8 -*-

from itertools import product
from collections import defaultdict

class Circuit(object):
    def __init__(self, function, value, children=()):
        # assert isinstance(function, int) or isinstance(function, long)
        assert isinstance(value, str)
        self.function = function
        self.value = value
        self.children = tuple(children)
        self._cost = 0
        if self.children:
            self._cost += (len(self.children) - 1) + sum(c.cost() for c in self.children)
        self._en = None
        self._pn = None
        self._funcs = None

    def expr(self, polish=False):
        if polish:
            if self._pn is None:
                self._pn = "".join(c.expr(polish=True) for c in self.children) + self.value
            return self._pn
        else:
            if self._en is None:
                if not self.children:
                    self._en = self.value
                else:
                    assert len(self.children) > 1
                    self._en = self.value.join( wrap(c.expr(polish=False)) for c in self.children)
            return self._en

    def __str__(self):
        return self.expr()

    def pexpr(self):
        return self.expr(polish=True)

    def cost(self):
        return self._cost

    def cost2(self):
        return len(self.functions())

    def functions(self):
        if self._funcs is None:
            self._funcs = {self.function} if self.children else set()
            for c in self.children:
                for f in c.functions():
                    self._funcs.add(f)
        return self._funcs

def wrap(v):
    return ("(" + v + ")") if len(v) > 1 else v
