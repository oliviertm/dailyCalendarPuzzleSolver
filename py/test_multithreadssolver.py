from puzzle import Vector, Trans, Piece, Board
from multithreadssolver  import MultiThreadPuzzleSolver

def testSolve():
    A = Piece(shape=[Vector(0,1),Vector(0,1),Vector(1,0)],name="A")
    B = Piece(shape=[Vector(0,1)],name="B")
    puzzle=Board([[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,None,None,0,0],[0,0,None,None,0,0],[0,0,None,None,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]])
    print("===== MultiTread Solving with 2 pieces without returning the pieces, expecting 2 solutions")
    solver=MultiThreadPuzzleSolver(puzzle,[A,B])
    solutions,tries,nbPcsPut=solver.solve(findAll=True,printSol=True)
    print("{} solutions after {} tries and {} pieces put :".format(len(solutions),tries,nbPcsPut))
    for sol in solutions:
        print(sol)

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
        [0,0,0,None,None,None,None,None,None,None,0,0,0],
        [0,0,0,0,0,0,0,None,None,None,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0],
    ]
    weekDayNum = date.weekday()
    dayNum = date.day-1
    monthNum=date.month-1
    board[int(monthNum/6)+3][(monthNum%6)+3] = date.strftime("%b")
    board[int(dayNum/7)+5][(dayNum%7)+3] = date.strftime("%d")
    if weekDayNum == 6:
        board[9][6] = date.strftime("%a")
    else:
        board[int(weekDayNum/3)+9][(weekDayNum%3)+7] = date.strftime("%a")
    return Board(board)

def CreatePieces():
    FourFlat= Piece(shape=[Vector(0,1),Vector(0,1),Vector(0,1)],name="I")# 4 squares in line
    SmallS = Piece(shape=[Vector(0,1),Vector(1,0),Vector(0,1)],name="s")# 4 squares small S
    SmallL = Piece(shape=[Vector(0,1),Vector(1,0),Vector(1,0)],name="Ls")# 4 squares small L
    T = Piece(shape=[Vector(1,0),Vector(1,0),Vector(-1,1),Vector(0,1)],name="T")# T shaped 5 squares
    Q = Piece(shape=[Vector(0,1),Vector(1,0),Vector(0,1),Vector(-1,0)],name="Q")# 5 squares in square with teeth
    BigS = Piece(shape=[Vector(1,0),Vector(0,1),Vector(0,1),Vector(1,0)],name="S")# 5 squares in big S
    SmallsTail= Piece(shape=[Vector(1,0),Vector(0,1),Vector(1,0),Vector(1,0)],name="sl")# 5 squares small S with long tail
    BigL = Piece(shape=[Vector(0,1),Vector(1,0),Vector(1,0),Vector(1,0)],name="L")# big L
    U = Piece(shape=[Vector(0,1),Vector(1,0),Vector(1,0),Vector(0,-1)],name="U")# U shaped 5 squares
    Lequal = Piece(shape=[Vector(0,1),Vector(0,1),Vector(1,0),Vector(1,0)],name="LL")# L with equal lengh arms
    return [FourFlat,SmallS,SmallL,T,Q,BigS,SmallsTail,BigL,U,Lequal]
    
from datetime import datetime

if __name__ == "__main__":
    # Simple puzzle solving test
    testSolve()
    # Complex Poodle puzzle daily calendar solving test
    date = datetime.strptime("06/05/2022","%d/%m/%Y")
    prettyDate = date.strftime("%A, %d %B %Y")
    pieces = CreatePieces()
    puzzle = GenerateBoard(date)
    solver = MultiThreadPuzzleSolver(puzzle,pieces)
    print("Start solving puzzle for {}".format(prettyDate))
    starttime = datetime.now()
    sols,tries,nbPcsPut= solver.solve(findAll=True,sides="front")
    print("{} solutions found for {} in {} after {} tries and placing {} pieces".format(len(sols),prettyDate,datetime.now() - starttime,tries,nbPcsPut))
