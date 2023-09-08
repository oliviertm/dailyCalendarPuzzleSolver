#include <iostream>
#include <string>
#include <time.h>
#include <stdexcept>
#include <ctime>
#include <chrono>
#include <stdlib.h>

using namespace std;

enum Trans { up, right, down, left, upBack, leftBack, downBack, rightBack};

// Puzzle board coordinates
class Coord
{
    public:
        int x;
        int y;
        
        Coord(int cx,int cy){x=cx;y=cy;}
        Coord(){x=0;y=0;}
        virtual ~Coord(){}
        void AssignFrom(const Coord& other){x=other.x;y=other.y;}
        Coord(const Coord& other){AssignFrom(other);}
        Coord& operator=(const Coord& other){AssignFrom(other);return *this;}
        bool operator==(const Coord& other){if((x==other.x)&&(y==other.y)) return true; else return false;}
        virtual ostream& put(ostream & o,char sep=' ') const {return o<< "(x=" << x << "y=" << y  << ")" << sep;}

	friend ostream& operator<<(ostream& o, const Coord& p){return p.put(o);}
};

// Vector used for puzzle piece definition
class Vect: public Coord
{
    public:
        
        Vect(int vx,int vy):Coord(vx,vy){}
        Vect():Coord(){}
        
        inline bool isNull(){if(x==0&&y==0) return true; else return false;}
};

// Puzzle piece
class Piece
{

protected:
    Vect * baseShape;
    Vect * currShape;
    
public:
    int shapeLength;
    int origin;
    unsigned char value;
    Trans* relevantTrans;
    int nbRelevantTrans;

    Piece(Vect shape[], int shapeLen, int val, Trans relTrans[], int nbRelTrans);
    virtual ~Piece();
    void transform(Trans transformation);
    Vect operator[](int index);
    virtual ostream& put(ostream & o,char sep=' ') const ;
    friend ostream& operator<<(ostream& o, const Piece& p){return p.put(o);}
};

Piece::Piece(Vect shape[], int shapeLen, int val, Trans relTrans[], int nbRelTrans)
{
    int i;
    shapeLength = shapeLen;
    baseShape = new Vect[shapeLength];
    currShape = new Vect[shapeLength];
    for(i=0;i<shapeLength;i++){
        baseShape[i] = shape[i];
        currShape[i] = shape[i];
    }
    origin = 0;
    value = val;
    nbRelevantTrans = nbRelTrans;
    relevantTrans = new Trans[nbRelTrans];
    for(i=0;i<nbRelevantTrans;i++){
        relevantTrans[i] = relTrans[i];
    }
}

Piece::~Piece()
{
    if(baseShape){
        delete[] baseShape;
        baseShape = NULL;
    }
    if(currShape){
        delete[] currShape;
        currShape = NULL;
    }
    if(relevantTrans){
        delete[] relevantTrans;
        relevantTrans = NULL;
    }
}

Vect Piece::operator[](int index)
{
    int actualIdx = index+origin;
    if(index>0) actualIdx -=1;
    if( (actualIdx>=0) && (actualIdx<shapeLength) )
        return currShape[actualIdx];
    else
        return Vect();
}

void Piece::transform(Trans transformation)
{
        for(int i=0;i<shapeLength;i++){
            switch(transformation){
                case Trans::up :
                    currShape[i] = baseShape[i];
                    break;
                case Trans::right :
                    currShape[i].x = baseShape[i].y;
                    currShape[i].y = -baseShape[i].x;
                    break;
                case Trans::down :
                    currShape[i].x = -baseShape[i].x;
                    currShape[i].y = -baseShape[i].y;
                    break;
                case Trans::left :
                    currShape[i].x = -baseShape[i].y;
                    currShape[i].y = baseShape[i].x;
                    break;
                case Trans::upBack :
                    currShape[i].x = -baseShape[i].x;
                    currShape[i].y = baseShape[i].y;
                    break;
                case Trans::rightBack :
                    currShape[i].x = baseShape[i].y;
                    currShape[i].y = baseShape[i].x;
                    break;
                case Trans::downBack :
                    currShape[i].x = baseShape[i].x;
                    currShape[i].y = -baseShape[i].y;
                    break;
                case Trans::leftBack :
                    currShape[i].x = -baseShape[i].y;
                    currShape[i].y = -baseShape[i].x;
                    break;
                default:
                    cout << "Invalid transformation " << transformation << " for piece: " << to_string(value) << endl;
            }
    }
}

