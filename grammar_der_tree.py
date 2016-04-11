# Little tricky function to print N levels of a given grammar derivation tree

N = 5

def productions_from(vn, P):
    return [(vn, derivation) for vnp, derivation in P if vnp == vn]

def nonterminals_in(sform, Vn):
    return [char for char in sform if char in Vn]

def level_derivation(previous_level, Vn, P):
    lvl = []
    for sform in previous_level:
        for vn in nonterminals_in(sform, Vn):
            for vnp, derivation in productions_from(vn, P):
                string = sform.replace(vn, "".join(derivation)).replace("lambda", "")
                lvl.append(string)

    return lvl

def dev_tree(Vn, Vt, P, S):
    tree = [[S]]
    for i in range(1, N):
        lvl = level_derivation(tree[i-1], Vn, P)
        tree.append(lvl)

    for l in tree:
        print(" ".join(l))



P = (
    ("S", ["a", "S", "b"]),
    ("S", ["b", "S", "a"]),
    ("S", ["lambda"])
)
dev_tree(["S"], ["a", "b", "lambda"], P, "S")
