from puzzle import Vector, Trans, Piece, Board
from solver import PuzzleSolver


def testSolve():
    A = Piece(shape=[Vector(0,1),Vector(0,1),Vector(1,0)],name="A")
    B = Piece(shape=[Vector(0,1)],name="B")
    puzzle=Board([[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,None,None,0,0],[0,0,None,None,0,0],[0,0,None,None,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]])
    print("===== Solving with 2 pieces without returning the pieces, expecting 2 solutions")
    solver=PuzzleSolver(puzzle,[A,B])
    solver.solve(findAll=True)

def testSolve2():
    A = Piece(shape=[Vector(0,1),Vector(0,1),Vector(1,-1)],name="A")
    B = Piece(shape=[Vector(0,1)],name="B")
    C = Piece(shape=[Vector(0,1),Vector(1,0)],name="C")
    puzzle=Board([[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,None,None,None,0,0],[0,0,None,None,None,0,0],[0,0,None,None,None,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]])
    print("===== Solving with 3 pieces without returning the pieces")
    solver=PuzzleSolver(puzzle,[A,B,C])
    solutions,nbTries,nbPcsPut = solver.solve(findAll=True,printSol=False)
    print("{} solutions found, expected 8".format(len(solutions)))
    
def testSolve3():
    A = Piece(shape=[Vector(0,1),Vector(0,1),Vector(1,0)],name="A")
    B = Piece(shape=[Vector(0,1),Vector(0,1),Vector(1,0)],name="B")
    C = Piece(shape=[],name="C")
    puzzle=Board([[0,0,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,None,None,None,0,0],[0,0,None,None,None,0,0],[0,0,None,None,None,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,0]])
    print("===== Solving with 3 pieces without returning pieces")
    solver=PuzzleSolver(puzzle,[A,B,C])
    solutions,nbTries,nbPcsPut = solver.solve(findAll=True,printSol=False)
    print("{} solutions found, expected 4".format(len(solutions)))
    print("===== Solving  with 3 pieces with returning pieces")
    solver2=PuzzleSolver(puzzle,[A,B,C])
    solutions2,nbTries2,nbPcsPut2 = solver2.solve(findAll=True,printSol=False,sides="both")
    print("{} solutions found, expected 8".format(len(solutions2)))

if __name__ == "__main__":
    testSolve()
    testSolve2()
    testSolve3()
