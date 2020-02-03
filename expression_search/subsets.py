#!/usr/bin/env python2
#-*- coding:utf-8 -*-
"""
Usage:
$ pypy subsets.py [OP] [ARCH] [MAX_COST]
- OP can be one of XOR, AND, ANDNOT, NOTAND, OR, ORNOT, NOTOR, ANDOR
- ARCH defines the gate set:
    - BASIC stands for (XOR, AND, NOT);
    - ARM in addition adds BIC (BitClear) and ORN (OrNot) gates;
- MAX COST is the maximum number of gates to consider

Example:
$ pypy subsets.py OR BASIC 6
$ pypy subsets.py AND ARM 6
"""

import sys
from itertools import product, combinations, permutations
from collections import defaultdict

from space import BFSpace, xorlist, hw

from string import ascii_lowercase
ALPHABET = ascii_lowercase

NVARS = 2
arg = sys.argv[1].upper()
if arg == "XOR":
    op = lambda a, b: a ^ b
elif arg == "AND":
    op = lambda a, b: a & b
elif arg == "ANDNOT":
    op = lambda a, b: a & (b ^ 1)
elif arg == "NOTAND":
    op = lambda a, b: 1 ^ (a & b)
elif arg == "OR":
    op = lambda a, b: a | b
elif arg == "ORNOT":
    op = lambda a, b: a | (b ^ 1)
elif arg == "NOTOR":
    op = lambda a, b: 1 ^ (a | b)
elif arg == "ANDOR":
    op = lambda a, b, c: a & b | c
    NVARS = 3
else:
    assert False

MAX_COST_EXPAND = int(sys.argv[3])
ONLY_BEST = False

NLEAK = 1
NSHARES = 2
assert NLEAK == 1, "Only 1 shares supported"
assert NSHARES == 2, "Only 2 shares supported"

print "NLEAK", NLEAK
print "NSHARES", NSHARES
print "NVARS", NVARS
VARNAMES = ALPHABET[:NSHARES*NVARS]
SPACE = BFSpace(varnames=VARNAMES)

def TARGET(*vs):
    vs = [xorlist(vs[NSHARES*i:NSHARES*(i+1)]) for i in xrange(NVARS)]
    if NVARS == 2:
        return op(vs[0], vs[1])
    elif NVARS == 3:
        return op(vs[0], vs[1], vs[2])
    else:
        assert False, "Not implemented"
TARGET = SPACE.make_truth_table(TARGET)

USE_SYMMETRIES = 1

print "SYMMETRIES", USE_SYMMETRIES

# (a @ b) is NAND (NotAND)
# (a # b) is ANDNOT (or BIC - BitClear)
# (a $ b) is ORNOT
if sys.argv[2] == "BASIC":
    OPS = "^&|"
elif sys.argv[2] == "ARM":
    OPS = "^&|" + "#$"
else:
    assert False, "Unknown architecture: %s" % sys.argv[2]

print "OPS", OPS

def make_secrets_func(f):
    def func(*vs):
        secrets = [xorlist(vs[NSHARES*i:NSHARES*(i+1)]) for i in xrange(NVARS)]
        return f(*secrets)
    return SPACE.make_truth_table(func)

# Setting sensitive functions
leak_tables = []

# do not leak single secrets
for i in xrange(NVARS):
    leak_tables.append(make_secrets_func(lambda *secrets: secrets[i]))

# do not leak joint secrets
if NVARS == 2:
    leak_tables.append(make_secrets_func(lambda s0, s1: s0 & s1))
    leak_tables.append(make_secrets_func(lambda s0, s1: s0 & (1 ^ s1)))
    leak_tables.append(make_secrets_func(lambda s0, s1: (1 ^ s0) & s1))
    leak_tables.append(make_secrets_func(lambda s0, s1: (1 ^ s0) & (1 ^ s1)))

# target should not be leaked as well, though should be covered by joint secrets
leak_tables.append(TARGET)


space = SPACE

ignore = {0, space.mask} # ignore functions for fast checks

def toi(vs):
    return sum(v*(1<<i) for i, v in enumerate(reversed(vs)))

def bitget(v, i):
    return (v >> (2**space.nvar-1-i)) & 1

def bitset(v, i, bit):
    v |= bit << (2**space.nvar-1-i)
    return v

