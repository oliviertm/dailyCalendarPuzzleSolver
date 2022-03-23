import multiprocessing as mp
from time import sleep
from enum import Enum
from copy import deepcopy
from datetime import datetime

class Coordinate():
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y
        
    def __eq__(self,other):
        """
        required to be able to use == operator on Coordinate object
        """
        if other is not None and self.x == other.x and self.y == other.y:
            return True
        else:
            return False
        
    def __repr__(self):
        return "(x={},y={})".format(self.x,self.y)

class Trans(Enum):
    UpFront = 1
    RightFront = 2
    DownFront = 3
    LeftFront = 4
    UpBack = 5
    RightBack = 6
    DownBack = 7
    LeftBack = 8

class Piece():
    def __init__(self,shape,name,relevantTrans=None):
        self._baseShape = shape
        self._currShape = shape
        self.name = name
        self._origin = 0
        if relevantTrans is None:
            self._relevantTrans = self.listRelevantTransform()
        else:
            if len(self._baseShape):
                self._relevantTrans = relevantTrans
            else:
                self._relevantTrans = Trans(0)

    def __repr__(self):
        return "(base={}\ncurrent={}\nname={}\norigin=({})\nrelevantTrans={})".format(self._baseShape,self._currShape,self.name,self._origin,self._relevantTrans)
                        
    def __len__(self):
        # Add one because a single square piece has no vector
        return len(self._currShape)+1
        
    def __getitem__(self,idx):
        """
        required to be able to use [] operator on Piece object
        """
        ret=None
        if idx>0:
            idx -=1
        if (idx+self._origin) < len(self._currShape) and (idx+self._origin) >= 0:
            ret = self._currShape[idx+self._origin]
        return ret
        
    def __eq__(self,other):
        """
        required to be able to use remove() operator on list of Piece objects
        As two pieces with the same name could not be distinguished once on a board, they are considered as the same as soon as they have the same name
        """
        if self.name == other.name:
            return True
        else:
            return False
        
    def setOrigin(self,origin):
        if origin >=0 and origin <= len(self._currShape):
            self._origin = origin
     
    def relevantTrans(self):
        return self._relevantTrans
        
    def listRelevantTransform(self):
        transformedPieces = []
        relevantTransform = []
        for trans in Trans:
            transPiece = self._transform(trans)
            invertedTransPiece = [Coordinate(-t.x,-t.y) for t in reversed(transPiece)]
            if transPiece not in transformedPieces and invertedTransPiece not in transformedPieces:
                transformedPieces.append(transPiece)
                relevantTransform.append(trans)
        return relevantTransform
        
    def transform(self,transformation):
        self._currShape = self._transform(transformation)
        
    def _transform(self,transformation):
        newShape = []
        for coord in self._baseShape:
            if transformation == Trans.UpFront :
                newShape.append(coord)
            if transformation == Trans.RightFront:
                newShape.append(Coordinate(coord.y,-coord.x))
            if transformation == Trans.DownFront:
                newShape.append(Coordinate(-coord.x,-coord.y))
            if transformation == Trans.LeftFront:
                newShape.append(Coordinate(-coord.y,coord.x))
            if transformation == Trans.UpBack :
                newShape.append(Coordinate(-coord.x,coord.y))
            if transformation == Trans.RightBack:
                newShape.append(Coordinate(coord.y,coord.x))
            if transformation == Trans.DownBack:
                newShape.append(Coordinate(coord.x,-coord.y))
            if transformation == Trans.LeftBack:
                newShape.append(Coordinate(-coord.y,-coord.x))
        return newShape
     
