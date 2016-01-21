#!/bin/bash
#Author : Hemanth H.M
#Licence : GNU GPLv3

# Usage
show_help(){
echo "Usage is $0 a|m|n|c|h"
echo "-a or --all to plot cpu(c),mem(m) and net(n)"
}

# Make directory to store the results
setdir(){
mkdir -p zip_Stats
cd zip_Stats
}

# Use dstat to get the data set
gendata(){
echo "Collecting stats for sec with an interval of 60sec"
dstat -tmnc 60 > dstat.dat&
[ "$?" -ne 0 ] && echo "Please check if you have installed dstat" && exit 1
sleep 10800s
exec 2>/dev/null
kill $! >/dev/null 2>&1

#save header
head -2 dstat.dat > zip_dstat.dat

#Remove the headers
sed '1,2d' dstat.dat > body.dat

#left file
awk -F '|' '{print $1 "|" $2 "|" $3  "|"}' body.dat > left.dat
awk -F '|' '{print $4}' body.dat > tmp_right.dat
awk -F ' ' '{printf ("%3d %3d %3d %3d %3d %3d\n" ,$1*2 ,$2/2 ,100-$1*2-$2/2  ,$4  ,$5 , $6) }'  tmp_right.dat > right.dat

awk 'NR==FNR{a[NR]=$0}NR>FNR{printf("%s%s\n", a[FNR],$0)}' left.dat right.dat >> zip_dstat.dat

awk -F '|' 'BEGIN {i=0} {printf(i  $1  $2  $3 "\n")} {i=i+60}' right.dat > plot_stat.dat

}
#############################################
#MAIN BLOCK
#############################################
# Use GNU plot to plot the graph
graph (){
gnuplot << EOF
set terminal $fileType
set output $output
set title $title
set xlabel $xlabel


set xtics 0,3600,72000
#set xdata time

set ylabel $ylabel
#set timefmt "%d-%m %H:%M:%S"
#set format x "%H:%M"

plot ${plot[*]}
EOF
}

# Plot CPU usage
plotcpu(){
fileType="png"
output='"cpu.png"'
title='"cpu-usage"'
xlabel='"time"'
ylabel='"percent"'

# Using an arry presrving the '"quotes"' is very much nessary
plot=( '"plot_stat.dat"' using 1:3  title '"system"' w lines ls 1 ,'"plot_stat.dat"' using 1:2 title '"user"' w lines ls 4 ,'"plot_stat.dat"' using 1:4 title '"idle"' w lines ls 5 )
 graph
}

# Plot memory usage
plotmem(){
fileType="png"
output='"memory.png"'
title='"memory-usage"'
xlabel='"time"'
ylabel='"size(Mb)"'

plot=( '"stat.dat"' using 1:8 title '"used"' with lines,'"stat.dat"' using 1:9 title '"buff"' with lines, '"stat.dat"' using 1:10 title '"cach"' with lines,'"stat.dat"' using 1:11 title '"free"' with lines )
graph "png" '"memo.png"' '"cpu-usage"' '"time"' '"percent"' $plot
}

# Plot network usage
plotnet(){
fileType="png"
output='"network.png"'
title='"network-usage"'
xlabel='"time"'
ylabel='"size(k)"'

plot=( '"stat.dat"' using 1:11 title '"sent"' with lines,'"stat.dat"' using 1:12 title '"recvd"' with lines )

graph

}

# Clean up all the collected stats
clean(){
echo "Cleaning"
cd Stats
rm -r *.dat
echo "Done!"
}

#Check for the first input if it's zero show help
[ -z $1 ] && show_help && exit 1;

# Set dir and gen data
setdir
gendata
#wait
#clean
# Loop for different options
while [[ $1 == -* ]]; do
case "$1" in
-h|--help|-\?) show_help; exit 0;;
-a|--all) plotcpu ; plotmem ; plotnet ; exit 0;;
-m|--mem) plotmem ; exit 0 ;;
-n|--net) plotnet ; exit 0 ;;
-c|--cpu) plotcpu ; exit 0 ;;
--) shift; break;;
-*) echo "invalid option: $1"; show_help; exit 1;;
esac
done
