#!/bin/env python3
from utils import util, video_param


def main():
    config = video_param.VideoParams.load_json('config.json')

    for encoder in ['ffmpeg']:
        video = video_param.VideoParams(project=encoder, encoder=encoder, config=config, yuv='yuv-10s', hevc='hevc',
                                        mp4='mp4', segment='segment', dectime='dectime')

        for video.name in config['videos_list']:
            video.yuv_video = f'{video.yuv}{video.sl}{config["videos_list"][video.name]}'
            for video.tile_format in config['tile_list']:
                for video.rate in config['rate_list']:
                    video.encode(factor='rate')
                    video.encapsule(factor='rate')
                    video.extract_tile(factor='rate')
                    video.make_segments(factor='rate')

                for video.qp in config['qp_list']:
                    video.encode(factor='qp')
                    video.encapsule(factor='qp')
                    video.extract_tile(factor='qp')
                    video.make_segments(factor='qp')
    # decode(config)


def decode(config):
    for encoder in ['kvazaar', 'ffmpeg']:
        v = video_param.VideoParams(project=encoder, encoder=encoder, config=config, yuv='yuv-10s', hevc='hevc',
                                    mp4='mp4', segment='segment', dectime='dectime')

        for v.name in config['videos_list']:
            for v.tile_format in config['tile_list']:
                for v.rate in config['rate_list']:
                    util.decode(video=v, decoder='mp4client', factor='qp', multithread=False)

                # for video.qp in config['qp_list']:
                #     util.decode(video=video, decoder='mp4client', factor='qp', multithread=False)


if __name__ == '__main__':
    main()
