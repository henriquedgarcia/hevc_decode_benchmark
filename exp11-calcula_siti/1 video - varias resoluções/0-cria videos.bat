

@REM off
ffmpeg -n -i om_nom.mp4 -qp 20 -t 10 -s 3840x1920 om_nom_3840x1920_qp20.mp4
ffmpeg -n -i om_nom.mp4 -qp 40 -t 10 -s 3840x1920 om_nom_3840x1920_qp40.mp4
ffmpeg -n -i om_nom.mp4 -qp 20 -t 10 -s 800x400 om_nom_800x400_qp20.mp4
ffmpeg -n -i om_nom.mp4 -qp 40 -t 10 -s 800x400 om_nom_800x400_qp40.mp4

@REM FOR /L %%i IN (1,1,5) DO FOR %%p IN (*.mp4) DO ffmpeg -hide_banner -nostats -benchmark -threads 1 -i %%p -f null - 1 >> %%p.txt  2>&1
