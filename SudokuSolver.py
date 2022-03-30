import itertools
import collections
from random import *

class SudokuSolver:
    
    def __init__(self, squares, all_units, peers):
        self.squares = squares
        self.all_units = all_units
        self.peers = peers
        
        

    def gridtoValues(self,grid):
        """
            Module to convert the string of values of variables in sudoku to a dictionary 
            with values filled with domain values for the unfilled variable"

            Parameters:
            -----------
                grid: String of values with '.' for unfilled variables

            return:
            -------
                gridValDict : keys   : variables of sudoku puzzle
                              values : value of the variable with domain values for '.'
        """
        gridValDict = {}
        for key,val in zip(self.squares,grid): 
            if(val == '.'):
                gridValDict[key] = '123456789'
            else:
                gridValDict[key] = val
        return gridValDict

    
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

    # Constraint 3 - naked pair rule
    def nakedTwin(self,gridValDict):
    
        for unit in self.all_units:
            for sq, nxtSq in itertools.combinations(unit,2):
                if(gridValDict[sq] == gridValDict[nxtSq]) and len(gridValDict[sq]) == 2:
                    
                    sqToBeUpdated = [u for u in unit if (u != sq and u != nxtSq)]
                    
                    for s in sqToBeUpdated:
                        
                        for d in gridValDict[sq]:
                            gridValDict[s] = gridValDict[s].replace(d,'')
            
        return gridValDict
    # Hidden pair rule
    def hiddenTwin(self,gridValDict):
        
        for unit in self.all_units:
            numDict ={'1':[], '2':[], '3':[], '4':[], '5':[], '6':[], '7':[],'8':[], '9':[]}
            for sq in unit:
                for dig in '123456789':
                    if(dig in gridValDict[sq]):
                        numDict[dig].append(sq)
            filDict = {key: val for key,val in numDict.items() if(len(val) == 2 ) }
            for k1, k2 in itertools.combinations(filDict, 2):
                if(collections.Counter(filDict[k1]) == collections.Counter(filDict[k2])):
                    for sq in filDict[k1]:
                        if(len(gridValDict[sq]) > 2):
                            for d in gridValDict[sq]:
                                if (d != k1 and d != k2):
                                    gridValDict[sq] = gridValDict[sq].replace(d,'')
                                    
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
            
            if(constraint == 4):
                gridValDict = self.eliminate(gridValDict) 
                gridValDict = self.singlePossibility(gridValDict) 
                gridValDict = self.nakedTwin(gridValDict)
                gridValDict = self.hiddenTwin(gridValDict)
                            
            solvedSquaresAfterElim = len([sq for sq in gridValDict.keys() if (len(gridValDict[sq])==1)] )
            
            flag = solvedSquares == solvedSquaresAfterElim
            if(len([sq for sq in gridValDict.keys() if (len(gridValDict[sq])==0)] )):
                return False
        return gridValDict
        
    

    def backtrack(self,gridValDict, constraint, var_order):
        """
        Recursive module to do so depth first search with backtracking.

        parameters:
        -----------
            gridValDict : Dictionary
                represents the variables of the puzzle with corresponding values
            constraint  : int
                2 represents elimination and single possibility
                3 represents elimination, single possibility and naked pair
                4 represents elimination, single possibility, naked pair and hidden pair
            var_order   : string 
                "min"    - minimun heuristic remaining values
                "rand"   - randomly select a value
                "static" - select unassigned variable in order

        

        """
        
        gridValDict = self.reduceGridVal(gridValDict, constraint)
        if(gridValDict is False):
            return False
        # Sudoku solved!! if len of all values is 1
        if(all([len(gridValDict[sq]) == 1 for sq in self.squares])):
            return gridValDict
        #unfilled square with min number of digits
        if(var_order == 'min'):
            n,sq = min((len(gridValDict[sq]), sq) for sq in self.squares if len(gridValDict[sq]) > 1)
            
        #randomly select an unfilled square
        if(var_order == 'rand'):
            sq = choice([sq for sq in self.squares if len(gridValDict[sq]) > 1])
            
        # Select the square in order
        if(var_order == 'static'):
            sq = [sq for sq in self.squares if len(gridValDict[sq]) > 1][0]
           
        # display(gridValDict)
        for digit in gridValDict[sq]:
            gridValCopy = gridValDict.copy()
            gridValCopy[sq] = digit
            
            if( self.backtrack(gridValCopy, constraint, var_order) ):
                return self.backtrack(gridValCopy, constraint, var_order)

    def solvePuzzle(self,grid,constraint, var_order):
        gridValDict = self.gridtoValues(grid)
        reduced_puzzle = self.reduceGridVal(gridValDict,constraint)
        soln = self.backtrack(reduced_puzzle, constraint, var_order)
        return soln
        
