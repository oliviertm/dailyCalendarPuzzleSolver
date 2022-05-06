#!/bin/bash

if [ $# -eq 0 ]; then
    CNT=0
    while [ $CNT -ne 12 ]
    do
        CNT=$(expr $CNT + 1)
        ./multiThreads.sh ${CNT} &
    done
    echo "All threads has been launched"
fi

if [ $# -eq 1 ]; then
    WDAY=0
    START=true
    FILENAME=Month_$1.txt
    echo '{' > $FILENAME
    while [ $WDAY -ne 7 ]
    do
        WDAY=$(expr $WDAY + 1)
        DAY=0
        while [ $DAY -ne 31 ]
        do
            DAY=$(expr $DAY + 1)
            if [ $START == false ]
            then
                echo "," >> $FILENAME
            else
                START=false
            fi
            ./poodlepuzzleDailyCalendarSolver.bin $WDAY $DAY $1 i >> $FILENAME
        done
    done
    echo '}' >> $FILENAME
fi
