# Configuration
from utils import util_stats

duration = 10
scale = '4320x2160'
w, h = list(map(int, scale.split('x')))
fps = 30
gop = 30

# qp_list = [20, 30, 40]
# rate_list = [2000000, 8000000, 24000000]
# tile_list = ['2x2', '3x3', '6x3']
qp_list = [20, 25, 30, 35, 40]
rate_list = [2000000, 4000000, 8000000, 16000000, 24000000]
tile_list = ['1x1', '6x4', '12x8']


def main():
    # videos = util.list_videos('input.json')

    videos = {'rollercoaster': 0,
              'lions': 0}

    for i in range(10):
        for name in videos:
            for tile in tile_list:
                for rate, qp in list(zip(rate_list, qp_list)):
                    print(f'\n***************\n* Rodada {i}. *\n***************\n')
                    util_stats.decode(name=name, scale=scale, fps=fps, tile=tile, duration=duration, quality=rate,
                                      factor='rate')


if __name__ == '__main__':
    main()
