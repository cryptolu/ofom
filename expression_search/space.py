#-*- coding:utf-8 -*-

from itertools import product, combinations, chain
from fractions import Fraction

class BFSpace(object):
    ONE = "1"

    def __init__(self, varnames):
        self.varnames = varnames
        self.nvar = len(varnames)
        self.mask = 2**(2**self.nvar) - 1

        self.debug = False

    def sbin(self, x):
        return bin(x).lstrip("0b").rjust(2**self.nvar, "0")

    def neg(self, x):
        return x ^ self.mask

    def make_truth_table(self, f):
        res = 0
        for xs in product(range(2), repeat=self.nvar):
            res = (res << 1) | f(*xs)
        return res

    def leaks1(self, tt, leak_masks):
        ntt = self.neg(tt)
        hw_tt = hw(tt)
        hw_ntt = hw(ntt)
        for mask in leak_masks:
            # print "MASK", mask
            fq1 = (hw(mask & tt), hw_tt)
            fq0 = (hw(mask & ntt), hw_ntt)
            if not fraq_eq(fq0, fq1):
                if self.debug:
                    print "leaks1:", self.sbin(tt), self.sbin(ntt), "vs", self.sbin(mask), ":", fq1, fq0
                return True
        return False

    def is_balanced(self, f):
        return hw(f) == 1 << (self.nvar - 1)

    NON_SYMMETRIC_OPS = "#$"

    def compute_op(self, op, ta, tb):
        if op == "^": return ta ^ tb
        if op == "&": return ta & tb
        if op == "|": return ta | tb
        if op == "@": return (ta & tb) ^ self.mask # NAND
        if op == "#": return (ta & (tb ^ self.mask)) # BIC (Bit Clear)
        if op == "$": return (ta | (tb ^ self.mask)) # ORN
        raise NotImplementedError("Unknown op: %r" % op)


def _hw(n):
    c = 0
    while n:
        c += 1
        n &= n - 1
    return c

hw_e = 16
hw_mask = (1 << hw_e) - 1
hw_table = [_hw(n) for n in xrange(1 << hw_e)]

def hw(n):
    c = 0
    while n:
        c += hw_table[n & hw_mask]
        n >>= hw_e
    return c

def xorlist(lst):
    if not lst:
        return 0
    return reduce(lambda a, b: a ^ b, lst)

def fraq_eq(fa, fb):
    # faster than Fractions?
    return fa[0] * fb[1] == fa[1] * fb[0]
