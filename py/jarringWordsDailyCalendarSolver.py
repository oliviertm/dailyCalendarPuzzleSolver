from puzzle import Vector, Trans, Piece, Board
from solver import PuzzleSolver
from datetime import datetime

def GenerateBoard(date):
    board = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,None,None,None,None,None,None,0,0,0,0],
        [0,0,0,None,None,None,None,None,None,0,0,0,0],
        [0,0,0,None,None,None,None,None,None,None,0,0,0],
        [0,0,0,None,None,None,None,None,None,None,0,0,0],
        [0,0,0,None,None,None,None,None,None,None,0,0,0],
        [0,0,0,None,None,None,None,None,None,None,0,0,0],
        [0,0,0,None,None,None,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0],
    ]
    dayNum = date.day-1
    monthNum=date.month-1
    board[int(monthNum/6)+3][(monthNum%6)+3] = date.strftime("%b")
    board[int(dayNum/7)+5][(dayNum%7)+3] = date.strftime("%d")
    return Board(board)

def CreatePieces():
    O = Piece(shape=[Vector(1,0),Vector(1,0),Vector(0,1),Vector(-1,0),Vector(-1,0)],name="O")# 6 squares rectangle
    t = Piece(shape=[Vector(1,0),Vector(1,0),Vector(1,0),Vector(-1,1)],name="t")# 5 squares small t shaped
    Q = Piece(shape=[Vector(0,1),Vector(1,0),Vector(0,1),Vector(-1,0)],name="Q")# 5 squares in square with teeth
    T = Piece(shape=[Vector(1,0),Vector(1,0),Vector(-1,1),Vector(0,1)],name="T")# T shaped 5 squares
    SmallsTail= Piece(shape=[Vector(1,0),Vector(0,1),Vector(1,0),Vector(1,0)],name="sl")# 5 squares small S with long tail
    BigL = Piece(shape=[Vector(0,1),Vector(1,0),Vector(1,0),Vector(1,0)],name="L")# big L
    U = Piece(shape=[Vector(0,1),Vector(1,0),Vector(1,0),Vector(0,-1)],name="U")# U shaped 5 squares
    Lequal = Piece(shape=[Vector(0,1),Vector(0,1),Vector(1,0),Vector(1,0)],name="LL")# L with equal lengh arms
    return [O,t,Q,T,SmallsTail,BigL,U,Lequal]
    
if __name__ == "__main__":
    userDate = input('Calendar puzzle date to solve (ex: 31/01/2022): ')
    try:
        date = datetime.strptime(userDate,"%d/%m/%Y")
    except ValueError:
        print("The date '{}' is not in the expected format dd/mm/yyyy".format(userDate))
    else:
        prettyDate = date.strftime("%A, %d %B %Y")
        pieces = CreatePieces()
        puzzle = GenerateBoard(date)
        solver = PuzzleSolver(puzzle,pieces)
        print("Start solving puzzle for {}".format(prettyDate))
        starttime = datetime.now()
        solutions,tries,nbPcsPut= solver.solve(findAll=True,printSol=True,sides="both")
        print("{} solutions found for {} in {} after {} tries and placing {} pieces".format(len(solutions),prettyDate,datetime.now() - starttime,tries,nbPcsPut))
     