ostream & Piece::put(ostream & o,char sep) const
{
    return o<<"(Piece "<< to_string(value) << ")" <<sep;
}

// Puzzle board sizes definition, to be customize for other types of puzzle board
#define BXL 13 // X len of the puzzle board
#define BYL 14 // Y len of the puzzle board
#define BOX 3 // Board origin in X, to prevent pieces from spanning out of board array
#define BOY 3 // Board origin in Y, to prevent pieces from spanning out of board array
// BOX and BOY depends of the max dimension of the biggest piece
#define BDXL 7 // X span from board origin BOX to display area border
#define BDYL 8 // Y span from board origin BOY to display area boarder 
// The board display area correspond to real life puzzle board
// the board not displayed area is a technical area required to place pieces without spanning out of the array implementing the board

// Puzzle board, only the constructor needs to be customized to change the type of puzzle board
class Board
{

protected:
    int boardArray[BYL][BXL];
    Coord arrayOrigin;

    void AssignFrom(const Board& other);
    bool putPieceSquare(Board &board, int value, Coord pos);
    
public:  
    Board * next; 
    
    Board(int weekday, int monthDay, int month);
    Board(const Board& other){AssignFrom(other);}
    virtual ~Board(){}
    Board& operator=(const Board& other){AssignFrom(other);return *this;} 
    void nextAvailablePos(Coord * pos);
    Board * putPiece(Piece &piece, Coord pos);
    void print();
    virtual ostream& put(ostream & o,char sep=' ') const ;
    friend ostream& operator<<(ostream& o, const Board& p){return p.put(o);}
};

Board::Board(int weekday, int monthDay, int month)
{
    // weekday from 1 to 7 with 1=Monday..7=Sunday
    // monthDay from 1 to 31
    // month from 1 for January to 12 for december
    int x,y;
    next = NULL;
    arrayOrigin.x= BOX;
    arrayOrigin.y = BOY;
    for(x=0;x<BXL;x++){
        for(y=0;y<BYL;y++){
            boardArray[y][x] = -1;
        }
    }
    for(x=arrayOrigin.x;x<(arrayOrigin.x+BDXL);x++){
        for(y=arrayOrigin.y;y<(arrayOrigin.y+BDYL);y++){
            boardArray[y][x] = 0;
        }
    }
    boardArray[3][9] = -1;
    boardArray[4][9] = -1;
    boardArray[10][3] = -1;
    boardArray[10][4] = -1;
    boardArray[10][5] = -1;
    boardArray[10][6] = -1;
    boardArray[((month-1)/6)+3][((month-1)%6)+3] = -1;
    boardArray[((monthDay-1)/7)+5][((monthDay-1)%7)+3] = -1;
    if((weekday-1) == 6) boardArray[9][6] = -1;
    else boardArray[((weekday-1)/3)+9][((weekday-1)%3)+7] = -1;
}

void Board::AssignFrom(const Board& other)
{
    int x,y;
    next = other.next;
    arrayOrigin = other.arrayOrigin;
    for(x=0;x<BXL;x++){
        for(y=0;y<BYL;y++){
            boardArray[y][x] = other.boardArray[y][x];
         }
    }
}

void Board::nextAvailablePos(Coord * pos)
{
    int y = arrayOrigin.y;
    int x;
    bool found = false;
    while(y<(BDYL+arrayOrigin.y) && (found == false)){
        x = arrayOrigin.x;
        while(x<(BDXL+arrayOrigin.x) && (found == false)){
            if( boardArray[y][x] == 0 ){
                pos->y = y-arrayOrigin.y;
                pos->x = x-arrayOrigin.x;
                found = true;
            }
            x++;   
        }
        y++;
    }
}

bool Board::putPieceSquare(Board &board, int value, Coord pos)
{
    if( board.boardArray[board.arrayOrigin.y+pos.y][board.arrayOrigin.x+pos.x] == 0) {
        board.boardArray[board.arrayOrigin.y+pos.y][board.arrayOrigin.x+pos.x] = value;
        return true;
    }
    else return false;
}
    
