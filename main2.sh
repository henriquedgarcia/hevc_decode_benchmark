#!/bin/bash

# exit when any command fails
set -e

input_file=saida.mp4
size=3840x2160
fps=32
start_time=40

# prepare file list to concatenate
rm list.txt
for ((i=0; i<10; i++));do
	echo "file 'saida.mp4'" >> list.txt
done

# create 1s video
ffmpeg -ss 40 -i clans_3840x2160_30.mp4 -t 1 -r 32 -map 0:0 saida.mp4

# Concatenate 10 times 1s video
ffmpeg -f concat -i list.txt yuv/output.yuv

# Encode to HEVC tiled video
mkdir -p hevc
for gop in 32; do
for qp in 20 25 30 35 40; do
for tile in 1x1 2x3 4x6 6x9 8x12; do
	out_name="clans_"$size"_"$fps"_"$tile"_gop"$gop"_qp"$qp
	in_name="yuv/output.yuv"
	
	# Define Params
	input="--input-res="$size" --input-fps "$fps" --input $in_name"
	params="--threads 1 -p "$gop" --preset veryslow --tiles "$tile" --slices tiles --mv-constraint frametilemargin -q "$qp
	output="--output hevc/"$out_name".hevc"
	
	# Encode
	echo kvazaar $input $params $output "2>&1 |" tee hevc/"$out_name"_log.txt; echo; # read -n 1 -s    # make a pause
	kvazaar $input $params $output 2>&1 | tee hevc/"$out_name"_log.txt
	echo
done
done
done
