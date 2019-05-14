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

    videos = {"pac_man": 0}
    # "rollercoaster": 0,
    # "lions": 0,
    # "om-non": 0}

    for name in videos:
        for tile in tile_list:
            m, n = list(map(int, tile.split('x')))
            for rate, qp in list(zip(rate_list, qp_list)):
                for tile_count in range(1, (m * n) + 1):
                    basename = f'{name}_{scale}_{fps}_{tile}'
                    mp4_folder = f'mp4{sl}{basename}'

                    rate_name = f'{basename}_rate{rate}_tile{tile_count}'
                    qp_name = f'{basename}_rate{rate}_tile{tile_count}'

                    rate_dash_folder = f'{mp4_folder}{sl}rate_dash'
                    qp_dash_folder = f'{mp4_folder}{sl}qp_dash'

                    rate_ini_name = f'{rate_name}_dashinit.mp4'
                    qp_ini_name = f'{qp_name}_dashinit.mp4'

                    with open(f'{rate_dash_folder}{sl}{rate_ini_name}', 'rb') as f_rate_ini, \
                            open(f'{qp_dash_folder}{sl}{qp_ini_name}', 'rb') as f_qp_ini:

                        for chunk in range(1, duration + 1):
                            dash_rate_name = f'{basename}_rate{rate}_tile{tile_count}_dash{chunk}'
                            with open(f'{rate_dash_folder}{sl}{dash_rate_name}.m4s', 'rb') as f_rate_chunk, \
                                    open(f'{rate_dash_folder}{sl}{dash_rate_name}.mp4', 'wb') as f_rate_chunk_mp4:
                                f_rate_chunk_mp4.write(f_rate_ini.read())
                                f_rate_chunk_mp4.write(f_rate_chunk.read())

                            dash_qp_name = f'{basename}_rate{rate}_tile{tile_count}_dash{chunk}'
                            with open(f'{qp_dash_folder}{sl}{dash_qp_name}.m4s', 'rb') as f_qp_chunk, \
                                    open(f'{qp_dash_folder}{sl}{dash_qp_name}.mp4', 'wb') as f_qp_chunk_mp4:
                                f_qp_chunk_mp4.write(f_rate_ini.read())
                                f_qp_chunk_mp4.write(f_qp_chunk.read())

    if __name__ == '__main__':
        main()
