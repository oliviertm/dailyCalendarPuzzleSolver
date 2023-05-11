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
        
    def move(self,vector):
        self.x+=vector.x
        self.y+=vector.y
               
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
    """
    def __init__(self,shape,name):
        self._baseShape = shape
        self._currShape = shape
        self.name = name
        self._origin = 0
        if len(self._baseShape):
            self._relevantTrans = self._listRelevantTransform()
        else:
            self._relevantTrans = [Trans.UpFront]

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
        
    def _listRelevantTransform(self):
        transformedPiecesFrames = []
        relevantTransform = []
        for trans in Trans:
            transPiece = self._transform(trans)
            minX = 0
            minY = 0
            maxX = 0
            maxY = 0
            pos  = Coordinate()
            for vect in transPiece:
                pos.move(vect)
                if pos.x>maxX:
                    maxX=pos.x
                if pos.x<minX:
                    minX=pos.x
                if pos.y>maxY:
                    maxY=pos.y
                if pos.y<minY:
                    minY=pos.y
            xSpan=maxX-minX
            ySpan=maxY-minY
            pos=Coordinate(-minX,-minY)
            transPieceFrame=[[0 for x in range(xSpan+1)] for y in range(ySpan+1)]
            transPieceFrame[pos.y][pos.x]=1
            for vect in transPiece:
                pos.move(vect)
                transPieceFrame[pos.y][pos.x]=1
            if transPieceFrame not in transformedPiecesFrames:
                transformedPiecesFrames.append(transPieceFrame)
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
        for y in range(len(self._board)):
            for x in range(len(self._board[y])):
                if x >= (xMin-1) and x <= (xMax+1) and y >= (yMin-1) and y <= yMax:
                    c=" "
                    if self._board[y][x] != self._board[y][x-1] :
                        c="|"
                    ret+=c
                    c=" "
                    if self._board[y][x] != self._board[y+1][x] :
                        c="_"
                    ret+=c
            if y >= (yMin-1) and y <= yMax:
                ret += "\n"
        return ret
        
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
