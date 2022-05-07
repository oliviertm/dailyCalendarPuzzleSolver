from enum import Enum
from copy import deepcopy

class Coordinate():
    """
    Class representing a coordinate on the puzzle board
    """
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

class Vector(Coordinate):
    """
    Class representing a vector, and used to define a puzzle piece
    """
    def __init__(self,x=0,y=0):
        super().__init__(x,y)

class Trans(Enum):
    """
    Class representing all physically possible puzzle pieces transformations
    There are 4 orientations with original piece side,
    and 4 more when the piece is flipped upside down
    """
    UpFront = 1
    RightFront = 2
    DownFront = 3
    LeftFront = 4
    UpBack = 5
    RightBack = 6
    DownBack = 7
    LeftBack = 8
    
    def isFront(self):
        if self.value < 5:
            return True
        else:
            return False

    def isBack(self):
        if self.value > 4:
            return True
        else:
            return False

class Piece():
    """
    Class used to represent a puzzle piece
    A puzzle pieces is coded with a list of Vector, a name and a list of relevant transformations
    The list of Vector represent the necessary moves to run through all the squares of the piece
    For example, this piece:      O                 ^ y axis
                                OOO    ---> x axis  |
    will be represented by 3 Vectors : two x=1,y=0 for the bottom part, 
    and one x=0,y=1 for the leg of this L shaped piece
    Of course, a piece of only 1 square will be represented with an empty Vector list
    The name of the piece is used to represent it on the puzzle board,
    in the example above this is "O"
    The relevantTrans is a list of Trans which will be used to test all relevant positions
    This class is able to compute this list automatically IF no piece square have more than
    two neighbors, otherwise, this list will be too long, and some solutions found will
    be the same.
    For example, the piece above will lead to a correctly computed list of relevantTrans
    but this piece won't:    OO
                             OO
    for this piece, you'll need to provide to this classe the list of relevantTrans, 
    which will be for this piece : relevantTrans=[Trans.UpFront], because this piece
    have two axis of symetry
    """
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
            invertedTransPiece = [Vector(-t.x,-t.y) for t in reversed(transPiece)]
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
                newShape.append(Vector(coord.y,-coord.x))
            if transformation == Trans.DownFront:
                newShape.append(Vector(-coord.x,-coord.y))
            if transformation == Trans.LeftFront:
                newShape.append(Vector(-coord.y,coord.x))
            if transformation == Trans.UpBack :
                newShape.append(Vector(-coord.x,coord.y))
            if transformation == Trans.RightBack:
                newShape.append(Vector(coord.y,coord.x))
            if transformation == Trans.DownBack:
                newShape.append(Vector(coord.x,-coord.y))
            if transformation == Trans.LeftBack:
                newShape.append(Vector(-coord.y,-coord.x))
        return newShape
     
class Board():
    """
    This class represent the board of the puzzle
    A board is initialized by a two dimensions array (a list of lists)
    This array shall contains "None" on any available square, and 0
    on squares where no pieces can be put
    As the puzzle solver will try to put pieces on boad borders, the array
    provided to build this board shall have enough unavailable square all 
    around to prevent the solver from trying to put a piece square outside
    the board array. The number of unavailable squares around the "None"
    filled cells of the board array depend on the length of the bigger
    piece of the piece list.
    Any shape of board is possible, providing that the "None" cells
    are surrounded by enough not availables cells (0 filled)
    to create a 2 dimensions array.
    The system of corrdinates of the puzzle is the following:
    board parameter of the contructor is a list of list such as it is a list
    of X axis lines. The coordinate x=0,y=0 correspond to the top left corner
    of the puzzle, and positive X are growing to the right, and positive Y are
    growing down, e.g
    board =  [ [x=0 y=0, x=1 y=0],
               [x=0 y=1, x=1 y=1] ]
    Due to the, the internal _board of this class is used with Y coordinates first
    """
    def __init__(self,board):
        if isinstance(board,Board):
            #Copy constructor
            self._board = deepcopy(board._board)
            self._origin = board._origin
        else:
            self._board = board
            self._origin = self._getOrigin()

    def _getOrigin(self):
        xMin= len(self._board[0])
        yMin = len(self._board)
        for y in range(len(self._board)):
            for x in range(len(self._board[y])):
                if self._board[y][x] != 0:
                    if x < xMin:
                        xMin = x
                    if y < yMin:
                        yMin = y
        return Coordinate(xMin,yMin)

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
        
    def _putPieceSquare(self,name,pos):
        if self._board[self._origin.y+pos.y][self._origin.x+pos.x] is None:
            self._board[self._origin.y+pos.y][self._origin.x+pos.x] = name
            return self
        else:
            return None
        
    def putPiece(self,piece,pos):
        newBoard = Board(self)
        newBoard = newBoard._putPieceSquare(piece.name,pos)
        if newBoard is None:
            return None
        idx = -1
        currPos = pos
        vect = piece[idx]
        while vect is not None:
            nextPos = Coordinate(currPos.x-vect.x,currPos.y-vect.y)
            newBoard = newBoard._putPieceSquare(piece.name,nextPos)
            if newBoard is None:
                return None
            currPos = nextPos
            idx -= 1
            vect = piece[idx]
        idx = 1
        currPos = pos
        vect = piece[idx]
        while vect is not None:
            nextPos = Coordinate(currPos.x+vect.x,currPos.y+vect.y)
            newBoard = newBoard._putPieceSquare(piece.name,nextPos)
            if newBoard is None:
                return None
            currPos = nextPos
            idx += 1
            vect = piece[idx]
        return newBoard
        
    def nextAvailablePos(self):
        ret = None
        x=self._origin.x
        y=self._origin.y
        while y < len(self._board) and ret is None:
            while x <len(self._board[y]) and ret is None:
                pos=self._board[y][x]
                if pos is None:
                    ret = Coordinate(x-self._origin.x,y-self._origin.y)
                x+=1
            x=0
            y+=1
            
        return ret