Board * Board::putPiece(Piece &piece, Coord pos)
{
    Board * newBoard = new Board(*this);
    bool success;
    Coord currPos;
    int index = -1; 
    Vect currVect;
    currPos = pos;
    success = putPieceSquare(*newBoard,piece.value,currPos);
    if(success){
        currVect = piece[index];
        while(!currVect.isNull())
        {
            currPos.x = currPos.x-currVect.x;
            currPos.y= currPos.y-currVect.y;
            success = putPieceSquare(*newBoard,piece.value,currPos);
            if(!success) {
                delete newBoard;
                return NULL;
            }
            index -= 1;
            currVect = piece[index];
        }
        index = 1;
        currPos= pos;
        currVect = piece[index];
        while(!currVect.isNull())
        {
            currPos.x= currPos.x+currVect.x;
            currPos.y = currPos.y+currVect.y;
            success = putPieceSquare(*newBoard,piece.value,currPos);
            if(!success) {
                delete newBoard;
                return NULL;
            }
            index += 1;
            currVect = piece[index];
        }
    } else {
        delete newBoard;
         return NULL;
    }
    return newBoard;
}

// Print board as python list
void Board::print(void)
{
     int y,x;
     bool firstY,firstX;
     cout << "[";
     firstY = true;
     for(y=arrayOrigin.y;y<(BDYL+arrayOrigin.y);y++){
         if(firstY==true){
             cout << "[";
             firstY=false;
         } else { 
             cout << ",[";
         }
         firstX=true;
         for(x=arrayOrigin.x;x<(BDXL+arrayOrigin.x);x++){
             if(firstX==false) cout << ",";
             else firstX=false;
             cout<<to_string(boardArray[y][x]);
         }
         cout << "]";
     }
     cout << "]";
}

// Print board in ASCII art
ostream & Board::put(ostream & o,char sep) const
{
    int y,x;
    for(y=arrayOrigin.y-1;y<(BDYL+arrayOrigin.y);y++){
        for(x=arrayOrigin.x;x<(BDXL+arrayOrigin.x+1);x++){
            if( boardArray[y][x-1] != boardArray[y][x] ){
                o << "|";
           } else {
                o<<" ";
           }
           if( boardArray[y+1][x] != boardArray[y][x] ){
                o << "_";
           } else {
                o<<" ";
           }
        }
        o<<endl;
    }
    return o<<sep;
}

bool Solve(Board& board, Piece * pieces[], int nbPieces, Board ** sols,int * nbTries,int * nbPlPcs,bool printSol,bool isUniqueSol, bool &keepSearching)
{
    bool isSolution = false;
    Coord pos;
    Trans* trans;
    Board* newBoard;
    Piece ** newPieces;
    int i,j;
    int newNbPieces =  nbPieces - 1;
    if(nbPieces != 0){
        board.nextAvailablePos(&pos);
        int pIdx=0;
        while(pIdx<nbPieces && keepSearching){
            int origin=0;
            while(origin<=pieces[pIdx]->shapeLength && keepSearching){
                trans=pieces[pIdx]->relevantTrans;
                int tIdx=0;
                while(tIdx<pieces[pIdx]->nbRelevantTrans && keepSearching){
                    pieces[pIdx]->origin=origin;
                    pieces[pIdx]->transform(*trans);
                    newBoard = board.putPiece(*pieces[pIdx],pos);
                    (*nbTries)++;
                    if(newBoard){
                        (*nbPlPcs)++;
                        if(newNbPieces>0){
                            newPieces  = new Piece*[newNbPieces];
                            j=0;
                            for(i=0;i<nbPieces;i++){
                                if(i!=pIdx){
                                    newPieces[j] = pieces[i];
                                    j++;
                                }
                            }
                        } else {
                            newPieces = NULL;
                        }
                        isSolution = Solve(*newBoard,newPieces,newNbPieces,sols,nbTries,nbPlPcs,printSol,isUniqueSol,keepSearching);
                        if(isSolution != true){
                            delete newBoard;
                        }
                        if( isUniqueSol == true && isSolution == true ){
                                 keepSearching = false;
                        }
                        isSolution = false;
                        delete newPieces;
                    }
                    tIdx++;
                    trans++;
                }
                origin++;
            }
            pIdx++;
        }
    } else {
        if(*sols){
            board.next = *sols;
        }
        *sols = &board;
        isSolution = true;
        if(printSol==true){
            cout << board << endl;
        }
    }
    return isSolution;
}

void printWeekday(int weekdayNum)
{
    switch(weekdayNum){
        case 1:
            cout << "Monday";
            break;
        case 2:
            cout << "Tuesday";
            break;
        case 3:
            cout << "Wednesday";
            break;
        case 4:
            cout << "Thursday";
            break;
        case 5:
            cout << "Friday";
            break;
        case 6:
            cout << "Saturday";
            break;
        case 7:
            cout << "Sunday";
            break;
        default:
            cout << "InvalidWeekdayNum";
    }
}

