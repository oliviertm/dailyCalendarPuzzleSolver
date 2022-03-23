# Daily Calendar Puzzle Solver

This code is designed to solve Daily Calendar Puzzle

Have a look on Google for *daily calendar puzzle* and you'll see how it looks like.

It's a Tetris like puzzle you need to solve differently for each day because the pieces have to fit in a grid with one square for each of the 12 months, each of the 31 days and each of the 7 days of week. Once solved, the Tetris pieces hide every squares except one for the current month, one for the current day of the month and one for the current day of the week.

This code implement the same algorithm in python and C++, even if it is more flexible and generic in its python version.

I first started with the python version, but as it requires 76 minutes to find all the solutions for one date, I tried to speed it up by using several threads (which corresponds to the version in this repository), and finally, as I needed to speed it up a lot, I implemented it again, and optimized it in C++. As a result, the computation time for the same task dropped from 76 minutes to 25 seconds.

The python code can be easily adapted to solve any Tetris like puzzle, but the C++ one is highly binded to this specific puzzle.

Python implementation ask for the date of the puzzle to solve in a prompt.

C++ implementation takes the date in command line with 3 numbers : 

 1. week day number from 1 to 7
 2. month day number from 1 to 31 
 3. month number from 1 to 12.

C++ implementation can also print all solutions of one date in a single line formatted to be readable with python json library (option 'i'), or turn upside down some pieces when looking for solutions (add the list of pieces numbers from 1 to 10 as arguments).

This repository also contains Linux and Windows makefiles for the C++, and a bash script able to run 12 threads to look for all the solutions for 7x12x31 dates on a multicore system.
