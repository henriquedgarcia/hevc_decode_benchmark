import os

from utils import util, video_param

config = video_param.VideoParams.load_json('config.json')
videos = util.list_videos('input.json')
sl = util.check_system()['sl']

duration = '60'
original = 'original'
yuv_forders = 'yuv-full'
os.makedirs(f'{yuv_forders}', exist_ok=True)

for name in ['ninja_turtles', 'jaws']:
    start_time = videos[name]
    par_in = f'-n -hide_banner -ss {start_time} -i ..{sl}{original}{sl}{name}.mp4'
    par_out = f'-t {duration} -r {config["fps"]} -vf scale={config["scale"]} -map 0:0 {yuv_forders}{sl}{name}.yuv'
    command = f'ffmpeg {par_in} {par_out}'
    # os.system(command)
    util.run(command, f'{yuv_forders}{sl}{name}', 'yuv', log_mode=None)
