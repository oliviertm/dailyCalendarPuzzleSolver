@echo off
REM Use http://www.mingw.org/ as C++ compiler, install it with GUI, and select all C++ package
REM Then add the installation path in PATH, e.g. C:\GCC\bin
REM And build the executable with this command
cls
g++ -std=c++11 CalendarPuzzleSolver.cpp -o CalendarPuzzleSolver.exe