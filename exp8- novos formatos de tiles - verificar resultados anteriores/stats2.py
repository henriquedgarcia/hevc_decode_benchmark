#!/bin/python3
import itertools
import os
import json
import numpy as np
import matplotlib.pyplot as plt

from utils import util

duration = 10
scale = '4320x2160'
w, h = list(map(int, scale.split('x')))
fps = 30
gop = 30
proc_num = 4

qp_list = [20, 30, 40]
rate_list = [2000000, 8000000, 24000000]
tile_list = ['1x1', '2x2', '3x3', '6x3']

sl = util.check_system()['sl']

videos = {'rollercoaster': 0,
          'lions': 0}


def main():
    collect_data()
    # grafico do tamanho do tiles pelo tempo
    graph1()
    graph2()
    # graph3()


def graph1():
    decode_time = _load_data('times.json')
    destiny = 'graph1_chunkXtime_tile-rate'
    os.makedirs(destiny, exist_ok=True)

    # ctx = itertools.product(videos, range(1, m * n + 1), rate_list)

    for (name) in videos:
        for (rate) in rate_list:
            for tile in tile_list:
                m, n = list(map(int, tile.split('x')))

                w_bar = 0.2
                idx = np.array([1., 2., 3., 4., 5.])
                plt.close()
                fig, [ax1, ax2] = plt.subplots(2, 1, figsize=(8, 8))

                time = {}
                size = {}

                for (t) in range(1, m * n + 1):
                    time[t] = []
                    size[t] = []

                    for chunk in range(1, duration + 1):
                        chunk_time = (decode_time[name][tile][str(rate)][str(t)][str(chunk)]['time'])
                        chunk_time = list(map(float, chunk_time))
                        chunk_time = np.average(chunk_time)
                        time[t].append(30 / float(chunk_time))
                        chunk_size = float(decode_time[name][tile][str(rate)][str(t)][str(chunk)]['size'])
                        size[t].append(chunk_size * 8)

                    ax1.plot(time[t], label=f'tile={t}')
                    ax2.plot(size[t], label=f'tile={t}')
                ax1.set_xlabel('Chunks')
                ax2.set_xlabel('Chunks')
                ax1.set_ylabel('Time')
                ax2.set_ylabel('Rate')
                ax1.set_title(f'{name} - Times by chunks, tile={tile}, rate={rate}')
                ax2.set_title(f'{name} - Rates by chunks, tile={tile}, rate={rate}')
                ax1.set_ylim(bottom=0)
                ax2.set_ylim(bottom=0)
                # ax1.legend(loc='upper center', ncol=int((m * n) / int((m *n)/6), bbox_to_anchor=(0.5, -0.25))
                # ax2.legend(loc='upper center', ncol=int((m * n) / int((m *n)/6), bbox_to_anchor=(0.5, -0.25))
                # plt.tight_layout()
                # plt.show()
                fig.savefig(f'{destiny}{sl}{name}_{rate}_{tile}')


def graph2():
    decode_time = _load_data('times.json')
    destiny = 'graph2_tileXtime_tile-rate'
    os.makedirs(destiny, exist_ok=True)

    # ctx = itertools.product(videos, range(1, m * n + 1), rate_list)
    ref = [0, 0]
    for (name) in videos:
        for (rate) in rate_list:
            for tile in tile_list:
                m, n = list(map(int, tile.split('x')))
                plt.close()

                fig, [ax1, ax2, ax3] = plt.subplots(3, 1, figsize=(8, 12))

                average_time = []
                average_size = []
                std_time = []
                std_size = []
                for (t) in range(1, m * n + 1):
                    time = []
                    size = []
                    for chunk in range(1, duration + 1):
                        chunk_time = (decode_time[name][tile][str(rate)][str(t)][str(chunk)]['time'])
                        chunk_time = list(map(float, chunk_time))
                        chunk_time = np.average(chunk_time)

                        time.append(30 / float(chunk_time))
                        chunk_size = float(decode_time[name][tile][str(rate)][str(t)][str(chunk)]['size'])
                        size.append(chunk_size * 8)

                    average_time.append(np.average(time))
                    average_size.append(np.average(size))
                    std_time.append(np.std(time))
                    std_size.append(np.std(size))

                if tile in '1x1':
                    ref[0] = average_time
                    ref[1] = average_size

                x = list(range(1, (m * n) + 1))
                ax1.bar(x, average_time, yerr=std_time)
                ax1.plot(x, [ref[0]] * ((m * n)), 'g')

                ax2.bar(x, average_size, yerr=std_size)

                ax3.bar(x, average_size, yerr=std_size)
                ax3.plot(x, [ref[1]] * ((m * n)), 'g')
                ax3.plot(x, [np.sum(average_size)] * ((m * n)), 'b')

                ax1.set_xlabel('Tile')
                ax2.set_xlabel('Tile')
                ax3.set_xlabel('Tile')
                ax1.set_ylabel('Time')
                ax2.set_ylabel('Rate')
                ax3.set_ylabel('Rate')
                ax1.set_title(f'{name} - Times by Tile, tile={tile}, rate={rate}')
                ax2.set_title(f'{name} - Rates by Tile, tile={tile}, rate={rate}')
                ax3.set_title(f'{name} - Rates by Tile (compare), tile={tile}, rate={rate}')
                if tile in '1x1':
                    ax1.set_xlim(left=0, right=2)
                    ax2.set_xlim(left=0, right=2)
                    ax3.set_xlim(left=0, right=2)
                ax1.set_ylim(bottom=0)
                ax2.set_ylim(bottom=0)
                ax3.set_ylim(bottom=0)
                # ax1.legend(loc='upper center', ncol=int((m * n) / int((m *n)/6), bbox_to_anchor=(0.5, -0.25))
                # ax2.legend(loc='upper center', ncol=int((m * n) / int((m *n)/6), bbox_to_anchor=(0.5, -0.25))
                # plt.tight_layout()
                # plt.show()
                fig.savefig(f'{destiny}{sl}{name}_{rate}_{tile}')