_permute_cache = {}
def permute(f, p):
    if (f, p) not in _permute_cache:
        f2 = 0
        for src, dst in p:
            b = bitget(f, src)
            f2 = bitset(f2, dst, b)
        _permute_cache[f,p] = f2
        return f2
    return _permute_cache[f,p]

perms = [ALPHABET[NSHARES*i:NSHARES*(i+1)] for i in xrange(NVARS)]
perms = [list(permutations(p)) for p in perms]
var_index = {v:i for i, v in enumerate(ALPHABET)}
ALL_PERMS = []
for var_perm in product(*perms):
    for var_perm in permutations(var_perm):
        var_perm = sum(var_perm, ())
        int_perm = [var_index[v] for v in var_perm]
        res = []
        for xs in product(range(2), repeat=space.nvar):
            xs2 = [xs[int_perm[i]] for i in xrange(space.nvar)]
            res.append((toi(xs), toi(xs2)))
        ALL_PERMS.append(tuple(res))
print "Total permutations", len(ALL_PERMS)

def subset_minimize(s):
    if not USE_SYMMETRIES:
        return s
    res = s[INITIAL_FUNCS:]
    for perm in ALL_PERMS:
        ss = tuple(permute(f, perm) for f in s[INITIAL_FUNCS:])
        res = min(res, ss)
    return s[:INITIAL_FUNCS] + res

def is_bad(f, subset):
    if f in ignore:
        return True
    if space.leaks1(f, leak_tables):
        ignore.add(f)
        return True
    return False

def expand_one_step():
    print "EXPANDING TO", len(by_cost), ":",
    prev = by_cost[-1]
    by_cost.append(set())
    for subset_prev in prev:
        for ia, ib in combinations(range(len(subset_prev)), 2):
            for op in OPS:
                check_function(subset_prev, op, ia, ib)
                if op in space.NON_SYMMETRIC_OPS:
                    check_function(subset_prev, op, ib, ia)
    print "RESULT", len(by_cost[-1])

def sid(subset):
    return tuple(sorted(subset))

def check_function(subset_prev, op, ia, ib):
    fa = subset_prev[ia]
    fb = subset_prev[ib]
    f = space.compute_op(op, fa, fb)
    if f == fa or f == fb or f in ignore or f in subset_prev:
        return
    subset = subset_prev + (f,)


    subset_id = sid(subset_minimize(subset))
    if subset_id in seen:
        return
    seen.add(subset_id)

    if is_bad(f, subset):
        return

    circ_a = best_expr[subset_prev[:ia+1]]
    circ_b = best_expr[subset_prev[:ib+1]]
    circ = Circuit(function=f, value=op, children=(circ_a, circ_b))
    best_expr[subset] = circ
    by_cost[-1].add(subset)


from circuit import Circuit

best_expr = {}
seen = set()
by_cost = [set()]

subset = []
exprs = []
f = space.make_truth_table(lambda *vs: 1)
subset.append(f)
exprs.append(Circuit(function=f, value="1"))
for i in xrange(space.nvar):
    f = space.make_truth_table(lambda *vs: vs[i])
    subset.append(f)
    exprs.append(Circuit(function=f, value=space.varnames[i]))
subset = tuple(subset)
exprs = tuple(exprs)
for i in xrange(len(subset)):
    best_expr[subset[:i+1]] = exprs[i]
seen.add(sid(subset))
by_cost[0].add(subset)

INITIAL_FUNCS = len(subset)

while len(by_cost)-1 < MAX_COST_EXPAND:
    expand_one_step()

    print "    ITERATING COST", len(by_cost)-1
    for subset in by_cost[-1]:
        fa = subset[-1]
        for fs in combinations(subset[:-1], NSHARES-2):
            # dual
            fb = xorlist(fs) ^ fa ^ TARGET
            assert xorlist(fs) ^ fa ^ fb == TARGET
            if fb not in subset:
                continue
            fs = [fa, fb] + list(fs)
            indexes = [subset.index(f) for f in fs]
            print "        SUBSET", len(subset) - INITIAL_FUNCS, ":",
            print "balanced?",
            for i in indexes:
                print int(space.is_balanced(subset[i])),
            print "shares:",
            for i in indexes:
                print best_expr[subset[:i+1]].cost2(),
            for i in indexes:
                print best_expr[subset[:i+1]].expr(),
            print
    print "    DONE"


