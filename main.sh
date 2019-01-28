#!/bin/bash

input_file=clans_3840x2160_30.mp4
size=3840x2160
fps=32
start_time=40

# This convert original vídeo to YUV420 format
# mkdir -p yuv
# for duration in 1 2 3 4 5; do	
	# name="yuv/clans_"$size"_"$fps"_"$duration"s"
	# ffmpeg -ss $start_time -i $input_file -r $fps $name.yuv
# done

# This encode YUV video in hevc tiled scheme and tiles splited in mp4 container tracks
mkdir -p mp4
mkdir -p hevc
for gop in 32 64 96 128; do
for qp in 20 25 30 35 40; do
for tile in 1x1 2x3 4x6 6x9 8x12; do
	# todo: Corrigir loop em função das novas durações
	# corrigir função de segmentação
	out_name="clans_"$size"_"$fps"_"$tile"_gop"$gop"_qp"$qp
	
	# Encode to HEVC
	input="--input-res="$size" --input-fps "$fps" --input clans_3840x2160_32.yuv"
	params="--threads 1 -p "$gop" --preset veryslow --no-open-gop --tiles "$tile" --slices tiles --mv-constraint frametilemargin -q "$qp
	output="--output hevc/"$out_name".hevc"
	echo '{ kvazaar '$input $params $output' 2> '$out_name'.txt ; } 2>> hevc/'$out_name'_log.txt'; echo
	# read -n 1 -s    # make a pause	
	kvazaar $input $params $output #2> "hevc/"$out_name"_log.txt"
	echo
	
	# Split tiles in mp4 container tracks
	echo 'MP4Box -add '$out_name'.hevc:split_tiles -new mp4/'$out_name'.mp4'
	# read -n 1 -s
	MP4Box -add hevc/"$out_name".hevc:split_tiles -new mp4/"$out_name".mp4
	echo
	
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

# measure time of decode
# read -n 1 -s
# for gop in 32 64 96 128; do
# for qp in 20 25 30 35 40; do
# for tile in 1x1 2x3 4x6 6x9 8x12; do
	# out_name="clans_"$size"_"$fps"_"$tile"_gop"$gop"_qp"$qp
	
	# for ((i = 0 ; i < 20 ; i++)); do
		# echo
		# echo $out_name is decoding $i times	
		# echo
		# { time ffmpeg -hwaccel cuvid -i $out_name -f null - 2>1; } 2>> "$out_name"_dectime_cuvid.txt
		# { time ffmpeg -i $out_name -f null - 2>1; } 2>> "$out_name"_dectime_nohwaccel.txt
	# done

# done
# done
# done




































#~ ffmpeg -y -ss 40 -i clas1280x720.mp4 -frames 120 -c:v libx265 -x265-params keyint=60:open-gop=0:qp=28 -map 0:0 clans-4s-60.hevc;
#~ ffmpeg -y -ss 40 -i clas1280x720.mp4 -frames 120 -c:v libx265 -x265-params keyint=90:open-gop=0:qp=28 -map 0:0 clans-4s-90.hevc;
#~ ffmpeg -y -ss 40 -i clas1280x720.mp4 -frames 120 -c:v libx265 -x265-params keyint=120:open-gop=0:qp=28 -map 0:0 clans-4s-120.hevc;
#~ ffmpeg -y -ss 40 -i clas1280x720.mp4 -frames 120 -r 32 clas_1280x720_30_2.yuv


#~ kvazaar --input clas_1280x720_30.yuv --bipred --no-open-gop --tiles 3x3 --slices tiles --mv-constraint frametilemargin -p 30 -q 40 --output clans_1280x720_fps30_qp28_gop64_3x3.hevc

#~ kvazaar --input clas_1280x720_30_2.yuv -p 32 --preset veryslow --no-open-gop --tiles 3x3 --slices tiles --mv-constraint frametilemargin -q 28 --output clans_1280x720_fps30_qp28_gop64_3x3.hevc

#~ ffmpeg -ss 40 -i clas1280x720.mp4 -i clans-4s-30.hevc -frames 120 -vf psnr="stats_file=stats.log"


#~ ffprobe -video_size $size -framerate $fps -show_streams clans1s.yuv > streams1s.txt

#~ ## Coletar
#~ ffprobe -video_size $size -framerate $fps -show_streams clans1s.yuv > streams1s.txt
#~ ffprobe -video_size $size -framerate $fps -show_frames clans1s.yuv > frames1s.txt

#~ ffprobe -video_size $size -framerate $fps -show_streams clans2s.yuv > streams2s.txt
#~ ffprobe -video_size $size -framerate $fps -show_frames clans2s.yuv > frames2s.txt

#~ ffprobe -video_size $size -framerate $fps -show_streams clans3s.yuv > streams3s.txt
#~ ffprobe -video_size $size -framerate $fps -show_frames clans3s.yuv > frames3s.txt

#~ ffprobe -video_size $size -framerate $fps -show_streams clans4s.yuv > streams4s.txt
#~ ffprobe -video_size $size -framerate $fps -show_frames clans4s.yuv > frames4s.txt

#~ ffprobe -video_size $size -framerate $fps -show_streams clans5s.yuv > streams5s.txt
#~ ffprobe -video_size $size -framerate $fps -show_frames clans5s.yuv > frames5s.txt


 #~ configuration: --prefix=/usr --extra-version=0ubuntu0.18.04.1 --toolchain=hardened --libdir=/usr/lib/x86_64-linux-gnu --incdir=/usr/include/x86_64-linux-gnu --enable-gpl --disable-stripping --enable-avresample --enable-avisynth --enable-gnutls --enable-ladspa --enable-libass --enable-libbluray --enable-libbs2b --enable-libcaca --enable-libcdio --enable-libflite --enable-libfontconfig --enable-libfreetype --enable-libfribidi --enable-libgme --enable-libgsm --enable-libmp3lame --enable-libmysofa --enable-libopenjpeg --enable-libopenmpt --enable-libopus --enable-libpulse --enable-librubberband --enable-librsvg --enable-libshine --enable-libsnappy --enable-libsoxr --enable-libspeex --enable-libssh --enable-libtheora --enable-libtwolame --enable-libvorbis --enable-libvpx --enable-libwavpack --enable-libwebp --enable-libx265 --enable-libxml2 --enable-libxvid --enable-libzmq --enable-libzvbi --enable-omx --enable-openal --enable-opengl --enable-sdl2 --enable-libdc1394 --enable-libdrm --enable-libiec61883 --enable-chromaprint --enable-frei0r --enable-libopencv --enable-libx264 --enable-shared
