#!/bin/bash

# exit when any command fails
#~ set -e

name[1]=clans
name[2]=super_mario
name[3]=rollercoaster
name[4]=ski
name[5]=surf
name[6]=jaws
name[7]=lions
name[8]=maldives
name[9]=om_nom
name[10]=pac_man
name[11]=elephants
name[12]=ninja_turtles

mkdir -p mp4
size="4320x2160"
fps="30"
gop=${fps}
total_frames=$((60*gop))

rate_list="1500000 3000000 6000000 12000000 24000000"
tile_list="1x1 6x4 12x8"

# Multiplex hevc in MP4 container
for ((i=1;i<13;i++)); do 		# Para cada vídeo
for tile in ${tile_list}; do	# Para cada tile
for rate in ${rate_list}; do	# para cada taxa
    # Std name
    out_name="${name[i]}_${size}_${fps}_${tile}_rate${rate}"

    # Criando pasta
    segment_folder=segment/${out_name}
    new_folder=decode/${out_name}
    mkdir -p ${new_folder}
    echo "Criando pasta $new_folder"

    # Define o numero de tiles em função da segmentação espacial
    if [[ ${tile} == "1x1" ]]; then
        n_tiles=1
        echo "tile == ${tile}, definindo n_tile <= ${n_tiles}"
    elif [[ ${tile} == "6x4" ]]; then
        n_tiles=25
        echo "tile == ${tile}, definindo n_tile <= ${n_tiles}"
    elif [[ ${tile} == "12x8" ]]; then
        n_tiles=97
        echo "tile == ${tile}, definindo n_tile <= ${n_tiles}"
    fi

    # Para cada chunk
	for ((frame=0; frame < total_frames; frame=frame+gop)); do
		chunk=$((frame/gop))

        # Para cada tile
		for ((t=1; t <= n_tiles; t++)); do
		    file_tile=${segment_folder}/${out_name}_tile${t}_chunk${chunk}.mp4

            # Se Encontrar o tile no container pule ele, senão, remova ele.
            if [[ ${tile} != "1x1" && "1" == ${t} ]]; then
                echo "Pulando o tile 1 de um video não 1x1."
                echo --------------------------------------------------------------------
                echo
                #read -n 1 -s  # make a pause
                continue
            else
                echo "Decodificando do arquivo ${out_name}_tile${t}_chunk${chunk}.mp4"
                echo --------------------------------------------------------------------
                echo "taskset -c 0 MP4Client -bench ${file_tile} 2| tee -a   ${segment_folder}/${out_name}_tile${t}_chunk${chunk}.log"
                echo --------------------------------------------------------------------
                #read -n 1 -s  # make a pause
                taskset -c 0 MP4Client -bench ${file_tile} 2| tee -a  ${segment_folder}/${out_name}_tile${t}_chunk${chunk}.log
                echo
            fi
		done
	done
done
done
done

































#!/bin/bash

input_file=clans_3840x2160_30.mp4
size=3840x2160
fps=32
start_time=40

# This encode YUV video in hevc tiled scheme and tiles splited in mp4 container tracks
# measure time of decode
read -n 1 -s
for gop in 32 64 96 128; do
for qp in 20 25 30 35 40; do
for tile in 1x1 2x3 4x6 6x9 8x12; do
	out_name="clans_"$size"_"$fps"_"$tile"_gop"$gop"_qp"$qp

	for ((i = 0 ; i < 20 ; i++)); do
		echo
		echo $out_name is decoding $i times	
		echo
		{ time ffmpeg -hwaccel cuvid -i $out_name -f null - 2>1; } 2>> "$out_name"_dectime_cuvid.txt
		{ time ffmpeg -i $out_name -f null - 2>1; } 2>> "$out_name"_dectime_nohwaccel.txt
	done

done
done
done




































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
