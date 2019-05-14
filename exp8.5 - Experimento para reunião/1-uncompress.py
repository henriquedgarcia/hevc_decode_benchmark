#!/bin/env python3
import os
from utils import util
import subprocess
import json
import time


# Configuration
duration = 10
scale = '4320x2160'
w = 4320
h = 2160
fps = 30
gop = 30
qp_list = [20, 25, 30, 35, 40]
# rate_list=[1500000, 3000000, 6000000, 12000000, 24000000]
rate_list = [2000000, 4000000, 8000000, 16000000, 24000000]
tile_list = ['1x1', '6x4', '12x8']


def main():
    programs = util.check_system()
    sl = programs['sl']
    ffmpeg = programs['ffmpeg']

    with open('input.json', 'r') as f:
        video_list = json.load(f)

    p_count = 0
    proc = []
    for name in video_list:
        ss = video_list[name]
        base_name = f'{name}_{scale}_{fps}'
        folder_in = f'original{sl}'
        folder_out = f'yuv{sl}'
        filepath_in = f'{folder_in}{name}.mp4'
        filepath_out = f'{folder_out}{base_name}.yuv'

        os.makedirs(folder_out, exist_ok=True)

        par_in = ('-n -hide_banner '
                  f'-ss {ss} '
                  f'-i {filepath_in}')
        par_out = (f'-t {duration} '
                   f'-r {fps} '
                   f'-vf scale={scale} '
                   '-map 0:0 '
                   f'{filepath_out}')

        command = f'{ffmpeg} {par_in} {par_out}'
        print(command + '\n')

        p = subprocess.Popen(command, stderr=subprocess.DEVNULL)
        proc.append(p)
        p_count += 1

        while p_count >= 3:
            time.sleep(1)
            print('.', end='',  flush=True)
            for p in proc:
                if p.poll() is not None:
                    print('\nConcluindo processo :')
                    proc.remove(p)
                    p_count -= 1
                    break

    for p in proc:
        p.wait()


if __name__ == '__main__':
    main()
