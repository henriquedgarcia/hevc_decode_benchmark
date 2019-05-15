from ../utils import util, video_param

config = video_param.VideoParams.load_json('config.json')


def main():
    # videos = util.list_videos('input.json')

    videos = {'rollercoaster': 0,
              'lions': 0}

    for i in range(10):
        for project in ['kvazaar', 'ffmpeg']:
            v = video_param.VideoParams(project=project, scale=config['scale'], fps=config['fps'], gop=config['gop'],
                                        duration=config['duration'], yuv='yuv-10s', hevc='hevc', mp4='mp4',
                                        segment='segment', dectime='dectime')

            for v.name in config['videos_list']:
                for v.tile_format in config['tile_list']:
                    for v.rate in config['rate_list']:
                        util.decode(video=v, decoder='mp4client', factor='qp', multithread=False)


if __name__ == '__main__':
    main()
