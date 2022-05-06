all: poodlepuzzleDailyCalendarSolver.bin

clean: 
	rm -f poodlepuzzleDailyCalendarSolver.bin poodlepuzzleDailyCalendarSolver.o

poodlepuzzleDailyCalendarSolver.o: poodlepuzzleDailyCalendarSolver.cpp
	g++ -Wall -std=c++11 -o poodlepuzzleDailyCalendarSolver.o -c poodlepuzzleDailyCalendarSolver.cpp

poodlepuzzleDailyCalendarSolver.bin: poodlepuzzleDailyCalendarSolver.o
	g++ -o poodlepuzzleDailyCalendarSolver.bin poodlepuzzleDailyCalendarSolver.o
