#!/bin/bash

cat << _end_ | gnuplot
set terminal postscript eps color
set output "random_simulated_annealing_test_linear.eps"
set key right bottom
set title "Random Simulated Annealing method (Linear TEMP [10-0.05])"
set xlabel "Cities"
set ylabel "Time (seconds)"
plot "./simulated_annealing_data/linear/data_1.txt" using 1:2 title "test_1" with lines lc "orange-red" lw 5,\
"./simulated_annealing_data/linear/data_2.txt" using 1:2 title "test_2" with lines lc "green" lw 5,\
"./simulated_annealing_data/linear/data_3.txt" using 1:2 title "test_3" with lines lc "dark-violet" lw 5,\
"./simulated_annealing_data/linear/data_4.txt" using 1:2 title "test_4" with lines lc "gold" lw 5,\
"./simulated_annealing_data/linear/data_5.txt" using 1:2 title "test_5" with lines lc "medium-blue" lw 5,
_end_
