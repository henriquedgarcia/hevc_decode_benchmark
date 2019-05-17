#!/bin/env python3
# import sys
# sys.modules[__name__].__dict__.clear()

# import importlib
# importlib.reload(modulename)

# Início
import itertools
from utils import util


sl = util.check_system()['sl']


def main():
    for n in range(5):
        print(f'Rodada {n}')
        decode()


def decode():
    # Configura os objetos
    config = util.Config('config.json')
    folders = dict(yuv=f'..{sl}yuv-10s', hevc='hevc', mp4='mp4', segment='segment', dectime='ffmpeg_dectime')
    video = util.VideoParams(config=config, **folders)
    video.project = 'ffmpeg'

    my_iterator = itertools.product(['ffmpeg'], config.videos_list, config.tile_list, ['rate_list', 'qp_list'])
    for factors in my_iterator:
        (video.decoder, video.name, video.tile_format, factor) = factors

        # Ignore
        if video.name in ('surf', '', '', '', '', 'clans', 'super_mario', 'ski', 'jaws', 'maldives', 'elephants',
                          'ninja_turtles', 'angels_fall', 'lion_king', 'pluto', 'ball', 'manhattan', 'venice'):
            continue

        video.factor = factor.split("_")[0]
        for video.quality in getattr(config, factor):
            util.decode(video=video, multithread=False)


if __name__ == '__main__':
    main()
