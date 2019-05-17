#!/bin/env python3
# import sys
# sys.modules[__name__].__dict__.clear()

# import importlib
# importlib.reload(modulename)

# Início
import itertools
from utils import util


def main(argv):
    encode()


def encode():
    # Configura os objetos
    config = util.Config('config.json')
    sl = util.check_system()['sl']

    # Cria objeto "video" com suas principais pastas
    video = util.VideoParams(config=config,
                             yuv=f'..{sl}yuv-10s',
                             hevc_base='hevc',
                             mp4_base='mp4',
                             segment_base='segment',
                             dectime_base='dectime')

    my_iterator = itertools.product(['kvazaar'], config.videos_list, config.tile_list, ['rate_list', 'qp_list'])
    for factors in my_iterator:
        (video.encoder, video.name, video.tile_format, factor) = factors

        # Ignore
        if video.name in ('surf', '', '', '', '', 'clans', 'super_mario', 'ski', 'jaws', 'maldives', 'elephants',
                          'ninja_turtles', 'angels_fall', 'lion_king', 'pluto', 'ball', 'manhattan', 'venice'):
            continue

        video.project = video.encoder
        video.factor = factor.split("_")[0]

        for video.quality in getattr(config, factor):
            util.encode(video)
            util.encapsule(video)
            util.extract_tile(video)
            util.make_segments(video)


if __name__ == '__main__':
    import sys
    main(sys.argv)
