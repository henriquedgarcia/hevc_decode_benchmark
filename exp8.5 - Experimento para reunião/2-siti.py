#!/bin/env python3
import os
import platform
import subprocess
import json

# Configuration
import time

from utils import util

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
    siti = programs['siti']

    with open('input.json', 'r') as f:
        video_list = json.load(f)

    for name in video_list:
        base_name = f'{name}_{scale}_{fps}'
        folder_in = f'yuv{sl}'

        filepath_in = f'{folder_in}{base_name}.yuv'
        filepath_out = f'{folder_in}{base_name}.log'
        params = (f'-w {w} '
                  f'-h {h} '
                  '-f 1 '
                  '-s '
                  f'-i {filepath_in}')
        command = f'{siti} {params}'
        print(command)
        with open(filepath_out, 'w') as f:
            subprocess.run(command, stdout=f, stderr=subprocess.STDOUT, encoding='utf-8')


if __name__ == '__main__':
    main()
