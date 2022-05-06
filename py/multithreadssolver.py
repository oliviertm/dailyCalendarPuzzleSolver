from copy import deepcopy
from datetime import datetime
from time import sleep
import multiprocessing as mp

def recursiveSolve(board,pieces,pid,tries,nbPcsPut,nbSol,side,startTime,findAll,pipe,stop):
    if len(pieces):
        pos = board.nextAvailablePos()
        for piece in pieces:
            for origin in range(len(piece)):
                piece.setOrigin(origin)
                relTrans = piece.relevantTrans()
                for trans in relTrans:
                    if  ( (side=="front" and trans.isFront()) or (side=="back" and trans.isBack()) or side=="both"):
                        piece.transform(trans)
                        newBoard = board.putPiece(piece,pos)
                        tries += 1
                        if pipe.poll():
                            signal = pipe.recv()
                            if "stop" in signal:
                                stop = True
                        if newBoard is not None and not stop:
                            nbPcsPut+=1
                            newPieces=deepcopy(pieces)
                            newPieces.remove(piece)
                            tries,nbPcsPut,nbSol,stop = recursiveSolve(newBoard,newPieces,pid,tries,nbPcsPut,nbSol,side,startTime,findAll,pipe,stop)
    else:
        print("\nSolution found by process {} in {} after testing {} combinations and putting {} pieces:".format(pid,str(datetime.now()-startTime)[:-7],tries,nbPcsPut))
        print(board,flush=True)
        if not findAll:
            pipe.send({"stop":True})
            stop = True
        nbSol += 1
    return tries,nbPcsPut,nbSol,stop

def pieceSolve(board,pieces,piece,side,startTime,findAll,pid,pipe):
        tries=0
        nbSol=0
        nbPcsPut=0
        stop=False
        pos = board.nextAvailablePos()
        relTrans = piece.relevantTrans()
        for trans in relTrans:
            if  ( (side=="front" and trans.isFront()) or (side=="back" and trans.isBack()) or side=="both"):
                piece.transform(trans)
                for origin in range(len(piece)):
                    piece.setOrigin(origin)
                    newBoard = board.putPiece(piece,pos)
                    tries += 1
                    if pipe.poll():
                        signal = pipe.recv()
                        if "stop" in signal:
                            stop = True
                    if newBoard is not None and not stop:
                        nbPcsPut+=1
                        newPieces=deepcopy(pieces)
                        newPieces.remove(piece)
                        tries,nbPcsPut,nbSol,stop = recursiveSolve(newBoard,newPieces,pid,tries,nbPcsPut,nbSol,side,startTime,findAll,pipe,stop)
        pipe.send({"tries":tries,"nbSol":nbSol,"nbPcsPut":nbPcsPut})
        print("End of process {} after {} with {} sol. found using {} tries and putting {} pieces".format(pid,str(datetime.now()-startTime)[:-7],nbSol,tries,nbPcsPut))

class MultiThreadPuzzleSolver():
    """
    This class is the multithread version of the puzzle solver, using Piece, Board and Trans
    Its creation requires a Board, and a list of Piece it will try to put on the Board
    The puzzle solving is launch by calling its solve() method, which have the following options:
    - findAll : False by default, set to True if you want the solver run until all solutions
                have been found
    - sides : "front" by default, set to "back" or "both" depending on how the pieces shall
              be used to solve the puzzle. "front" and "back" definition are related to
              the way each pieces have been defined and the coordinate system of the board
    Unlike the single tread version of the solver, this one always print the solutions as soon
    as they have been found, because the return of the list of solutions from the launch threads
    haven't been implemented.
    Using this version of the puzzle solver is interesting on multi-core system, because on single
    core system, the use of multiple threads on a single core may slow down the solving of the puzzle
    """
    def __init__(self,board,pieces):
        self._board = board
        self._pieces = pieces
        self._startTime = None
        self._processes = []
        self._findAll=False
        
    def solve(self,findAll=False,sides="front"):
        self._sides = sides
        self._findAll = findAll
        self._startTime = datetime.now()
        for piece in self._pieces:
                parentPipe, childPipe= mp.Pipe()
                p = mp.Process(target=pieceSolve, \
                    args=(self._board,self._pieces,piece,self._sides,self._startTime,self._findAll,len(self._processes),childPipe))
                self._processes.append({"proc":p,"pipe":parentPipe})
                p.start()
        tries = 0
        nbSol = 0
        nbPcsPut = 0
        while len(self._processes):
            stoppedProc = []
            for p in self._processes:
                if p["pipe"].poll():
                    answer = p["pipe"].recv()
                    if "tries" in answer:
                        tries += answer["tries"]
                        nbSol += answer["nbSol"]
                        nbPcsPut += answer["nbPcsPut"]
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
        return nbSol,tries,nbPcsPut