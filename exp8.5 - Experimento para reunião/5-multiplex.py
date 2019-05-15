#!/bin/env python3
import json
import os
import platform
import subprocess

from utils import util
import multiprocessing
from multiprocessing import managers

# Configuration
proc_num = 4
duration = 10,
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
    mp4box = programs['mp4box']
    sl = programs['sl']

    # videos = util.list_videos('input.json')

    videos = {"pac_man": 0,
              "rollercoaster": 0}
              #"lions": 0,
              #"om_non": 0}

    for name in videos:
        for tile in tile_list:
            m, n = list(map(int, tile.split('x')))
            for rate, qp in list(zip(rate_list, qp_list)):
                for tile_count in range(1, (m * n) + 1):
                    folder = f'{name}_{scale}_{fps}_{tile}'
                    filepath_in_rate = f'hevc{sl}{folder}{sl}{folder}_rate{rate}_tile{tile_count}'
                    filepath_in_qp = f'hevc{sl}{folder}{sl}{folder}_qp{qp}_tile{tile_count}'

                    os.makedirs(f'mp4{sl}{folder}', exist_ok=True)

                    filepath_out_rate = f'mp4{sl}{folder}{sl}{folder}_rate{rate}_tile{tile_count}'
                    filepath_out_qp = f'mp4{sl}{folder}{sl}{folder}_qp{qp}_tile{tile_count}'

                    if os.path.isfile(filepath_out_rate + '.mp4'):
                        print(f'arquivo {filepath_out_rate + ".hevc"} existe. Pulando.')
                    else:
                        command = f'{mp4box} -add {filepath_in_rate}.hevc:split_tiles -new {filepath_out_rate}.mp4'
                        print(command)
                        with open(filepath_out_rate + '.log', 'w', encoding='utf-8') as f:
                            subprocess.run(command, shell=True, stdout=f, stderr=subprocess.STDOUT)

                    if os.path.isfile(filepath_out_qp + '.mp4'):
                        print(f'arquivo {filepath_out_qp + ".hevc"} existe. Pulando.')
                    else:
                        command = f'{mp4box} -add {filepath_in_qp}.hevc:split_tiles -new {filepath_out_qp}.mp4'
                        print(command)
                        with open(filepath_out_qp + '.log', 'w', encoding='utf-8') as f:
                            subprocess.run(command, shell=True, stdout=f, stderr=subprocess.STDOUT)

                    filepath_in_rate = f'mp4{sl}{folder}{sl}{folder}_rate{rate}_tile{tile_count}'
                    filepath_in_qp = f'mp4{sl}{folder}{sl}{folder}_qp{qp}_tile{tile_count}'

                    os.makedirs(f'mp4{sl}{folder}{sl}rate_dash', exist_ok=True)
                    os.makedirs(f'mp4{sl}{folder}{sl}qp_dash', exist_ok=True)

                    filepath_out_rate = f'mp4{sl}{folder}{sl}rate_dash{sl}{folder}_rate{rate}_tile{tile_count}'
                    filepath_out_qp = f'mp4{sl}{folder}{sl}qp_dash{sl}{folder}_qp{qp}_tile{tile_count}'

                    if os.path.isfile(filepath_out_rate + '.mpd'):
                        print(f'arquivo {filepath_out_rate + ".mpd"} existe. Pulando.')
                    else:
                        command = f'{mp4box} -dash 1000 -profile live -out {filepath_out_rate}.mpd {filepath_in_rate}.mp4'
                        print(command)
                        with open(filepath_out_rate + '.log', 'w', encoding='utf-8') as f:
                            subprocess.run(command, shell=True, stdout=f, stderr=subprocess.STDOUT)

                    if os.path.isfile(filepath_out_qp + '.mpd'):
                        print(f'arquivo {filepath_out_qp + ".mpd"} existe. Pulando.')
                    else:
                        command = f'{mp4box} -dash 1000 -profile live -out {filepath_out_qp}.mpd {filepath_in_qp}.mp4'
                        print(command)
                        with open(filepath_out_qp + '.log', 'w', encoding='utf-8') as f:
                            subprocess.run(command, shell=True, stdout=f, stderr=subprocess.STDOUT)


if __name__ == '__main__':
    main()
