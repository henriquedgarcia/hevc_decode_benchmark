#!/usr/bin/env bash
set -e

input_file=clans_3840x2160_32.yuv
size=3840x2160
fps=32

gop_list="32"
rate_list="1500000 3000000 6000000 12000000 24000000"
tile_list="1x1 2x3 4x6 6x9 8x12"

for gop in ${gop_list}; do
for rate in ${rate_list}; do
for tile in ${tile_list}; do
    folder="hevc/"${size}"_"${fps}"_"${tile}"_gop"${gop}"_rate"${rate}
	mkdir -p ${folder}

    for ((position = 0; position < 1920; position = position + 32)); do
	in_name=${input_file}
	out_name="clans_"${size}"_"${fps}"_"${tile}"_gop"${gop}"_rate"${rate}_${position}

	# Define Params
	input="--seek "${position}" -n 32 --input-res="${size}" --input-fps "${fps}" --input "${in_name}
	params="-p "${gop}" --preset veryslow --tiles "${tile}" --slices tiles --mv-constraint frametilemargin --bitrate "${rate}
	output="--output "${folder}"/"${out_name}".hevc"

	# Encode
	echo --------------------------------------------------------------------
	echo kvazaar ${input} ${params} ${output} "2>&1" | tee ${folder}"/"${out_name}_log.txt;  #read -n 1 -s    # make a pause
	echo --------------------------------------------------------------------
	kvazaar ${input} ${params} ${output} 2>&1 | tee ${folder}"/"${out_name}_log.txt
	echo
	done
done
done
done
done