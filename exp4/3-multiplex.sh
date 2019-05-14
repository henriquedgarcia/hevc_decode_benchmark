#!/bin/bash
# exit when any command fails
set -e

#input_file=clans_3840x2160_30.mp4
input_file=saida.mp4
size=3840x2160
fps=32

gop_list=32
qp_list="20 40" #25 30 35 40
tile_list="1x1 8x12" #2x3 4x6 6x9 8x12

# Split tiles in ISO mp4 tracks
mkdir -p mp4

for gop in $gop_list; do
for qp in $qp_list; do
for tile in $tile_list; do
	out_name="clans_"$size"_"$fps"_"$tile"_gop"$gop"_qp"$qp
	# duration=$((gop/32))
	# in_name="yuv/clans_"$size"_"$fps"_"$duration"s.yuv"
	# in_name="yuv/output.yuv"
	
	# Encode to HEVC
	# input="--input-res="$size" --input-fps "$fps" --input $in_name"
	# params="--threads 1 -p "$gop" --preset veryslow --tiles "$tile" --slices tiles --mv-constraint frametilemargin -q "$qp
	# output="--output hevc/"$out_name".hevc"
	# echo kvazaar $input $params $output "2>&1 |" tee hevc/"$out_name"_log.txt
	# echo
	# read -n 1 -s    # make a pause
	# kvazaar $input $params $output 2>&1 | tee hevc/"$out_name"_log.txt
	# echo

	# echo 'MP4Box -add '$out_name'.hevc:split_tiles -new mp4/'$out_name'.mp4'
	# read -n 1 -s
	MP4Box -add hevc/"$out_name".hevc:split_tiles -new mp4/"$out_name".mp4
	# echo

	# Segment mp4 in dash segments
	# out_name="clans_"$size"_"$fps"_"$tile"_gop"$gop"_qp"$qp
	# time=$((1000*gop/32))
	# echo 
	# echo mkdir -p "$out_name"
	# echo MP4Box -dash $time -profile live -out "$out_name"/clans.mpd $out_name.mp4
	# read -n 1 -s
	# mkdir -p "$out_name"
	# MP4Box -dash "$time" -profile live -out "$out_name"/clans.mpd "$out_name".mp4
	# echo
done
done
done
