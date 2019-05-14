# Configuration
import os
import shutil
import subprocess

from utils import util

duration = 10
scale = '4320x2160'
w = 4320
h = 2160
fps = 30
gop = 30


def main():
    programs = util.check_system()
    sl = programs['sl']
    mp4client = programs['mp4client']

    qp_list = [20, 25, 30, 35, 40]
    rate_list = [2000000, 4000000, 8000000, 16000000, 24000000]
    # rate_list = [8000000]
    tile_list = ['1x1', '6x4', '12x8']
    # tile_list = ['12x8']
    # videos = util.list_videos('input.json')

    # videos = {"pac_man": 0,
    #           "rollercoaster": 0,
    #           "lions": 0,
    #           "om_nom": 0}
    videos = {'rollercoaster': 0,
              'lions': 0}

    for i in range(1):
        for name in videos:
            for tile in tile_list:
                m, n = list(map(int, tile.split('x')))
                for rate, qp in list(zip(rate_list, qp_list)):
                    out_folder = f'dectime{sl}{name}_{tile}_rate{rate}'
                    os.makedirs(out_folder, exist_ok=True)

                    for t in range(1, m * n + 1):
                        for chunk in range(1, duration + 1):
                            video_path = f'dash{sl}{name}_{scale}_{fps}_{tile}_rate{rate}{sl}segments{sl}{name}_tile{t}_track{t + 1}_{chunk:03}'
                            log_path = f'{out_folder}{sl}{name}_tile{t}_{chunk:03}'

                            command = f'start /b /wait /affinity 0x800 {mp4client} -bench {video_path}.mp4'
                            print('\n' + command)

                            while True:
                                with open('temp.tmp', 'w', encoding='utf-8') as f1:
                                    p = subprocess.run(command, shell=True, stdout=f1, stderr=subprocess.STDOUT)
                                print(f'returncode = {p.returncode}')

                                if p.returncode == 0:
                                    with open('temp.tmp', 'r', encoding='utf-8') as f1, \
                                            open(f'{log_path}.log', 'a', encoding='utf-8') as f2:
                                        f2.write(f1.read())
                                        break
                                else:
                                    print(f'Algum erro. Exitcode == {p.returncode}. Tentando novamente.')

                            # command = f'{mp4client} -bench {video_path}.mp4'
                            # util.run(command, f'{video_path}_dectime_multi_thread', 'log', mode='a', overwrite=True)


if __name__ == '__main__':
    main()
