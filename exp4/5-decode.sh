#!/bin/bash

#input_file=clans_3840x2160_30.mp4
input_file=saida.mp4
size=3840x2160
fps=32

gop_list=32
qp_list="20 40" #25 30 35 40
tile_list="1x1 8x12" #2x3 4x6 6x9 8x12

# measure time of decode
mkdir -p dectime

for ((i = 1 ; i < 51 ; i++)); do
for gop in $gop_list; do
for qp in $qp_list; do
for tile in $tile_list; do
	out_name="clans_"$size"_"$fps"_"$tile"_gop"$gop"_qp"$qp	
	in_name="hevc/"$out_name".hevc"

	echo
	echo Decoding $in_name $i times	

	for hw in cuvid none vaapi; do
	for t in 0 1; do
		echo accel= $hw, threads=$t
		{ time ffmpeg -v quiet -stats -threads $t -hwaccel $hw -i $in_name -threads 1 -f null - ; } 2>> dectime/"$out_name"_dectime_"$hw"_"$t".txt
		
	done
	done
done
done
done
done





