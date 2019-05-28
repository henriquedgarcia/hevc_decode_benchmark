#!/bin/env python3
from utils import util


def main():
    encode()


def encode():
    config = util.Config('config.json')
    sl = util.check_system()['sl']

    video = util.VideoParams(config=config,
                             yuv=f'..{sl}yuv-full',
                             hevc_base='hevc',
                             mp4_base='mp4',
                             segment_base='segment',
                             dectime_base='dectime',
                             project='ffmpeg-60s-qp',
                             encoder='ffmpeg',
                             factor='crf')

    # for video.name in config.videos_list:
    for video.name in ['om_nom', 'rollercoaster']:
        for video.tile_format in config.tile_list:
            for video.quality in getattr(config, f'{video.factor}_list'):
                util.encode(video)
                # util.make_segments(video)


if __name__ == '__main__':
    main()
