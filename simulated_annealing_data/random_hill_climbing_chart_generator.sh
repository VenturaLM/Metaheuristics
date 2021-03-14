#!/bin/bash

cat << _end_ | gnuplot
set terminal postscript eps color
set output "random_hill_climbing_test.eps"
set key right bottom
set title "Random Hill Climbing method"
set xlabel "Cities"
set ylabel "Time (seconds)"
plot "./random_hill_climbing_data/data_1.txt" using 1:2 title "test_1" with lines lc "orange-red" lw 5,\
"./random_hill_climbing_data/data_2.txt" using 1:2 title "test_2" with lines lc "green" lw 5,\
"./random_hill_climbing_data/data_3.txt" using 1:2 title "test_3" with lines lc "dark-violet" lw 5,\
"./random_hill_climbing_data/data_4.txt" using 1:2 title "test_4" with lines lc "gold" lw 5,\
"./random_hill_climbing_data/data_5.txt" using 1:2 title "test_5" with lines lc "medium-blue" lw 5,
_end_
