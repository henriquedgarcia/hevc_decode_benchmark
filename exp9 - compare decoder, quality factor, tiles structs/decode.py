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

    # Cria objeto "video" com suas principais pastas
    video = util.VideoParams(config=config,
                             yuv=f'..{sl}yuv-10s',
                             hevc_base='hevc',
                             mp4_base='mp4',
                             segment_base='segment',
                             dectime_base='dectime')
    video.project = 'ffmpeg'

    my_iterator = itertools.product(['ffmpeg'], config.videos_list, config.tile_list, ['rate_list', 'qp_list'])
    for factors in my_iterator:
        (video.decoder, video.name, video.tile_format, factor) = factors

        # Ignore
        if video.name not in ('om_nom', 'lions', 'pac_man', 'rollercoaster'): continue

        video.factor = factor.split("_")[0]
        for video.quality in getattr(config, factor):
            util.decode(video=video, multithread=False)


if __name__ == '__main__':
    main()
