from SudokuSolver import SudokuSolver 


squares   = str
gridValDict = dict
cols = '123456789'
rows      = 'ABCDEFGHI'
#cols      = digits

def cross(A,B) -> tuple:
    return tuple(a+b for a in A for b in B)

def display(values):
    "Display these values as a 2-D grid."
    rows      = 'ABCDEFGHI'
    cols      = '123456789'

    width = 1+max(len(values[s]) for s in squares)
    
    
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print ( ''.join(values[r+c].center(width)+('|' if c in '36' else '')
                    for c in cols) )
        if r in 'CF': print(line)
    print()

squares   = cross(rows, cols)
all_boxes = [cross(rs, cs)  for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')] 
all_units = [cross(rows, c) for c in cols] + [cross(r, cols) for r in rows] + all_boxes
units     = {s: tuple(u for u in all_units if s in u) for s in squares}
peers     = {s: set().union(*units[s]) - {s} for s in squares}


grid1 = '..53.....8......2..7..1.5..4....53...1..7...6..32...8..6.5....9..4....3......97..'
grid = '..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3..'


solver = SudokuSolver(squares, all_units, peers)
solution = solver.solvePuzzle(grid1)
display(solution)
