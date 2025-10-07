def build_tree(formula):
    formula = formula.strip()
    if not formula:
        raise ValueError("Empty formula")
    if len(formula) == 1 and formula.isupper():
        return formula

    depth = 0
    for i in reversed(range(len(formula))):
        if formula[i] == ')':
            depth += 1
        elif formula[i] == '(':
            depth -= 1
        elif depth == 0:
            for o in ['<->', '->', '|', '&']:
                start = i - len(o) + 1
                if start >= 0 and formula[start:].startswith(o):
                    left = formula[:start]
                    right = formula[i + 1:]
                    return (o, build_tree(left), build_tree(right))

    if formula[0] == '~':
        return ('~', build_tree(formula[1:]))

    if formula[0] == '(' and formula[-1] == ')':
        return build_tree(formula[1:-1])

    raise ValueError(f"Invalid formula: {formula}")
