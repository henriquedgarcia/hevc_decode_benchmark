#!/bin/bash

# exit when any command fails
set -e

input_file=om_nom.yuv
size=4320x2160
fps=32

gop_list=32
qp_list="20 25 30 35 40"
rate_list="1500000 3000000 6000000 12000000 24000000"
tile_list="1x1" # 8x12" #2x3 4x6 6x9 8x12

# Encode to HEVC tiled video
mkdir -p hevc
for gop in $gop_list; do
# for qp in $qp_list; do
for rate in $rate_list; do
for tile in $tile_list; do
	# folder=hevc/"$size"_"$fps"_"$tile"_gop"$gop"_qp"$qp"
	# mkdir -p $folder

	# for ((position=63; position < 96; i=i+gop)); do
	position=63
	in_name="$input_file"
	# out_name="clans_"$size"_"$fps"_"$tile"_gop"$gop"_qp"$qp
	out_name="clans_"$size"_"$fps"_"$tile"_gop"$gop"_"$rate"bps"
	
	# Define Params
	input="--seek "$position" -n "$gop" --input-res="$size" --input-fps "$fps" --input $in_name"
	# params="-p "$gop" --preset veryslow --tiles "$tile" --slices tiles --mv-constraint frametilemargin -q "$qp
	params="-p "$gop" --preset veryslow --tiles "$tile" --slices tiles --mv-constraint frametilemargin --bitrate "$rate
	output="--output "hevc"/"$out_name".hevc"
	
	# Encode
	echo --------------------------------------------------------------------
	echo kvazaar $input $params $output "2>&1 |" tee hevc/"$out_name"_log.txt; # read -n 1 -s    # make a pause
	echo --------------------------------------------------------------------
	kvazaar $input $params $output 2>&1 | tee hevc/"$out_name"_log.txt
	echo
	# done
done
done
done
