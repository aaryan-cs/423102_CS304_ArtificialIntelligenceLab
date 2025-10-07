from convertCnf import convertToCNF
from logicParser import build_tree

KB = """
(A&B)->C
D->E
C|D->F
"""

G = """
(A&B)->D
"""

def makeFormula(base):
    formula = ""
    for line in base.strip().splitlines():
        formula += f"({line})&"
    formula = formula[:-1] if formula[-1] == '&' else formula
    return formula

def simplify(cnf):
    uniq = []
    for s in cnf:
        if not any(s > x for x in cnf):
            uniq.append(s)
    return uniq

formula = makeFormula(KB) + f"&~({makeFormula(G)})"

tree = build_tree(formula)
cnf = convertToCNF(tree)
cnf = simplify(cnf)

def resolve(cnf):
    pairs = set()
    for i in range(len(cnf)):
        for j in range(i + 1, len(cnf)):
            pairs.add((i, j))

    while pairs:
        i, j = pairs.pop()
        c1, c2 = cnf[i], cnf[j]

        for l1 in c1:
            for l2 in c2:
                if l1 == f'~{l2}' or l2 == f'~{l1}':
                    c12 = (c1 - {l1}) | (c2 - {l2})
                    if len(c12) == 0:
                        return True
                    cnf.append(c12)
                    for i in range(len(cnf) - 1):
                        pairs.add((i, len(cnf) - 1))
    return False


if resolve(cnf):
    print("Does entail")
else:
    print("Does not entail")