class Board():
    def __init__(self,board,origin=None):
        self._board = board
        if origin==None:
            self._origin = self._nextAvailablePos(Coordinate(0,0))
        else:
            self._origin=origin
        
    def __repr__(self):
        ret = ""
        padding = max([len(repr(i)) for j in self._board for i in j])+1
        xMax = 0
        xMin= len(self._board[0])
        yMax = 0
        yMin = len(self._board)
        for y in range(len(self._board)):
            for x in range(len(self._board[y])):
                if self._board[y][x] != 0:
                    if x < xMin:
                        xMin = x
                    if x > xMax:
                        xMax = x
                    if y < yMin:
                        yMin = y
                    if y > yMax:
                        yMax = y
        printedBoard=[]
        for y in range(len(self._board)):
            if y >= yMin and y <= yMax:
                printedBoard.append([])
            for x in range(len(self._board[y])):
                if x >= xMin and x <= xMax and y >= yMin and y <= yMax:
                    printedBoard[y-yMin].append(self._board[y][x])
        for line in printedBoard:
            ret += "".join([repr(i).ljust(padding) for i in line]) + "\n"
        return "(\n{})".format(ret)
        
    def _putPieceSquare(self,board,name,pos):
        if board[self._origin.y+pos.y][self._origin.x+pos.x] is None:
            board[self._origin.y+pos.y][self._origin.x+pos.x] = name
            return board
        else:
            return None
        
    def putPiece(self,piece,pos):
        newBoard = deepcopy(self._board)
        nextBoard = self._putPieceSquare(newBoard,piece.name,pos)
        if nextBoard is None:
            return None
        idx = -1
        currPos = pos
        vect = piece[idx]
        while vect is not None:
            nextPos = Coordinate(currPos.x-vect.x,currPos.y-vect.y)
            newBoard = self._putPieceSquare(nextBoard,piece.name,nextPos)
            if newBoard is None:
                return None
            nextBoard = newBoard
            currPos = nextPos
            idx -= 1
            vect = piece[idx]
        idx = 1
        currPos = pos
        vect = piece[idx]
        while vect is not None:
            nextPos = Coordinate(currPos.x+vect.x,currPos.y+vect.y)
            newBoard = self._putPieceSquare(nextBoard,piece.name,nextPos)
            if newBoard is None:
                return None
            nextBoard = newBoard
            currPos = nextPos
            idx += 1
            vect = piece[idx]
        return Board(board=nextBoard,origin=self._origin)
        
    def nextAvailablePos(self):
        return self._nextAvailablePos(self._origin)
        
    def _nextAvailablePos(self,origin):
        ret = None
        x=origin.x
        y=origin.y
        while y < len(self._board) and ret is None:
            while x <len(self._board[y]) and ret is None:
                pos=self._board[y][x]
                if pos is None:
                    ret = Coordinate(x-origin.x,y-origin.y)
                x+=1
            x=0
            y+=1
            
        return ret
        
