from sage.all import *


def fastGauss(m:list) -> list:
    F = GF(2)
    M = matrix(F,m)
    marks = [0]*len(m)
    height,width = M.dimensions()
    for w in range(width):
        col = M.column(w)
        for h in range(height):
            if col[h] == 1:
                for i in range(width):
                    if i == w:
                        continue
                    if M[h,i] == 1:
                        M.set_column(i, M.column(i) + col)
                marks[h] = 1
                break
    undet = []
    if 1 in marks:
        for h in range(height):
            if marks[h] == 0: undet += [h]
    else:
        return None
    solution_space = []
    for i in undet:
        if set(M.row(i)) == {0}:
            solution_space += [[1 if i == j else 0 for j in range(height)]]
            continue
        positions = [i for i, x in enumerate(M.row(i)) if x == 1]
        pos_sol = [i for i, row in enumerate(M) if (any(row[pos] == 1 for pos in positions)) and (marks[i] == 1)] + [i]
        sol = [1 if i in pos_sol else 0 for i in range(height)]
        solution_space += [sol]

    return solution_space