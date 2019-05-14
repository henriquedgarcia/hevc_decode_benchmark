#!/bin/env python3
from utils import video_param


def main():
    config = video_param.VideoParams.load_json('config.json')

    for project in ['kvazaar']:
        video = video_param.VideoParams(project=project, encoder=project, decoder='mp4client', config=config, yuv='yuv',
                                        hevc='hevc',
                                        mp4='mp4', segment='segment', dectime='dectime')

        for video.name in config['videos_list']:
            video.yuv_video = f'{video.yuv}{video.sl}{config["videos_list"][video.name]}'
            for video.tile_format in config['tile_list']:
                for video.rate in config['rate_list']:
                    # video.encode(factor='rate')
                    # video.encapsule(factor='rate')
                    # video.extract_tile(factor='rate')
                    # video.make_segments(factor='rate')
                    video.decode(factor='rate', multithread=False)

                # for video.qp in config['qp_list']:
                    # video.encode(factor='qp')
                    # video.encapsule(factor='qp')
                    # video.extract_tile(factor='qp')
                    # video.make_segments(factor='qp')
                    # video.decode(factor='qp', multithread=False)


if __name__ == '__main__':
    main()
