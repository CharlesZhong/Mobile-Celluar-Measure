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
echo "Collecting stats for 60sec with an interval of 10sec"
dstat -tmnc 5 > dstat.dat&
[ "$?" -ne 0 ] && echo "Please check if you have installed dstat" && exit 1
sleep 300s
exec 2>/dev/null
kill $! >/dev/null 2>&1
#Remove the headers
sed '1,2d' dstat.dat > qstat.dat
awk -F '|' 'BEGIN {i=0} {printf(i  $2  $3  $4 "\n")} {i=i+5}' qstat.dat > stat.dat
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


set xtics 0,30,300
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
plot=( '"stat.dat"' using 1:9  title '"system"' w lines ls 1 ,'"stat.dat"' using 1:8 title '"user"' w lines ls 4 ,'"stat.dat"' using 1:10 title '"idle"' w lines ls 5 )
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
