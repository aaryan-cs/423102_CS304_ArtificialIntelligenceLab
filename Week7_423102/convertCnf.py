from logicParser import build_tree

def traverseCNF(node,):
    if type(node) == str:
        return node
    elif node[0] == '~':
        return f'~{node[1]}'
    elif node[0] == '&':
        return f'{traverseCNF(node[1])} & {traverseCNF(node[2])}'
    elif node[0] == '|':
        return f'{traverseCNF(node[1])}|{traverseCNF(node[2])}'
    else:
        raise "Not in CNF"
    
def splitCNF(node, clauses, current=None):
    if type(node) != str and node[0] == '&':
        splitCNF(node[1], clauses)
        splitCNF(node[2], clauses)
    else:
        newClause = False
        if current == None:
            current = set()
            newClause = True
        
        if type(node) == str:
            if f'~{node}' in current:
                current.clear()
            else:
                current.add(node)
        elif node[0] == '~':
            if node[1] in current:
                current.clear()
            else:
                current.add(f'~{node[1]}')
        
        elif node[0] == '|':
            splitCNF(node[1], clauses, current)
            if current:
                splitCNF(node[2], clauses, current)
        else:
            raise "Not in CNF"

        if newClause and current:
            clauses.append(current)

def buildCNFTree(node):
    if type(node) == str:
        return node
    
    if len(node) == 3 and node[0] == '<->':
        return buildCNFTree(('&', ('->', node[1], node[2]), ('->', node[2], node[1])))
    elif len(node) == 3 and node[0] == '->':
        return buildCNFTree(('|', ('~', node[1]), node[2]))
    elif len(node) == 2 and node[0] == '~':
        inner = node[1]
        if type(inner) == str:
            return node    
        if len(inner) == 2 and inner[0] == '~':
            return buildCNFTree(inner[1])
        elif len(inner) == 3 and inner[0] == '&':
            return buildCNFTree(('|', ('~', inner[1]), ('~', inner[2])))
        elif len(inner) == 3 and inner[0] == '|':
            return buildCNFTree(('&', ('~', inner[1]), ('~', inner[2])))
        elif len(inner) == 3 and (inner[0] == '<->' or inner[0] == '->'):
            return buildCNFTree(('~', buildCNFTree(inner)))
        else:
            raise "Error while attempting De Morgan's laws"
    elif len(node) == 3 and node[0] == '|':
        node1 = buildCNFTree(node[1])
        node2 = buildCNFTree(node[2])
        
        if node1[0] == '&':
            return ('&', buildCNFTree(('|', node2, node1[1])), buildCNFTree(('|', node2, node1[2])))
        elif node2[0] == '&':
            return ('&', buildCNFTree(('|', node1, node2[1])), buildCNFTree(('|', node1, node2[2])))
        else:
            return ('|', node1, node2)
    elif len(node) == 3 and node[0] == '&':
        return ('&', buildCNFTree(node[1]), buildCNFTree(node[2]))
    else:
        raise "Error: Invalid node"
    
def convertToCNF(tree):
    clauses = []
    splitCNF(buildCNFTree(tree), clauses)
    return clauses
    

# if __name__ == '__main__':
#     result = build_tree("((~P & Q) <-> (R|S)) | (~P -> S)")

#     cnf = buildCNFTree(result)
#     print(cnf)

#     print(traverseCNF(cnf))

#     clauses = []
#     splitCNF(cnf, clauses)
#     print(clauses)

