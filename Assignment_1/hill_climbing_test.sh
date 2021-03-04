#!/bin/bash

cat << _end_ | gnuplot
set terminal postscript eps color
set output "hill_climbing_test.eps"
set key right bottom
set title "Hill Climbing method"
set xlabel "Number of cities"
set ylabel "Time (seconds)"
plot "./hill_climbing_data/data_1.txt" using 1:2 title "test_1" with lines lc "orange" lw 2,\
"./hill_climbing_data/data_2.txt" using 1:2 title "test_2" with lines lc "green" lw 2,\
"./hill_climbing_data/data_3.txt" using 1:2 title "test_3" with lines lc "purple" lw 2,\
"./hill_climbing_data/data_4.txt" using 1:2 title "test_4" with lines lc "yellow" lw 2,\
"./hill_climbing_data/data_5.txt" using 1:2 title "test_5" with lines lc "light-blue" lw 2,
_end_
