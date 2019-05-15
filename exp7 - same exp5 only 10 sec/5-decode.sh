#!/bin/bash

size="4320x2160"
fps="30"
gop=${fps}
total_frames=$((60*gop))

videos="pac_man clans super_mario rollercoaster ski surf jaws lions maldives om_nom elephants ninja_turtles"
rate_list="2000000 4000000 8000000 16000000 24000000"
tile_list="1x1 6x4 12x8"
qp_list="20 25 30 35 40"

# Decode using MP4Client
for ((i=0;i<1;i++)); do
for video in ${videos}; do 		# Para cada vídeo
for tile in ${tile_list}; do	# Para cada tile
    # Define o numero de tiles em função da segmentação espacial
    if [[ ${tile} == "1x1" ]]; then
        n_tiles=1
    elif [[ ${tile} == "6x4" ]]; then
        n_tiles=24
    elif [[ ${tile} == "12x8" ]]; then
        n_tiles=96
    fi
    #echo "tile == ${tile}, definindo n_tile <= ${n_tiles}"
    for rate in ${rate_list}; do	# para cada taxa

#        for qp in ${qp_list}; do
#            in_name="dash/"${video}"_"${size}"_"${fps}"_"${tile}"_qp"${qp}"/segments/"${video}"_tile"${t}"_track"$((t+1))"_"${chunk}".mp4"
#            out_name="dectime/"${video}"_"${size}"_"${fps}"_"${tile}"_qp"${qp}"_tile"${t}"_"${chunk}
#            echo --------------------------------------------------------------------
#            echo "in_name = ${in_name}"
#            echo "out_name = ${out_name}"
#            echo --------------------------------------------------------------------
#
#            while :; do
#            #read -n 1 -s
#                echo "Rodando singlethread. Rodada ${i}"
#                taskset -c 0 MP4Client -bench -no-thread ${in_name} &> temp.tmp; exitcode=$?
#                echo "exitcode == ${exitcode}."
#
#                if [[ ${exitcode} == 0 ]]; then
#                    echo
#                    cat temp.tmp >> ${out_name}_single.log;
#                    break
#                fi
#                echo "Algum erro. Exitcode == ${exitcode}. Tentando novamente."
#            done
#
#            while :; do
#                echo "rodando multithread. Rodada ${i}"
#                MP4Client -bench ${in_name} &> temp.tmp; exitcode=$?
#                echo "exitcode == ${exitcode}."
#
#                if [[ ${exitcode} == 0 ]]; then
#                    echo
#                    cat temp.tmp >> ${out_name}_multi.log
#                    break;
#                fi
#                echo "Algum erro. Exitcode == ${exitcode}. Tentando novamente."
#            done
#        done

        for ((t=1; t <= n_tiles; t++)); do
        for chunk in $(seq -f "%03g" 1 60); do
            in_name="dash/"${video}"_"${size}"_"${fps}"_"${tile}"_rate"${rate}"/segments/"${video}"_tile"${t}"_track"$((t+1))"_"${chunk}".mp4"
            out_folder="dectime/${video}_${tile}_rate${rate}"
            out_name="${out_folder}/${video}_tile${t}_${chunk}.log"
            mkdir -p ${out_folder}

            echo --------------------------------------------------------------------
            echo "in_name = ${in_name}"
            echo "out_name = ${out_name}"
            echo --------------------------------------------------------------------

            while :; do
            #read -n 1 -s
                echo "Rodando singlethread. Rodada ${i}"
                taskset -c 0 MP4Client -bench -no-thread ${in_name} &> temp.tmp; exitcode=$?
                echo "exitcode == ${exitcode}."

                if [[ ${exitcode} == 0 ]]; then
                    echo
                    cat temp.tmp >> ${out_name}_single.log;
                    break
                fi
                echo "Algum erro. Exitcode == ${exitcode}. Tentando novamente."
            done

#            while :; do
#                echo "rodando multithread. Rodada ${i}"
#                MP4Client -bench ${in_name} &> temp.tmp; exitcode=$?
#                echo "exitcode == ${exitcode}."
#
#                if [[ ${exitcode} == 0 ]]; then
#                    echo
#                    cat temp.tmp >> ${out_name}_multi.log
#                    break;
#                fi
#                echo "Algum erro. Exitcode == ${exitcode}. Tentando novamente."
#            done
        done
    done
    done
done
done
done