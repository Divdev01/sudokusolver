# sudokusolver
Sudoku is number puzzle with 9X9 grid with 9 3X3 subgrids. Some of the squares are filled with numbers. The objective of the puzzle is to fill all the 81 squares with numbers from 1-9 in a way that no number gets repeated in each row, column or box.

The objective of this work is to design an agent that solves sudoku puzzle. The Agent uses the following steps

## Constraint Propagation
Constraint propagation is an inference that can be used to reduce the domain values for the variable, that will inturn reduces the domain value of another variable and so on.

## Backtracking Search
Back tracking search uses a depth first search to try all values till the bottom and then backtrack if these is any inconsistency (ie no value can be assigned to the variable to satisfy the constraint)

# References

    https://en.wikipedia.org/wiki/Sudoku

    Artificial Intelligence: A mordern approach by Stuart Russell and Peter Norvig

    https://norvig.com/sudoku.html

    https://www.sudokudragon.com/sudokustrategy.htm
