#!/bin/bash
#set -x

size="4320x2160"
fps="30"
gop=${fps}
total_frames=$((10*gop))

videos="pac_man om_nom lions rollercoaster"
rate_list="2000000 8000000 24000000"
tile_list="1x1 2x2 3x3 6x4"
qp_list="20 30 40"

# Decode using MP4Client
for ((i=0;i<5;i++)); do
for video in ${videos}; do
for tile in ${tile_list}; do
    if [[ ${tile} == "1x1" ]]; then n_tiles=1
    elif [[ ${tile} == "2x2" ]]; then n_tiles=4
    elif [[ ${tile} == "3x3" ]]; then n_tiles=6
    elif [[ ${tile} == "6x4" ]]; then n_tiles=24
    fi
    #echo "tile == ${tile}, definindo n_tile <= ${n_tiles}"

    for ((t=1; t <= n_tiles; t++)); do
    for chunk in $(seq -f "%03g" 1 10); do
        for qp in ${qp_list}; do
            base=${video}_${size}_${fps}_${tile}_qp${qp}
            in_name=ffmpeg/segment/${base}/${base}_tile${t}_${chunk}.mp4
            out_name=ffmpeg/dectime/${base}
            mkdir -p ${out_name}
            out_name=${out_name}/${base}_tile${t}_${chunk}
#            ./run.sh ${in_name} ${out_name} ${i}
            ./run-ffmpeg.sh ${in_name} ${out_name} ${i}
#            read -n 1 -s
        done

        for rate in ${rate_list}; do
            base=${video}_${size}_${fps}_${tile}_rate${rate}
            in_name=ffmpeg/segment/${base}/${base}_tile${t}_${chunk}.mp4
            out_name=ffmpeg/dectime/${base}
            mkdir -p ${out_name}
            out_name=${out_name}/${base}_tile${t}_${chunk}
            ./run-ffmpeg.sh ${in_name} ${out_name} ${i}
#           ./run.sh ${in_name} ${out_name} ${i}
        done
    done
    done
done
done
done

size="4320x2160"
fps="30"
gop=${fps}
total_frames=$((10*gop))

videos="clans super_mario ski surf jaws maldives elephants ninja_turtles"
rate_list="2000000 8000000 24000000"
tile_list="1x1 2x2 3x3 6x4"
qp_list="20 30 40"

# Decode using MP4Client
for ((i=0;i<5;i++)); do
for video in ${videos}; do
for tile in ${tile_list}; do
    if [[ ${tile} == "1x1" ]]; then n_tiles=1
    elif [[ ${tile} == "2x2" ]]; then n_tiles=4
    elif [[ ${tile} == "3x3" ]]; then n_tiles=6
    elif [[ ${tile} == "6x4" ]]; then n_tiles=24
    fi
    #echo "tile == ${tile}, definindo n_tile <= ${n_tiles}"

    for ((t=1; t <= n_tiles; t++)); do
    for chunk in $(seq -f "%03g" 1 10); do
        for qp in ${qp_list}; do
            base=${video}_${size}_${fps}_${tile}_qp${qp}
            in_name=ffmpeg/segment/${base}/${base}_tile${t}_${chunk}.mp4
            out_name=ffmpeg/dectime/${base}
            mkdir -p ${out_name}
            out_name=${out_name}/${base}_tile${t}_${chunk}
            #./run.sh ${in_name} ${out_name} ${i}
            ./run-ffmpeg.sh ${in_name} ${out_name} ${i}
#            read -n 1 -s
        done

        for rate in ${rate_list}; do
            base=${video}_${size}_${fps}_${tile}_rate${rate}
            in_name=ffmpeg/segment/${base}/${base}_tile${t}_${chunk}.mp4
            out_name=ffmpeg/dectime/${base}
            mkdir -p ${out_name}
            out_name=${out_name}/${base}_tile${t}_${chunk}
            #./run.sh ${in_name} ${out_name} ${i}
            ./run-ffmpeg.sh ${in_name} ${out_name} ${i}
        done
    done
    done
done
done
done
