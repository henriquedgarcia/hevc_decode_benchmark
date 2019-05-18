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
                             yuv=f'..{sl}yuv-10s')
    
    video.project = 'ffmpeg'

    dec = ['mp4client', 'ffmpeg']
    # dec = ['mp4client']
    mt = [True, False]
    my_iterator = itertools.product(dec,
                                    config.videos_list,
                                    config.tile_list,
                                    ['rate', 'qp'],
                                    mt)
    for factors in my_iterator:
        (video.decoder, video.name, video.tile_format, video.factor, multithread) = factors

        video.dectime_base = f'dectime_{video.decoder}'
        for video.quality in getattr(config, f'{video.factor}_list'):
            util.decode(video=video, multithread=multithread)


if __name__ == '__main__':
    main()