class Solver():
    def __init__(self,board,pieces,frontOnly=False,printSol=True,findAll=True):
        self._board = board
        self._pieces = pieces
        self._frontOnly = frontOnly
        self._startTime = None
        self._processes = []
        self._printSol = printSol
        self._findAll=findAll
        
    def solve(self):
        self._startTime = datetime.now()
        for piece in self._pieces:
                parentPipe, childPipe= mp.Pipe()
                p = mp.Process(target=Solver._pieceSolve, args=(self,self._board,self._pieces,piece,len(self._processes),childPipe))
                self._processes.append({"proc":p,"pipe":parentPipe})
                p.start()
        tries = 0
        nbSol = 0
        while len(self._processes):
            stoppedProc = []
            for p in self._processes:
                if p["pipe"].poll():
                    answer = p["pipe"].recv()
                    if "tries" in answer:
                        tries += answer["tries"]
                        nbSol += answer["nbSol"]
                        stoppedProc.append(p)
                    elif "stop" in answer:
                        for p in self._processes:
                            if p["proc"].is_alive():
                                try:
                                    p["pipe"].send({"stop":True})
                                except BrokenPipeError:
                                    pass#process terminated since is_alive() called
            sleep(1)
            for p in stoppedProc:
                self._processes.remove(p)
        return nbSol,tries
 
    def _pieceSolve(self,board,pieces,piece,pid,pipe):
            tries=0
            nbSol=0
            stop=False
            pos = self._board.nextAvailablePos()
            relTrans = piece.relevantTrans()
            for trans in relTrans:
                if  self._frontOnly is False or trans.value < 5:
                    piece.transform(trans)
                    for origin in range(len(piece)):
                        piece.setOrigin(origin)
                        newBoard = self._board.putPiece(piece,pos)
                        tries += 1
                        if pipe.poll():
                            signal = pipe.recv()
                            if "stop" in signal:
                                stop = True
                        if newBoard is not None and not stop:
                            newPieces=deepcopy(pieces)
                            newPieces.remove(piece)
                            tries,nbSol,stop = self._recursiveSolve(newBoard,newPieces,pid,tries,nbSol,pipe,stop)
            pipe.send({"tries":tries,"nbSol":nbSol})
            #print("End of process {} after {} with {} sol. found using {} tries".format(pid,str(datetime.now()-self._startTime)[:-7],nbSol,tries))
        
    def _recursiveSolve(self,board,pieces,pid,tries,nbSol,pipe,stop):
        if len(pieces):
            pos = board.nextAvailablePos()
            for piece in pieces:
                for origin in range(len(piece)):
                    piece.setOrigin(origin)
                    relTrans = piece.relevantTrans()
                    for trans in relTrans:
                        if  self._frontOnly is False or trans.value < 5:
                            piece.transform(trans)
                            newBoard = board.putPiece(piece,pos)
                            tries += 1
                            if pipe.poll():
                                signal = pipe.recv()
                                if "stop" in signal:
                                    stop = True
                            if newBoard is not None and not stop:
                                newPieces=deepcopy(pieces)
                                newPieces.remove(piece)
                                tries,nbSol,stop = self._recursiveSolve(newBoard,newPieces,pid,tries,nbSol,pipe,stop)
        else:
            if self._printSol :
                print("\nSolution found by process {} in {} after testing {} combinations:".format(pid,str(datetime.now()-self._startTime)[:-7],tries))
                print(board,flush=True)
            if not self._findAll:
                pipe.send({"stop":True})
                stop = True
            nbSol += 1
        return tries,nbSol,stop

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
    FourFlat= Piece(shape=[Coordinate(0,1),Coordinate(0,1),Coordinate(0,1)],name="I")# 4 squares in line
    SmallS = Piece(shape=[Coordinate(0,1),Coordinate(1,0),Coordinate(0,1)],name="s")# 4 squares small S
    SmallL = Piece(shape=[Coordinate(0,1),Coordinate(1,0),Coordinate(1,0)],name="Ls")# 4 squares small L
    T = Piece(shape=[Coordinate(1,0),Coordinate(1,0),Coordinate(-1,1),Coordinate(0,1)],name="T",relevantTrans=[Trans.UpFront,Trans.RightFront,Trans.DownFront,Trans.LeftFront])# T shaped 5 squares
    Q = Piece(shape=[Coordinate(0,1),Coordinate(1,0),Coordinate(0,1),Coordinate(-1,0)],name="Q")# 5 squares in square with teeth
    BigS = Piece(shape=[Coordinate(1,0),Coordinate(0,1),Coordinate(0,1),Coordinate(1,0)],name="S")# 5 squares in big S
    SmallsTail= Piece(shape=[Coordinate(1,0),Coordinate(0,1),Coordinate(1,0),Coordinate(1,0)],name="sl")# 5 squares small S with long tail
    BigL = Piece(shape=[Coordinate(0,1),Coordinate(1,0),Coordinate(1,0),Coordinate(1,0)],name="L")# big L
    U = Piece(shape=[Coordinate(0,1),Coordinate(1,0),Coordinate(1,0),Coordinate(0,-1)],name="U")# U shaped 5 squares
    Lequal = Piece(shape=[Coordinate(0,1),Coordinate(0,1),Coordinate(1,0),Coordinate(1,0)],name="LL")# L with equal lengh arms
    return [FourFlat,SmallS,SmallL,T,Q,BigS,SmallsTail,BigL,U,Lequal]
    
