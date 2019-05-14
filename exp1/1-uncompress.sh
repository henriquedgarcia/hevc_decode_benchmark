#!/bin/bash
set -e  # Exit on single error

input_file=clans_3840x2160_30.mp4
intermediate_file=saida.mp4
output_file=output.yuv

size=3840x2160
fps=32
start_time=40

# echo prepare file list to concatenate
# rm list.txt
# for ((i=0; i<10; i++));do
	# echo "file 'yuv/$intermediate_file'" >> list.txt
# done

echo create 1s video
# ffmpeg -ss 40 -i $input_file -t 1 -r 32 -vf 'scale=3840x2160' -map 0:0 yuv/$intermediate_file
ffmpeg -i $input_file -t 60 -r 32 -vf 'scale=3840x2160' -map 0:0 yuv/$output_file

# echo Concatenate 10 times 1s video
# ffmpeg -f concat -i list.txt yuv/$output_file

