# Daily Calendar Puzzle Solver

This code is designed to solve this Daily Calendar Puzzle:

![Daily Calendar Puzzle](img/poodlepuzzleDailyCalendarPuzzle.jpeg)

It's a Tetris like puzzle you need to solve differently for each day because the pieces have to fit in a grid with one square for each of the 12 months, each of the 31 days and each of the 7 days of week. Once solved, the Tetris pieces hide every squares except one for the current month, one for the current day of the month and one for the current day of the week.

This code implement the same algorithm in python and C++, even if it is more flexible and generic in its python version.

I first started with the python version, but as it requires 76 minutes to find all the solutions for one date, I tried to speed it up by using several threads (which corresponds to the version in this repository), and finally, as I needed to speed it up a lot, I implemented it again, and optimized it in C++. As a result, the computation time for the same task dropped from 76 minutes to 25 seconds.

The python code can be easily adapted to solve any Tetris like puzzle, but the C++ one is more binded to this specific puzzle (actually, the Board class constructor only is strongly binded to this specific puzzle).

Python implementation ask for the date of the puzzle to solve in a prompt.

C++ implementation takes the date in command line with 3 numbers : 

 1. week day number from 1 to 7
 2. month day number from 1 to 31 
 3. month number from 1 to 12.

C++ implementation can also print all solutions of one date in a single line formatted to be readable with python json library (option 'i'), or turn upside down some pieces when looking for solutions (add the list of pieces numbers from 1 to 10 as arguments).

This repository also contains Linux and Windows makefiles for the C++, and a bash script able to run 12 threads to look for all the solutions for 7x12x31 dates on a multicore system by using the C++ implementation and make it print the solutions in 12 files (one for each month).

Here is an example of the python code execution (configured to stop looking for other solutions when a first one has been found):

    Calendar puzzle date to solve (ex: 31/01/2022): 27/03/2023
    Start multithreads puzzle solving for Monday, 27 March 2023:
    
    Solution found by process 6 in 0:01:54 after testing 120279 combinations:
    (
    'sl'  'sl'  'Mar' 'T'   'T'   'T'   0
    'I'   'sl'  'sl'  'sl'  'T'   's'   0
    'I'   'S'   'S'   'Ls'  'T'   's'   's'
    'I'   'LL'  'S'   'Ls'  'Ls'  'Ls'  's'
    'I'   'LL'  'S'   'S'   'U'   'U'   'U'
    'L'   'LL'  'LL'  'LL'  'U'   '27'  'U'
    'L'   'L'   'L'   'L'   'Mon' 'Q'   'Q'
    0     0     0     0     'Q'   'Q'   'Q'
    )
    1 solutions for Monday, 27 March 2023 found in 0:01:57.323853 after 1144610 tries

And here is an example of the C++ implementation use for the same date (which always look for all solutions before ending execution):

    $./CamendarPuzzleSolver.bin 1 27 3
    Solutions:
      7  7 -1  4  4  4 -1
      1  7  7  7  4  2 -1
      1  6  6  3  4  2  2
      1 10  6  3  3  3  2
      1 10  6  6  9  9  9
      8 10 10 10  9 -1  9
      8  8  8  8 -1  5  5
     -1 -1 -1 -1  5  5  5
    
    1 solutions found after 3026228 tries for Monday 27  March
    End of program reached,  execution duration: 9 seconds

Well note that the date used for this example only have one solution (which can only be seen with the C++ implementation).
