class sudoku:
    def __init__(self, gridValDict, squares):
        self.gridValDict = gridValDict
        self.squares = squares

    def cross(A,B) -> tuple:
        return tuple(a+b for a in A for b in B)

    
    

    def display(values):
        "Display these values as a 2-D grid."
        width = 1+max(len(values[s]) for s in squares)
        line = '+'.join(['-'*(width*3)]*3)
        for r in rows:
            print ( ''.join(values[r+c].center(width)+('|' if c in '36' else '')
                        for c in cols) )
            if r in 'CF': print(line)
        print()