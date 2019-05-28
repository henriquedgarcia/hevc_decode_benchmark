import subprocess

from utils import util

config = util.Config('config.json')
sl = util.check_system()['sl']
video = util.VideoParams(config)

config.duration = '60'
original = f'..{sl}original'
yuv_forders_10s = f'..{sl}yuv-10s'
yuv_forders_60s = f'..{sl}yuv-full'
util.makedir(f'{yuv_forders_10s}')
util.makedir(f'{yuv_forders_60s}')
scale = config.scale
fps = config.fps

for name in config.videos_list:
    start_time = config.videos_list[name]['time']

    out_name = f'{name}_{scale}_{fps}.yuv'
    in_name = f'{original}{sl}{name}.mp4'

    par_in = f'-y -hide_banner -v quiet -ss {start_time} -i {in_name}'

    par_out_10s = f'-t 10 -r {fps} -vf scale={scale} -map 0:0 ..{sl}yuv-10s{sl}{out_name}'
    command = f'ffmpeg {par_in} {par_out_10s}'
    print(command)
    subprocess.run(command, shell=True, stderr=subprocess.STDOUT)

    par_out_60s = f'-t 60 -r {fps} -vf scale={scale} -map 0:0 ..{sl}yuv-full{sl}{out_name}'
    command = f'ffmpeg {par_in} {par_out_60s}'
    print(command)
    subprocess.run(command, shell=True, stderr=subprocess.STDOUT)