def CreatePiecesBack():
    FourFlat= Piece(shape=[Coordinate(0,1),Coordinate(0,1),Coordinate(0,1)],name="I",relevantTrans=[Trans.UpBack,Trans.RightBack,Trans.DownBack,Trans.LeftBack])# 4 squares in line
    SmallS = Piece(shape=[Coordinate(0,1),Coordinate(1,0),Coordinate(0,1)],name="s",relevantTrans=[Trans.UpBack,Trans.RightBack,Trans.DownBack,Trans.LeftBack])# 4 squares small S
    SmallL = Piece(shape=[Coordinate(0,1),Coordinate(1,0),Coordinate(1,0)],name="Ls",relevantTrans=[Trans.UpBack,Trans.RightBack,Trans.DownBack,Trans.LeftBack])# 4 squares small L
    T = Piece(shape=[Coordinate(1,0),Coordinate(1,0),Coordinate(-1,1),Coordinate(0,1)],name="T",relevantTrans=[Trans.UpBack,Trans.RightBack,Trans.DownBack,Trans.LeftBack])# T shaped 5 squares
    Q = Piece(shape=[Coordinate(0,1),Coordinate(1,0),Coordinate(0,1),Coordinate(-1,0)],name="Q",relevantTrans=[Trans.UpBack,Trans.RightBack,Trans.DownBack,Trans.LeftBack])# 5 squares in square with teeth
    BigS = Piece(shape=[Coordinate(1,0),Coordinate(0,1),Coordinate(0,1),Coordinate(1,0)],name="S",relevantTrans=[Trans.UpBack,Trans.RightBack,Trans.DownBack,Trans.LeftBack])# 5 squares in big S
    SmallsTail= Piece(shape=[Coordinate(1,0),Coordinate(0,1),Coordinate(1,0),Coordinate(1,0)],name="sl",relevantTrans=[Trans.UpBack,Trans.RightBack,Trans.DownBack,Trans.LeftBack])# 5 squares small S with long tail
    BigL = Piece(shape=[Coordinate(0,1),Coordinate(1,0),Coordinate(1,0),Coordinate(1,0)],name="L",relevantTrans=[Trans.UpBack,Trans.RightBack,Trans.DownBack,Trans.LeftBack])# big L
    U = Piece(shape=[Coordinate(0,1),Coordinate(1,0),Coordinate(1,0),Coordinate(0,-1)],name="U",relevantTrans=[Trans.UpBack,Trans.RightBack,Trans.DownBack,Trans.LeftBack])# U shaped 5 squares
    Lequal = Piece(shape=[Coordinate(0,1),Coordinate(0,1),Coordinate(1,0),Coordinate(1,0)],name="LL",relevantTrans=[Trans.UpBack,Trans.RightBack,Trans.DownBack,Trans.LeftBack])# L with equal lengh arms
    return [FourFlat,U,Q, BigL,SmallL,SmallsTail,SmallS,Lequal,BigS,T]#list by freqency in first pos in sol

def testSolve3():
    A = Piece(shape=[Coordinate(0,1),Coordinate(0,1),Coordinate(1,0)],name="A")
    B = Piece(shape=[Coordinate(0,1),Coordinate(0,1),Coordinate(1,0)],name="B")
    C = Piece(shape=[],name="C")
    puzzle=Board([[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,None,None,None,0,0],[0,0,None,None,None,0,0],[0,0,None,None,None,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]])
    print("With returning pieces")
    solver=Solver(puzzle,[A,B,C],findAll=False)
    starttime = datetime.now()
    nbSol,tries = solver.solve()
    print("{} solutions found in {} after {} tries".format(nbSol,datetime.now()- starttime,tries))
    print("Without returning pieces")
    solver2=Solver(puzzle,[A,B,C],True,printSol=False,findAll=True)
    starttime = datetime.now()
    nbSol,tries = solver2.solve()
    print("{} solutions found in {} after {} tries".format(nbSol,datetime.now() - starttime,tries))
      
if __name__ == '__main__':
    #testSolve3()
    userDate = input('Calendar puzzle date to solve (ex: 31/01/2022): ')
    try:
        date = datetime.strptime(userDate,"%d/%m/%Y")
    except ValueError:
        print("The date '{}' is not in the expected format dd/mm/yyyy".format(userDate))
    else:
        prettyDate = date.strftime("%A, %d %B %Y")
        pieces = CreatePieces()
        puzzle = GenerateBoard(date)
        solver = Solver(puzzle,pieces,frontOnly=True,printSol=True,findAll=False)
        print("Start multithreads puzzle solving for {}:".format(prettyDate))
        starttime = datetime.now()
        nbSol,tries = solver.solve()
        print("{} solutions for {} found in {} after {} tries".format(nbSol,prettyDate,datetime.now() - starttime,tries))
