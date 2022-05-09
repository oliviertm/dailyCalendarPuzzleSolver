from puzzle import Vector, Trans, Piece, Board
from solver import PuzzleSolver

def GenerateHemaBoard():
    board = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,None,None,None,None,None,None,None,None,0,0,0],
        [0,0,0,None,None,None,None,None,None,None,None,0,0,0],
        [0,0,0,None,None,None,None,None,None,None,None,0,0,0],
        [0,0,0,None,None,None,None,None,None,None,None,0,0,0],
        [0,0,0,None,None,None,None,None,None,None,None,0,0,0],
        [0,0,0,None,None,None,None,None,None,None,None,0,0,0],
        [0,0,0,None,None,None,None,None,None,None,None,0,0,0],
        [0,0,0,None,None,None,None,None,None,None,None,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    ]
    return Board(board)

def CreateHemaPieces():
    Orange= Piece(shape=[Vector(1,0),Vector(0,1),Vector(0,1),Vector(0,1)],name="O")
    Pink = Piece(shape=[Vector(1,0),Vector(0,1),Vector(-1,0),Vector(0,1),Vector(0,1),Vector(1,0),Vector(1,0)],name="P")
    greenQ = Piece(shape=[Vector(1,0),Vector(0,1),Vector(-1,0),Vector(0,1),Vector(1,0),Vector(1,0)],name="vQ")
    T = Piece(shape=[Vector(1,0),Vector(1,0),Vector(-1,1),Vector(0,1)],name="T")
    blueQ = Piece(shape=[Vector(-1,0),Vector(0,1),Vector(1,0),Vector(0,1)],name="bQ")
    ZigZag = Piece(shape=[Vector(0,1),Vector(1,0),Vector(0,1),Vector(1,0)],name="Z")
    Cross= Piece(shape=[Vector(-1,1),Vector(1,0),Vector(1,0),Vector(-1,1)],name="+")
    DoubleSquare = Piece(shape=[Vector(0,1),Vector(1,-1),Vector(0,1),Vector(0,1),Vector(1,0),Vector(0,-1)],name="OO")
    U = Piece(shape=[Vector(0,1),Vector(1,0),Vector(1,0),Vector(1,0),Vector(0,-1)],name="U")
    L = Piece(shape=[Vector(0,1),Vector(0,1),Vector(1,0),Vector(1,0)],name="L")
    h = Piece(shape=[Vector(0,1),Vector(0,1),Vector(1,-1),Vector(1,0),Vector(0,1)],name="h")
    return [Orange,Pink,greenQ,T,blueQ,ZigZag,Cross,DoubleSquare,U,L,h]

if __name__ == "__main__":
    hemaBoard = GenerateHemaBoard()
    hemaPieces = CreateHemaPieces()
    solver = PuzzleSolver(hemaBoard,hemaPieces)
    solutions,nbTries,nbPcsPut = solver.solve(findAll=True,printSol=True,sides="both")
    print("{} solutions found after {} tries and {} placed pieces:\n{}".format(len(solutions),nbTries,nbPcsPut,solutions))
