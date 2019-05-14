#!/bin/env python3
import os
import shutil
from utils import util

# Configuration
proc_num = 4
duration = 10,
scale = '4320x2160'
w, h = list(map(int, scale.split('x')))
fps = 30
gop = 30

qp_list = [20, 30, 40]
rate_list = [2000000, 8000000, 24000000]
tile_list = ['1x1']


def main():
    programs = util.check_system()
    mp4box = programs['mp4box']
    sl = util.check_system()['sl']

    # videos = util.list_videos('input.json')

    videos = {"rollercoaster": 0,
              "lions": 0}

    for name in videos:
        for tile in tile_list:
            for rate, qp in list(zip(rate_list, qp_list)):
                # ----------------------------------------------
                # Encode
                # ----------------------------------------------
                yuv_video_name = f'yuv{sl}{name}_{scale}_{fps}'

                hevc_video = util.encode(name=name, scale=scale, gop=gop, fps=fps, tile=tile,
                                         yuv_video_name=yuv_video_name, quality=rate, factor='rate')

                # ----------------------------------------------
                # Encapsule
                # ----------------------------------------------
                mp4_video = util.encapsule(name=name, scale=scale, fps=fps, tile=tile, hevc_video=hevc_video,
                                           quality=rate, factor='rate')

                # ----------------------------------------------
                # Extract and segment Tiles
                # ----------------------------------------------
                util.extract_segment(name=name, scale=scale, fps=fps, tile=tile, mp4_video=mp4_video, quality=rate,
                                     factor='rate')


if __name__ == '__main__':
    main()
