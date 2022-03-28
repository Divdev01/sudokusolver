import itertools

class SudokuSolver:
    
    def __init__(self, squares, all_units, peers):
        self.squares = squares
        self.all_units = all_units
        
        self.peers = peers
        
        

    def gridtoValues(self,grid):
        #digits = '123456789'
        gridValDict = {}
        for key,val in zip(self.squares,grid): 
            if(val == '.'):
                gridValDict[key] = '123456789'
            else:
                gridValDict[key] = val
        return gridValDict

    # def display(self,values):
    #     "Display these values as a 2-D grid."
    #     rows      = 'ABCDEFGHI'
    #     cols      = '123456789'

    #     width = 1+max(len(values[s]) for s in self.squares)
        
        
    #     line = '+'.join(['-'*(width*3)]*3)
    #     for r in rows:
    #         print ( ''.join(values[r+c].center(width)+('|' if c in '36' else '')
    #                     for c in cols) )
    #         if r in 'CF': print(line)
    #     print()

    # Constraint 1 - elimination rule
    def eliminate(self,gridValDict):
        for sq,val in gridValDict.items():
            if(len(val) == 1):
                digit = val
                for peer in self.peers[sq]:
                    gridValDict[peer] = gridValDict[peer].replace(digit,'')
                
        return gridValDict

    #Contraint 2 - Single possibility rule - 
    def singlePossibility(self, gridValDict):
        for unit in self.all_units:
            for d in '123456789':
                sq_dig = [sq for sq in unit if(d in gridValDict[sq])]
                if(len(sq_dig) == 1):
                    gridValDict[sq_dig[0]] = d
        return gridValDict

    # Constraint 3 - naked twins rule
    def nakedTwin(self,gridValDict):
    
        for unit in self.all_units:
            for sq, nxtSq in itertools.combinations(unit,2):
                if(gridValDict[sq] == gridValDict[nxtSq]) and len(gridValDict[sq]) == 2:
                    
                    sqToBeUpdated = [u for u in unit if (u != sq and u != nxtSq)]
                    
                    for s in sqToBeUpdated:
                        
                        for d in gridValDict[sq]:
                            gridValDict[s] = gridValDict[s].replace(d,'')
            
        return gridValDict

    def reduceGridVal(self, gridValDict, constraint):
        flag = False
        while not (flag): 

            solvedSquares = len([sq for sq in gridValDict.keys() if (len(gridValDict[sq])==1)] )
            
            if(constraint == 1):
                gridValDict = self.eliminate(gridValDict)  #Constraint 1 :elimination strategy
            
            if(constraint == 2):
                gridValDict = self.eliminate(gridValDict) 
                gridValDict = self.singlePossibility(gridValDict) 

            if(constraint == 3):
                gridValDict = self.eliminate(gridValDict) 
                gridValDict = self.singlePossibility(gridValDict) 
                gridValDict = self.nakedTwin(gridValDict)
            
            solvedSquaresAfterElim = len([sq for sq in gridValDict.keys() if (len(gridValDict[sq])==1)] )
            
            flag = solvedSquares == solvedSquaresAfterElim
            if(len([sq for sq in gridValDict.keys() if (len(gridValDict[sq])==0)] )):
                return False
        return gridValDict
        
    


    def backtrack(self,gridValDict, constraint):
        
        gridValDict = self.reduceGridVal(gridValDict, constraint)
        if(gridValDict is False):
            return False
        # Sudoku solved!! if len of all values is 1
        #print("length:",[len(gridValDict[sq]) for sq in squares] )
        #print([len(gridValDict[sq]) == 1 for sq in squares])
        #print("boolean", all([len(gridValDict[sq]) == 1 for sq in squares]))
        if(all([len(gridValDict[sq]) == 1 for sq in self.squares])):
        #  print("**********")
            return gridValDict
        #unfilled square with min number of digits
        n,sq = min((len(gridValDict[sq]), sq) for sq in self.squares if len(gridValDict[sq]) > 1)
        # display(gridValDict)
        for digit in gridValDict[sq]:
            gridValCopy = gridValDict.copy()
            gridValCopy[sq] = digit

            # success = backtrack(gridValCopy)
            # if success:
            #   return success
            
            if( self.backtrack(gridValCopy, constraint) ):
                return self.backtrack(gridValCopy, constraint)

    def solvePuzzle(self,grid,constraint):
        gridValDict = self.gridtoValues(grid)
        reduced_puzzle = self.reduceGridVal(gridValDict,constraint)
        # print("reduced puzzle after constraint propagation")
        # self.display(reduced_puzzle)
        # print("Solved Puzzle")
        soln = self.backtrack(reduced_puzzle, constraint)
        return soln
        # self.display(soln)