void printMonth(int monthNum)
{
    switch(monthNum){
        case 1:
            cout << "January";
            break;
        case 2:
            cout << "February";
            break;
        case 3:
            cout << "March";
            break;
        case 4:
            cout << "April";
            break;
        case 5:
            cout << "May";
            break;
        case 6:
            cout << "June";
            break;
        case 7:
            cout << "July";
            break;
        case 8:
            cout << "August";
            break;
        case 9:
            cout << "September";
            break;
        case 10:
            cout << "October";
            break;
        case 11:
            cout << "November";
            break;
        case 12:
            cout << "December";
            break;
        default:
            cout << "InvalidMonthNumber";
    }
}

void printError(string msg, string arg=""){
    cerr << msg << " " << arg << endl;
}

void printHelp(string prog)
{
    cout << "Synopsis:\n\n    [weekday day month] [-h] [-u] [-i] [-s] [-t [PcsNb] [PcsNb] [PcsNb]...]\n\nDescription:\n\n    Solver for Daily Calendar Puzzle with month, day of month and day of week. Return value is 0 if at least one solution has been found or -h option is used.\n\nArguments:\n\n    weekday day month\n          Date to solve. weekday from 1=Monday to 7=Sunday, day from 1 to 31 and month from 1 to 12.\n\n    -h    Print this help\n\n    -u    Stop looking for solutions when a first one has been found\n\n    -i    Make the results appear once all of them has been found in a single line of python syntax\n\n    -s     Make the pieces be used with their smooth side up as reference side, instead their frosted side\n\n    -t    Specify which pieces can be flipped (use both sides instead reference side only)\n\n    PcsNb Number of a piece in range 1-10 added after '-t' to specify a pieces which shall be used both sides during solutions searching.\n\n          Pieces numbers are these ones:\n\n          7  7     4  4  4\n          1  7  7  7  4  2\n          1  6  6  3  4  2  2\n          1 10  6  3  3  3  2\n          1 10  6  6  9  9  9\n          8 10 10 10  9     9\n          8  8  8  8     5  5\n                      5  5  5\n\nExample\n\n    To solve Friday 23rd of January\n\n    " << prog << " 5 23 1\n" << endl;
}


