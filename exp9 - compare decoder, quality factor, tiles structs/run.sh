#!/bin/bash

in_name=$1
out_name=$2
i=$3

echo --------------------------------------------------------------------
echo "in_name = ${in_name}"
echo "out_name = ${out_name}"
echo --------------------------------------------------------------------

while :; do
    echo "Rodando singlethread. Rodada ${i}"
    taskset -c 0 MP4Client -bench -no-thread ${in_name} &> temp.tmp;
    exitcode=$?
    echo "exitcode == ${exitcode}."

    if [[ ${exitcode} == 0 ]]; then
        cat temp.tmp | grep tempo | tee -a ${out_name}_single.log;
		echo
        break
    fi
    #echo "Algum erro. Exitcode == ${exitcode}. Tentando novamente."
done

while :; do
    echo "Rodando multithread. Rodada ${i}"
    MP4Client -bench ${in_name} &> temp.tmp; exitcode=$?
    echo "exitcode == ${exitcode}."


    if [[ ${exitcode} == 0 ]]; then
        cat temp.tmp | grep tempo | tee -a ${out_name}_multi.log
		echo
        break;
    fi
    #echo "Algum erro. Exitcode == ${exitcode}. Tentando novamente."
done
