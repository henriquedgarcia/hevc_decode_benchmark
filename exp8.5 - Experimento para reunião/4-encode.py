#!/bin/env python3
import os
import subprocess
import time

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
rate_list = [2000000, 4000000, 8000000, 16000000, 24000000]
tile_list = ['1x1', '6x4', '12x8']


def main():
    programs = util.check_system()
    kvazaar = programs['kvazaar']
    sl = programs['sl']

    # videos = util.list_videos('input.json')

    videos = {"pac_man": 0,
              "rollercoaster": 0,
              "lions": 0,
              "om_non": 0}
    videos = {"om_nom": 0}

    for name in videos:
        for tile in tile_list:
            m, n = list(map(int, tile.split('x')))
            for rate, qp in list(zip(rate_list, qp_list)):
                for tile_count in range(1, (m * n) + 1):
                    folder = f'{name}_{scale}_{fps}_{tile}'
                    filename = f'{folder}_tile{tile_count}'
                    filepath_in = f'yuv{sl}{folder}{sl}{filename}.yuv'

                    os.makedirs(f'hevc{sl}{folder}', exist_ok=True)
                    filepath_out_rate = f'hevc{sl}{folder}{sl}{folder}_rate{rate}_tile{tile_count}'
                    filepath_out_qp = f'hevc{sl}{folder}{sl}{folder}_qp{qp}_tile{tile_count}'
                    params_common = (f'--input {filepath_in} '
                                     f'--input-res {scale} '
                                     f'--input-fps {fps} '
                                     f'-p {gop} '
                                     '--no-tmvp '
                                     '--no-open-gop')
                    params_rate = f'{params_common} --bitrate {rate} --output {filepath_out_rate + ".hevc"}'
                    params_qp = f'{params_common} --qp {qp} --output {filepath_out_qp + ".hevc"}'

                    if os.path.isfile(filepath_out_rate + '.hevc'):
                        print(
                            f'arquivo {filepath_out_rate + ".hevc"} existe. Pulando.')
                    else:
                        command = f'{kvazaar} {params_rate}'
                        with open(filepath_out_rate + '.log', 'w',
                                  encoding='utf-8') as f:
                            print(command)
                            subprocess.run(command, shell=True, stdout=f,
                                           stderr=subprocess.STDOUT)

                    if os.path.isfile(filepath_out_qp + '.hevc'):
                        print(
                            f'arquivo {filepath_out_qp + ".hevc"} existe. Pulando.')
                    else:
                        command = f'{kvazaar} {params_qp}'
                        with open(filepath_out_qp + '.log', 'w',
                                  encoding='utf-8') as f:
                            print(command)
                            subprocess.run(command, shell=True, stdout=f,
                                           stderr=subprocess.STDOUT)


if __name__ == '__main__':
    main()