int main(int argc, char* argv[])
{
    auto startTime = std::chrono::high_resolution_clock::now();
    int wdayNum = 0;
    int dayNum = 0;
    int monthNum = 0;
    int fourFlatTransLen=2;
    int smallSTransLen=2;
    int smallLTransLen=4;
    int tTransLen=4;
    int uTransLen=4;
    int bigSTransLen=2;
    int smallStailTransLen=4;
    int bigLTransLen=4;
    int qTransLen=4;
    int lEqualTransLen=4;
    bool inLine = false;
    bool fSide=true;
    Board * sols = NULL;
    Trans allTrans[8] = {Trans::up,Trans::right,Trans::down,Trans::left,Trans::upBack,Trans::rightBack,Trans::downBack,Trans::leftBack};
    Trans allFaceTrans[4] = {Trans::up,Trans::right,Trans::down,Trans::left};
    Trans upRightTrans[4] = {Trans::up,Trans::right,Trans::upBack,Trans::rightBack};
    bool isArgsValid=true;
    bool isArgValid;
    bool isHelpOpt=false;
    bool isArgPcsFlip=false;
    bool isUniqueSol=false;
    string prog(argv[0]);
    for(int i=1; i<argc;i++){
        isArgValid=false;
        string arg(argv[i]);
        if( isArgsValid && !isArgPcsFlip && (wdayNum == 0 || dayNum == 0 || monthNum == 0 ) ){
            int p;
            bool isNum=true;
            try {
                p = stoi(arg);// convert argument to a number
            } catch ( std::invalid_argument& e ){
                isNum=false;
            }
            if( isNum &&  isArgsValid && !isArgValid && wdayNum == 0 ){
                if( p>=1 && p<=7){
                    wdayNum = p;// week day number, monday=1, tuesday=2...
                    isArgValid=true;
                } else {
                    printError("Week day number out of [1-7] range:",arg);
                    isArgsValid=false;
                }
            }
            if( isNum && isArgsValid && !isArgValid && dayNum == 0 ){
                if( p>= 1 && p<=31 ){
                    dayNum = p;//day number from 1 to 31
                    isArgValid=true;
                } else {
                    printError("Month day number out of [1-31] range:",arg);
                    isArgsValid=false;
                }
            }
            if( isNum && isArgsValid && !isArgValid && monthNum == 0 ){
                if( p>= 1 && p<=12 ){
                    monthNum = p;// month number, january=1, february=2...
                    isArgValid=true;
                 } else {
                    printError("Month number out of [1-12] range:",arg);
                    isArgsValid=false;
                }
            }
        }
        if( !isArgValid && isArgsValid && arg.compare("-i")==0) {
            inLine=true;//inline python processable printing of the results
            isArgValid=true;
        }
        if( !isArgValid && isArgsValid && arg.compare("-s")==0){
            fSide=false;//front side not used, back side of pieces are the base side to use
            isArgValid=true;
        }
        if( !isArgValid && isArgsValid && arg.compare("-t")==0){
            isArgPcsFlip = true; // next arguments are pieces numbers
            isArgValid=true;
        }
        if( !isArgValid && isArgsValid && arg.compare("-u")==0){
            isUniqueSol = true;
            isArgValid=true;
        }
         if( !isArgValid && isArgsValid && arg.compare("-h")==0 ){
            isArgValid=true;
            isHelpOpt=true;
        }
        if( !isArgValid && isArgsValid && isArgPcsFlip ){
            int p;
            try {
                p = stoi(arg);// convert argument to a number to identify the piece to use on both sides
            } catch ( std::invalid_argument& e){
                printError("Invalid piece number of range [1-10]:",arg);
                isArgsValid=false;
            }
            if( p<1 || p>10){
                printError("Invalid piece number of range [1-10]:",arg);
                isArgsValid=false;
            } else {
                isArgValid=true;
            }
            switch(p){
                case 2:
                    smallSTransLen=4;
                    break;
                case 3:
                    smallLTransLen=8;
                    break;
                case 6:
                    bigSTransLen=4;
                    break;
                case 7:
                    smallStailTransLen=8;
                    break;
                case 8:
                    bigLTransLen=8;
                    break;
                case 5:
                    qTransLen=8;
                    break;
                default:
                    break;//other pieces are the same once returned, so they are not returned to avoid creating identical solutions
            }        
        }
        if( !isArgValid && isArgsValid  ){
            printError("Unkown argument:",arg);
            isArgsValid=false;
        }
    }
    if( wdayNum == 0 || dayNum == 0 || monthNum == 0 ){
        if(wdayNum == 0 && dayNum == 0 && monthNum == 0 && isArgsValid && !isHelpOpt){
            // get the current time
            auto now = std::chrono::system_clock::now();
            std::time_t time = std::chrono::system_clock::to_time_t(now);
             // get the current day of week, day in month, and month number
            std::tm* timeinfo = std::localtime(&time);
            wdayNum = timeinfo->tm_wday == 0 ? 7 : timeinfo->tm_wday;
            dayNum = timeinfo->tm_mday;
            monthNum = timeinfo->tm_mon + 1;
            cout << "No date provided, solving current date." << endl;
        } else {
            if( isArgsValid && !isHelpOpt ){
                isArgsValid = false;
                printError("Missing at least one of the following numbers : weekday day month");
            }
        }
    }
    if( !isArgsValid || isHelpOpt ) {
        printHelp(prog);
        if( isHelpOpt){
            exit(0);
        } else {
            exit(1);
        }
    } else {
        if(fSide==false){
            // update relevant transformations lists to put back side first to use it as base side
            allTrans[0] = Trans::upBack;
            allTrans[1] = Trans::rightBack;
            allTrans[2] = Trans::downBack;
            allTrans[3] = Trans::leftBack;
            allTrans[4] = Trans::up;
            allTrans[5] = Trans::right;
            allTrans[6] = Trans::down;
            allTrans[7] = Trans::left;
            allFaceTrans[0] = Trans::upBack;
            allFaceTrans[1] = Trans::rightBack;
            allFaceTrans[2] = Trans::downBack;
            allFaceTrans[3] = Trans::leftBack;
            upRightTrans[0] = Trans::upBack;
            upRightTrans[1] = Trans::rightBack;
            upRightTrans[2] = Trans::up;
            upRightTrans[3] = Trans::right;
        }
        // Create the 10 pieces      
        Vect FourFlatArray[3]= {Vect(0,1),Vect(0,1),Vect(0,1)};
        Piece FourFlat(FourFlatArray, 3, 1, upRightTrans, fourFlatTransLen);
        Vect SmallSArray[3]=  {Vect(0,1),Vect(1,0),Vect(0,1)};;
        Piece SmallS(SmallSArray, 3, 2, upRightTrans, smallSTransLen);
        Vect SmallLArray[3] =  {Vect(0,1),Vect(1,0),Vect(1,0)};
        Piece SmallL(SmallLArray, 3, 3, allTrans, smallLTransLen);
        Vect TArray[4] =  {Vect(1,0),Vect(1,0),Vect(-1,1),Vect(0,1)};
        Piece T(TArray, 4, 4, allFaceTrans, tTransLen);
        Vect QArray[4] = {Vect(0,1),Vect(1,0),Vect(0,1),Vect(-1,0)};
        Piece Q(QArray, 4, 5, allTrans, qTransLen);
        Vect BigSArray[4] = {Vect(1,0),Vect(0,1),Vect(0,1),Vect(1,0)};
        Piece BigS(BigSArray, 4, 6, upRightTrans, bigSTransLen);
        Vect SmallsTailArray[4] = {Vect(1,0),Vect(0,1),Vect(1,0),Vect(1,0)};
        Piece SmallsTail(SmallsTailArray, 4, 7, allTrans, smallStailTransLen);
        Vect BigLArray[4] = {Vect(0,1),Vect(1,0),Vect(1,0),Vect(1,0)};
        Piece BigL(BigLArray, 4, 8, allTrans, bigLTransLen);
        Vect UArray[4] = {Vect(0,1),Vect(1,0),Vect(1,0),Vect(0,-1)};
        Piece U(UArray, 4, 9, allFaceTrans, uTransLen);
        Vect LequalArray[4] = {Vect(0,1),Vect(0,1),Vect(1,0),Vect(1,0)};
        Piece Lequal(LequalArray, 4, 10, allFaceTrans, lEqualTransLen); 
       
        //  Create the board
        Board puzzle(wdayNum,dayNum,monthNum);
        // Solving
        int nbTries=0;
        int nbSols=0;
        int nbPlPcs=0;
        Board * nextSol;
        // Create the list of pieces to give to the solver
        Piece * puzzlePieces[10] = {&FourFlat,&U,&Q,&SmallsTail,&SmallL,&BigL,&SmallS,&Lequal,&BigS,&T};//this order is from the most to least frequent appearance in first case, when pieces are used on their front side, fSide=true
        if(inLine==false){
            cout << "Solutions:" << endl;
        }
        bool keepSearching = true;
        // Call the solving function
        Solve(puzzle, puzzlePieces, 10, &sols,&nbTries,&nbPlPcs,(inLine==false),isUniqueSol,keepSearching);

        if(inLine==false){
            // Print the solution as human readable
            if(sols){
                nbSols ++;
                nextSol = sols->next;
                while(nextSol){
                    nbSols++;
                    nextSol = nextSol->next;
                }
             }
            cout << nbSols << " solutions found after " << nbTries << " tries and "<<  nbPlPcs << " pieces placed for ";
            printWeekday(wdayNum);
            cout << " " << dayNum << " ";
            printMonth(monthNum);
            cout << endl;
        } else {
            // print the solution as python dict entry
            cout << "\"";
            printWeekday(wdayNum);
            cout << " " << dayNum;
            printMonth(monthNum); 
            cout << "\": { \"nbPcsPlaced\": " << nbPlPcs << ",\"nbTries\":" << nbTries << ", \"sols\": [";
            if(sols){
                (*sols).print();
                nbSols ++;
                nextSol = sols->next;
                while(nextSol){
                    cout << ",";
                    (*nextSol).print();
                    nbSols++;
                    nextSol = nextSol->next;
                }
            }
            cout  << "], \"nbSol\": " << nbSols << "}";
        }
        if(!sols){
            if(fSide){
                // turning pieces 5 is enough to get solution for all dates like wed 27 when using frosted side only, except sun 6th apr, for which another piece need to be returned
                cout << "Try with option: -t 5 2 " << endl;
            } else {
                // turning piece 5 is enough when using smooth side as reference to get a solution for all dates like mon 27th which have no solution smooth side only
                cout << "Try with option: -t 5" << endl;
            }
        }
    }
    if(inLine==false){
        auto endTime = std::chrono::high_resolution_clock::now();
        cout << "End of program reached, execution duration: " << (float)(std::chrono::duration_cast<std::chrono::milliseconds>(endTime-startTime).count())/1000 << " seconds" << endl;
    }
    if ( !sols ){
        exit(1);
    } else {
        exit(0);
    }
}
