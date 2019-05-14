#!/bin/env python3
import os
import shutil

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
    cp = programs['cp']

    with open('input.json', 'r') as f:
        video_list = json.load(f)

    p_count = 0
    proc = []

    video_list = dict(maldives=0)

    for name in video_list:
        ss = video_list[name]
        folder_in = f'yuv{sl}'
        in_name = f'{name}_{scale}_{fps}'
        filepath_in = f'{folder_in}{in_name}.yuv'

        for tile in tile_list:

            m, n = list(map(int, tile.split('x')))
            tile_w = int(w / m)
            tile_h = int(h / n)

            folder_name = f'{in_name}_{tile}'
            folder_out = f'yuv{sl}{folder_name}'

            os.makedirs(folder_out, exist_ok=True)

            tile_count = 0

            for y in range(0, h, tile_h):
                for x in range(0, w, tile_w):
                    tile_count += 1
                    out_name = f'{folder_name}_tile{tile_count}'
                    filepath_out = f'{folder_out}{sl}{out_name}.yuv'


                    # Encode params
                    input_params = ('-hide_banner -n '
                                    f'-s {scale} '
                                    f'-framerate {fps} '
                                    f'-i {filepath_in}')

                    filter_params = f'-vf "crop=w={tile_w}:h={tile_h}:x={x}:y={y}"'

                    command = f'{ffmpeg} {input_params} {filter_params} {filepath_out}'
                    print('Processando: ' + command)

                    p = subprocess.Popen(command, shell=True, stderr=subprocess.DEVNULL)

                    proc.append(p)
                    p_count += 1

                    while p_count >= 1:
                        time.sleep(1)

                        print('.', end='', flush=True)

                        for p in proc:
                            if p.poll() is not None:
                                p_count -= 1
                                proc.remove(p)
                                print('\n\nConcluido:' + p.args + '\n\n')
                                break

    for p in proc:
        p.wait()


if __name__ == '__main__':
    main()
