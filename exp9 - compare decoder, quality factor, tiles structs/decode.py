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
    decoders = ['ffmpeg', 'mp4client']
    threads = ['single']  # 'single' or 'multi'
    factor = ['rate', 'qp']
    
    for (video.decoder, 
         video.name, 
         video.tile_format, 
         video.factor, 
         video.threads) in itertools.product(decoders,
                                             config.videos_list,
                                             config.tile_list,
                                             factor,
                                             threads):

        video.dectime_base = f'dectime_{video.decoder}'
        video.quality_list = getattr(config, f'{video.factor}_list')
        
        for video.quality in video.quality_list:
            util.decode(video=video)


if __name__ == '__main__':
    main()
