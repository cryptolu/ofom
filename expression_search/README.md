# Search for Optimal First-order Sharing Expressions

This folder contains an implementation of the expression search algorithm (Algorithm 1) from the paper

[Optimal First-Order Boolean Masking for Embedded IoT Devices](https://link.springer.com/chapter/10.1007/978-3-319-75208-2_2) \
by Alex Biryukov, Daniel Dinu, Yann Le Corre and Aleksei Udovenko (CARDIS 2017)

The code is written in Python 2. For optimal performance, it is suggested to run it using PyPy. The script should be called as follows:

```bash
$ pypy subsets.py [OP] [ARCH] [MAX_COST]
```

- `OP` can be one of XOR, AND, ANDNOT, NOTAND, OR, ORNOT, NOTOR, ANDOR
- `ARCH` defines the gate set:
    - `BASIC`  stands for (XOR, AND, NOT);
    - `ARM` in addition adds BIC (BitClear) and ORN (OrNot) gates;
- `MAX COST` is the maximum number of gates to consider;

Example:
``` bash
$ pypy subsets.py OR BASIC 6
...
EXPANDING TO 6 : RESULT 1139464
    ITERATING COST 6
        SUBSET 6 : balanced? 1 1 shares: 3 3 (b|c)^(b&d) (a&c)^(a|d)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (a|d)^(b&d) (a&c)^(b|c)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (b&c)^(b|d) (a|c)^(a&d)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (a&d)^(b|d) (a|c)^(b&c)
    DONE

$ pypy subsets.py AND ARM 6
...
EXPANDING TO 6 : RESULT 11539239
    ITERATING COST 6
        SUBSET 6 : balanced? 1 1 shares: 3 3 (a&d)^(b#d) (a&c)^(b#c)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (a&d)$(d$b) (a&c)^(b#c)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (a&d)^(b#d) (a&c)$(c$b)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (a&d)^(d$b) (a&c)^(c$b)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (a&d)$(d$b) (a&c)$(c$b)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (b#c)^(b|d) (a&c)^(d#a)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (d#a)^(b|d) (a&c)^(b#c)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (c$b)&(b|d) (a&c)^(d#a)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (d#a)$(b|d) (a&c)^(c$b)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (d#a)^(b|d) (a&c)$(c$b)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (b&c)^(d#b) (a&c)$(a$d)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (b&c)^(b$d) (a&c)^(a$d)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (b&c)$(b$d) (a&c)$(a$d)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (c$b)^(b|d) (a&c)^(a$d)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (c$b)&(b|d) (a&c)$(a$d)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (a$d)^(b|d) (a&c)^(c$b)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (a$d)&(b|d) (a&c)$(c$b)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (b&c)$(b$d) (a&c)^(d#a)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (a|d)^(d#b) (a|c)^(c#b)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (d#b)$(a|d) (c#b)$(a|c)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (a|d)&(b$d) (a|c)^(c#b)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (a|d)^(b$d) (c#b)$(a|c)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (d#b)$(a|d) (a|c)^(b$c)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (a|d)^(d#b) (a|c)&(b$c)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (a|d)^(b$d) (a|c)^(b$c)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (a|d)&(b$d) (a|c)&(b$c)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (c#b)^(b&d) (a|c)^(a#d)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (a#d)^(b&d) (a|c)^(c#b)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (b&d)$(b$c) (a|c)^(a#d)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (b$c)^(b&d) (a#d)$(a|c)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (a#d)^(b&d) (a|c)&(b$c)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (b#d)$(b|c) (a|c)^(d$a)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (b|c)^(b#d) (a|c)&(d$a)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (b|c)^(d$b) (a|c)^(d$a)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (b|c)&(d$b) (a|c)&(d$a)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (b$c)^(b&d) (a|c)^(d$a)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (b&d)$(b$c) (a|c)&(d$a)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (d$a)^(b&d) (a|c)^(b$c)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (b&d)$(d$a) (a|c)&(b$c)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (b$d)&(a|d) (a|c)^(c#b)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (b$d)^(a|d) (c#b)$(a|c)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (a#d)^(b&d) (a#c)^(b&c)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (b&d)$(d$a) (a#c)^(b&c)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (d#a)$(b|d) (a$c)^(b|c)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (d#a)^(b|d) (a$c)&(b|c)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (a$d)^(b|d) (a$c)^(b|c)
        SUBSET 6 : balanced? 1 1 shares: 3 3 (a$d)&(b|d) (a$c)&(b|c)
    DONE
```
