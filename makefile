all: CalendarPuzzleSolver.bin

clean: 
	rm -f CalendarPuzzleSolver.bin CalendarPuzzleSolver.o

CalendarPuzzleSolver.o: CalendarPuzzleSolver.cpp
	g++ -Wall -std=C++11 -o CalendarPuzzleSolver.o -c CalendarPuzzleSolver.cpp

CalendarPuzzleSolver.bin: CalendarPuzzleSolver.o
	g++ -o CalendarPuzzleSolver.bin CalendarPuzzleSolver.o
