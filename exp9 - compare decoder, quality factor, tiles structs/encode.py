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

    # Cria um iterador produto carnesiano de todos os parametros da caracterização
    my_iterator = itertools.product(['kvazaar', 'ffmpeg'],
                                    config.videos_list,
                                    config.tile_list,
                                    ['rate', 'qp'])

    # Itera sobre o iterador
    for factors in my_iterator:
        # Define atributos básicos
        video.encoder = factors[0]
        video.project = video.encoder
        video.name = factors[1]
        video.tile_format = factors[2]
        video.factor = factors[3]

        # Para cada qualidade
        for video.quality in getattr(config, f'{video.factor}_list'):
            util.encode(video)
            util.encapsule(video)
            util.extract_tile(video)
            util.make_segments(video)


if __name__ == '__main__':
    import sys

    main(sys.argv)
