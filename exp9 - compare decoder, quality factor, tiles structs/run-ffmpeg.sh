#!/bin/bash

in_name=$1
out_name=$2
i=$3

echo --------------------------------------------------------------------
echo "in_name = ${in_name}"
echo "out_name = ${out_name}"
echo --------------------------------------------------------------------

echo "Rodando singlethread. Rodada ${i}"
{ time taskset -c 0 ffmpeg -loglevel quiet -i ${in_name} -f null -; } &> temp.tmp
cat temp.tmp | tee -a ${out_name}_single.log;
echo

echo "Rodando multithread. Rodada ${i}"
{ time ffmpeg -loglevel quiet -i ${in_name} -f null -; } &> temp.tmp
cat temp.tmp | tee -a ${out_name}_multi.log
echo
