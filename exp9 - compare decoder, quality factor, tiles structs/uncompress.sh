#!/bin/bash
#~ set -e  # Exit on single error

size="4320x2160"
fps="30"

time[1]=0:00
name[1]=clans.mp4
time[2]=0:05
name[2]=super_mario.mp4
time[3]=1:30
name[3]=rollercoaster.mp4
time[4]=0:40
name[4]=ski.webm
time[5]=1:04
name[5]=surf.mp4
time[6]=1:49
name[6]=jaws.webm
time[7]=0:07
name[7]=lions.webm
time[8]=0:07
name[8]=maldives.mp4
time[9]=0:10
name[9]=om_nom.mp4
time[10]=0:20
name[10]=pac_man.mp4
time[11]=1:00
name[11]=elephants.mp4
time[12]=0:00
name[12]=ninja_turtles.mp4

mkdir -p yuv
for ((i=1;i<13;i++)); do
  name_out=${name[i]%.webm}
  name_out=${name_out%.mp4}
  par_in="-n -hide_banner -ss ${time[i]} -i original/${name[i]}"
  par_out="-t 60 -r ${fps} -vf scale=${size} -map 0:0"
  
  echo
  echo --------------------------------------------------------------------
  echo ffmpeg ${par_in} ${par_out} yuv/${name_out}.yuv
  echo --------------------------------------------------------------------
  echo
  #~ read -n 1 -s  # make a pause

  ffmpeg ${par_in} ${par_out} yuv/${name_out}.yuv
done
