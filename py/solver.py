from copy import deepcopy
from datetime import datetime
from sys import stdout

class PuzzleSolver():
    """
    This class is the puzzle solver, using Piece, Board and Trans
    Its creation requires a Board, and a list of Piece it will try to put on the Board
    The puzzle solving is launch by calling its solve() method, which have the following options:
    - findAll : False by default, set to True if you want the solver run until all solutions
                have been found
    - print : True by defaut, set to False if you don't want the solutions printed as soon as
              they have been found, and only returned when execution has ended
    - sides : "front" by default, set to "back" or "both" depending on how the pieces shall
              be used to solve the puzzle. "front" and "back" definition are related to
              the way each pieces have been defined and the coordinate system of the board
      The solve() method returns a tuple containing:
          - The solutions as list of Board objects
          - The number of tries used (tries to put a piece on a square)
          - The number of pieces successfully put on the puzzle board
    """
    def __init__(self,board,pieces):
        self._board = board
        self._pieces = pieces
        self._sides = "front"
        self._nbPieces = len(self._pieces)
        self._startTime = None
        self._nbTries = 0
        self._nbPcsPut = 0
        self._findAll = False
        self._stop = False
        self._print=True
        
    def solve(self,findAll=False,printSol=True,sides="front"):
        self._findAll = findAll
        self._print = printSol
        self._sides = sides       
        solutions = []
        self._startTime = datetime.now()
        solutions=self._solve(self._board,self._pieces,solutions)
        return solutions,self._nbTries,self._nbPcsPut
        
    def _solve(self,board,pieces,solutions):
        nbPcs = len(pieces)
        if nbPcs:
            pos = board.nextAvailablePos()
            for piece in pieces:
                for origin in range(len(piece)):
                    piece.setOrigin(origin)
                    relTrans = piece.relevantTrans()
                    for trans in relTrans:
                        if nbPcs == self._nbPieces and not self._stop:
                            execDuration = str(datetime.now()-self._startTime)
                            if execDuration.rfind('.') != -1:
                                execDuration = execDuration[:execDuration.rfind('.')]
                            stdout.write("\r{0} - {1:.2f}% - {2} sol. over {3} pcs put with {4} tested combi.".format(\
                                    execDuration,\
                                    ((pieces.index(piece)*len(piece)*len(relTrans))+(origin*len(relTrans))+relTrans.index(trans))/(nbPcs*len(piece)*len(relTrans))*100,\
                                    len(solutions),\
                                    self._nbPcsPut,
                                    self._nbTries\
                                    )\
                                )
                            stdout.flush()
                        if  not self._stop and ( (self._sides=="front" and trans.isFront()) or (self._sides=="back" and trans.isBack()) or self._sides=="both"):
                            piece.transform(trans)
                            newBoard = board.putPiece(piece,pos)
                            self._nbTries += 1
                            if newBoard is not None:
                                self._nbPcsPut += 1
                                newPieces=deepcopy(pieces)
                                newPieces.remove(piece)
                                solutions=self._solve(newBoard,newPieces,solutions)
            if nbPcs == self._nbPieces:
                    print("\n")#to cleanely end same line print above
        else:
            if self._print == True:
                print("\nSolution found in {} after testing {} combinations and putting {} pieces:".format(str(datetime.now()-self._startTime)[:-7],self._nbTries,self._nbPcsPut))
                print(board,flush=True)
            if not self._findAll:
                self._stop = True
            solutions.append(board)
        return solutions