def graph3():
    # Esta função calcular apenas a taxa dos chunks com qp, já que não os tiles não foram decodificados.
    decode_time = _load_data('times.json')
    destiny = 'graph2_tileXtime_tile-rate'
    os.makedirs(destiny, exist_ok=True)

    # ctx = itertools.product(videos, range(1, m * n + 1), rate_list)
    ref = [0, 0]
    for (name) in videos:
        for (qp) in qp_list:
            for tile in tile_list:
                m, n = list(map(int, tile.split('x')))

                plt.close()
                fig, [ax1, ax2, ax3] = plt.subplots(3, 1, figsize=(8, 12))

                average_time = []
                average_size = []
                std_time = []
                std_size = []
                for (t) in range(1, m * n + 1):
                    time = []
                    size = []
                    for chunk in range(1, duration + 1):
                        [chunk_time] = (decode_time[name][tile][str(rate)][str(t)][str(chunk)]['time'])
                        time.append(30 / float(chunk_time))
                        chunk_size = float(decode_time[name][tile][str(rate)][str(t)][str(chunk)]['size'])
                        size.append(chunk_size * 8)

                    average_time.append(np.average(time))
                    average_size.append(np.average(size))
                    std_time.append(np.std(time))
                    std_size.append(np.std(size))

                if tile in '1x1':
                    ref[0] = average_time
                    ref[1] = average_size
                else:
                    x = list(range(1, (m * n) + 1))
                    ax1.bar(x, average_time, yerr=std_time)
                    ax1.plot(x, [ref[0]] * ((m * n)), 'g')

                ax2.bar(x, average_size, yerr=std_size)

                ax3.bar(x, average_size, yerr=std_size)
                ax3.plot(x, [ref[1]] * ((m * n)), 'g')
                ax3.plot(x, [np.sum(average_size)] * ((m * n)), 'b')

                ax1.set_xlabel('Tile')
                ax2.set_xlabel('Tile')
                ax3.set_xlabel('Tile')
                ax1.set_ylabel('Time')
                ax2.set_ylabel('Rate')
                ax3.set_ylabel('Rate')
                ax1.set_title(f'{name} - Times by Tile, tile={tile}, rate={rate}')
                ax2.set_title(f'{name} - Rates by Tile, tile={tile}, rate={rate}')
                ax3.set_title(f'{name} - Rates by Tile (compare), tile={tile}, rate={rate}')
                if tile in '1x1':
                    ax1.set_xlim(left=0, right=2)
                    ax2.set_xlim(left=0, right=2)
                    ax3.set_xlim(left=0, right=2)
                ax1.set_ylim(bottom=0)
                ax2.set_ylim(bottom=0)
                ax3.set_ylim(bottom=0)
                # ax1.legend(loc='upper center', ncol=int((m * n) / int((m *n)/6), bbox_to_anchor=(0.5, -0.25))
                # ax2.legend(loc='upper center', ncol=int((m * n) / int((m *n)/6), bbox_to_anchor=(0.5, -0.25))
                # plt.tight_layout()
                # plt.show()
                fig.savefig(f'{destiny}{sl}{name}_{rate}_{tile}')


def _load_data(filename='times.json'):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def collect_data():
    decode_time = {}

    for name in videos:
        decode_time[name] = {}

        for tile in tile_list:
            decode_time[name][tile] = {}
            m, n = list(map(int, tile.split('x')))

            for rate, qp in list(zip(rate_list, qp_list)):
                decode_time[name][tile][rate] = {}

                for t in range(1, m * n + 1):
                    decode_time[name][tile][rate][t] = {}

                    for chunk in range(1, duration + 1):
                        decode_time[name][tile][rate][t][chunk] = {}
                        decode_time[name][tile][rate][t][chunk]['time'] = []
                        decode_time[name][tile][rate][t][chunk]['size'] = 0
                        # basename_qp = f'{name}_{scale}_{fps}_{tile}_qp{quality}'
                        basename_rate = f'{name}_{scale}_{fps}_{tile}_rate{rate}'

                        dectime_folder_rate = f'dectime{sl}{basename_rate}'
                        log_path = f'{dectime_folder_rate}{sl}{basename_rate}_tile{t}_{chunk:03}'
                        video_path = f'dash{sl}{basename_rate}{sl}{basename_rate}_tile{t}_{chunk:03}'

                        size = os.path.getsize(video_path + '.mp4')
                        decode_time[name][tile][rate][t][chunk]['size'] = size
                        with open(log_path + '.log', 'r') as f:
                            for line in f:
                                ix = line.find('frames FPS')
                                if ix > 0:
                                    ix += 11
                                    time = line[ix:ix + 6].split(' ')[0]
                                    decode_time[name][tile][rate][t][chunk]['time'].append(time)
                                    print(f'{basename_rate}_tile{t}_{chunk:03} = time: [{time}], size: {size}')

    _save_data(decode_time, filename=f'times.json')


def _save_data(decode_time, filename='times.json'):
    import json
    with open(filename, 'w') as f:
        json.dump(decode_time, f, indent=2)


if __name__ == "__main__":
    main()
