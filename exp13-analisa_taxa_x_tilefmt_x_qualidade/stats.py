#!/bin/python3
import os
from itertools import product

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from utils import util

sl = util.check_system()['sl']


def main():
    # stats()
    # graph1()
    # graph2()
    # graph3()
    # graph4 (decodificação por vídeo 1x1 variando qualidade)
    hist()
    pass


def hist():
    """
    Fazer um histograma para cada fator que estamos avaliando
    qualidade: 2000 kbps, 24000 kbps
    fmt: 1x1, 3x2, 6x4
    video: om_nom e rollercoaster
    Total: 2 x 3 x 2 = 12 histogramas

    :return:
    """
    config = util.Config('Config.json')
    dectime = util.load_json('times.json')

    factors = (['om_nom', 'rollercoaster'],
               ['1x1', '3x2', '6x4'],
               [2000000, 24000000])

    # for name, fmt, quality in product(*factors):
    #     m, n = list(map(int, fmt.split('x')))
    #
    #     factors = (list(range(1, m * n + 1)),
    #                list(range(1, config.duration + 1)))
    #     times = []
    #     for tile, chunk in product(*factors):
    #         times.append(dectime['ffmpeg'][name][fmt]['rate'][str(quality)][str(tile)][str(chunk)]['single']['times']['ut'])

    times = [[dectime['ffmpeg'][name][fmt]['rate'][str(quality)][str(tile)][str(chunk)]['single']['times']['ut']
              for (tile, chunk) in
              product(list(range(1, list(map(int, fmt.split('x')))[0] * list(map(int, fmt.split('x')))[1] + 1)),
                      list(range(1, config.duration + 1)))]
             for (name, fmt, quality) in
             product(*factors)]


def graph3() -> None:
    """
    bar
    fmt X average_dec_time (seconds) and fmt X average_rate (Bytes)
    :return: None
    """
    dirname = 'graph3'

    config = util.Config('config.json')
    dectime = util.load_json('times.json')

    # decoders = ['ffmpeg', 'mp4client']
    factors = ['rate']
    threads = ['single']

    # for decoder in decoders:
    for name in config.videos_list:
        for factor in factors:

            for thread in threads:
                df = pd.DataFrame()
                plt.close()
                fig, ax = plt.subplots(2, 1, figsize=(8, 5))
                quality_list = getattr(config, f'{factor}_list')
                offset = 0
                for quality in quality_list:
                    average_size = []
                    std_size = []
                    average_time = []
                    std_time = []
                    width = 0.8 / len(quality_list)
                    start_position = (0.8 - width) / 2

                    for fmt in config.tile_list:
                        m, n = list(map(int, fmt.split('x')))
                        size = []
                        time = []

                        for tile in range(1, m * n + 1):
                            for chunk in range(1, config.duration + 1):
                                size.append(dectime['ffmpeg'][name][fmt][factor][str(quality)][str(tile)][str(chunk)][thread]['size'])
                                time.append(dectime['ffmpeg'][name][fmt][factor][str(quality)][str(tile)][str(chunk)][thread]['times']['ut'])

                        average_size.append(np.average(size))
                        std_size.append(np.std(size))
                        average_time.append(np.average(time))
                        std_time.append(np.std(time))

                    x = np.array(range(1, len(average_time) + 1)) - start_position + offset
                    offset += width
                    ax[0].bar(x, average_time, width=width, yerr=std_time, label=f'rate_total={quality}')
                    ax[1].bar(x, average_size, width=width, yerr=std_size, label=f'rate_total={quality}')

                    df[f'times_{name}_{quality}'] = average_time

                ax[0].set_xticklabels(config.tile_list)
                ax[0].set_xticks(np.array(range(1, len(config.tile_list) + 1)))
                ax[1].set_xticklabels(config.tile_list)
                ax[1].set_xticks(np.array(range(1, len(config.tile_list) + 1)))

                ax[0].set_xlabel('Tile')
                ax[1].set_xlabel('Tile')
                ax[0].set_ylabel('Average Time')
                ax[1].set_ylabel('Average Rate')
                ax[0].set_title(f'{name} - Times by tiles, {factor}')
                ax[1].set_title(f'{name} - Rates by tiles, {factor}')
                ax[0].set_ylim(bottom=0)
                ax[1].set_ylim(bottom=0)
                ax[0].legend(loc='upper left', ncol=1, bbox_to_anchor=(1.01, 1.0))
                ax[1].legend(loc='upper left', ncol=1, bbox_to_anchor=(1.01, 1.0))
                plt.tight_layout()
                os.makedirs(dirname, exist_ok=True)
                print(f'Salvando {dirname}{sl}{name}_{factor}.')
                fig.savefig(f'{dirname}{sl}{name}_{factor}')
                # plt.show()
                1


def graph2() -> None:
    """
    bar
    tile X average_dec_time (seconds) and tile X average_rate (Bytes)
    :return: None
    """
    dirname = 'graph2'

    config = util.Config('config.json')
    dectime = util.load_json('times.json')

    # decoders = ['ffmpeg', 'mp4client']
    factors = ['rate']
    threads = ['single']

    # for decoder in decoders:
    for name in config.videos_list:
        for factor in factors:

            for thread in threads:
                for fmt in config.tile_list:
                    m, n = list(map(int, fmt.split('x')))
                    plt.close()
                    fig, ax = plt.subplots(2, 1, figsize=(10, 5))

                    quality_list = getattr(config, f'{factor}_list')
                    offset = 0
                    for quality in quality_list:
                        average_size = []
                        std_size = []
                        average_time = []
                        std_time = []

                        width = 0.8 / len(quality_list)
                        start_position = (0.8 - width) / 2

                        for tile in range(1, m * n + 1):
                            size = []
                            time = []

                            for chunk in range(1, config.duration + 1):
                                size.append(dectime['ffmpeg'][name][fmt][factor][str(quality)][str(tile)][str(chunk)][thread]['size'])
                                time.append(dectime['ffmpeg'][name][fmt][factor][str(quality)][str(tile)][str(chunk)][thread]['times']['ut'])

                            average_size.append(np.average(size))
                            std_size.append(np.std(size))
                            average_time.append(np.average(time))
                            std_time.append(np.std(time))

                        x = np.array(range(1, len(average_time) + 1)) - start_position + offset
                        offset += width

                        if factor in 'rate':
                            quality = int(quality / (m * n))

                        ax[0].bar(x, average_time, width=width, yerr=std_time, label=f'quality={quality}_corr={np.corrcoef(x=(average_time, average_size))[1][0]}')
                        ax[1].bar(x, average_size, width=width, yerr=std_size, label=f'quality={quality}_ffmpeg')

                    ax[0].set_xlabel('Tile')
                    ax[1].set_xlabel('Tile')
                    ax[0].set_ylabel('Average Time')
                    ax[1].set_ylabel('Average Rate')
                    ax[0].set_title(f'{name} - Times by tiles, tile={fmt}, {factor}')
                    ax[1].set_title(f'{name} - Rates by tiles, tile={fmt}, {factor}')
                    ax[0].set_ylim(bottom=0)
                    ax[1].set_ylim(bottom=0)
                    ax[0].legend(loc='upper left', ncol=1, bbox_to_anchor=(1.01, 1.0))
                    ax[1].legend(loc='upper left', ncol=1, bbox_to_anchor=(1.01, 1.0))
                    plt.tight_layout()
                    os.makedirs(dirname, exist_ok=True)
                    print(f'Salvando {dirname}{sl}{name}_{fmt}_{factor}.')
                    fig.savefig(f'{dirname}{sl}{name}_{fmt}_{factor}')
                    # plt.show()
                    1


def graph1() -> None:
    """
    chunks X dec_time (seconds) and chunks X file_size (Bytes)
    :return:
    """
    dirname = 'graph1'

    config = util.Config('config.json')
    dectime = util.load_json('times.json')

    # decoders = ['ffmpeg', 'mp4client']
    factors = ['rate']
    threads = ['single']

    # for decoder in decoders:
    for name in config.videos_list:
        for factor in factors:
            for quality in getattr(config, f'{factor}_list'):
                quality = np.array(quality)
                for thread in threads:
                    for fmt in config.tile_list:
                        m, n = list(map(int, fmt.split('x')))
                        plt.close()
                        fig, ax = plt.subplots(1, 2, figsize=(18, 6))

                        for tile in range(1, m * n + 1):
                            size = []
                            time_ffmpeg = []
                            # time_mp4client = []

                            for chunk in range(1, config.duration + 1):
                                size.append(dectime['ffmpeg'][name][fmt][factor][str(quality)][str(tile)][str(chunk)][thread]['size'])
                                time_ffmpeg.append(dectime['ffmpeg'][name][fmt][factor][str(quality)][str(tile)][str(chunk)][thread]['times']['ut'])
                                # time_mp4client.append(dectime['mp4client'][name][fmt][factor][str(quality)][str(tile)][str(chunk)][thread]['times'])

                            ax[0].plot(time_ffmpeg, label=f'ffmpeg_tile={tile}_ffmpeg')
                            # ax[0][1].plot(time_mp4client, label=f'tile={tile}')
                            ax[1].plot(size, label=f'tile={tile}')
                            # ax[1][1].plot(time_ffmpeg, label=f'ffmpeg_tile={tile}_ffmpeg')
                            # ax[1][1].plot(time_mp4client, label=f'mp4client_tile={tile}_mp4client')

                        quality_ind = quality
                        if factor in 'rate':
                            quality_ind = int(quality / (m * n))

                        ax[0].set_xlabel('Chunks')
                        # ax[0][1].set_xlabel('Chunks')
                        ax[1].set_xlabel('Chunks')
                        # ax[1][1].set_xlabel('Chunks')
                        ax[0].set_ylabel('Time')
                        # ax[0][1].set_ylabel('Time')
                        # ax[1][1].set_ylabel('Time')
                        ax[1].set_ylabel('Rate')
                        ax[0].set_title(f'ffmpeg - {name} - Times by chunks, tile={fmt}, {factor}={quality_ind}')
                        # ax[0][1].set_title(f'mp4client {name} - Times by chunks, tile={fmt}, {factor}={quality_ind}')
                        ax[1].set_title(f'{name} - Rates by chunks, tile={fmt}, {factor}={quality_ind}')
                        # ax[1][1].set_title(f'mp4client x ffmpeg - {name} - Times by chunks, tile={fmt}, {factor}={quality_ind}')
                        # ax[0].set_ylim(bottom=0)
                        # ax[1].set_ylim(bottom=0)
                        ax[1].set_ylim(bottom=0)
                        # ax[1][1].set_ylim(bottom=0)
                        # ax[0][1].legend(loc='upper left', ncol=2, bbox_to_anchor=(1.01, 1.0))
                        ax[1].legend(loc='upper left', ncol=2, bbox_to_anchor=(1.01, 1.0))
                        plt.tight_layout()
                        # plt.()
                        os.makedirs(dirname, exist_ok=True)
                        print(f'Salvando {dirname}{sl}{name}_{fmt}_{factor}={quality_ind}.')
                        fig.savefig(f'{dirname}{sl}{name}_{fmt}_{factor}={quality_ind}')
                        # fig.show()
                        1


def stats():
    # Configura os objetos
    config = util.Config('config.json')

    # Base object
    video_seg = util.VideoSegment(config=config)
    video_seg.project = 'ffmpeg'
    video_seg.segment_base = 'segment'

    # To iterate
    decoders = ['ffmpeg', 'mp4client']
    videos_list = config.videos_list
    tile_list = config.tile_list
    q_factors = ['rate', 'qp']
    multithreads = ['single']
    times = dict()
    for factors in product(decoders, videos_list, tile_list, q_factors, multithreads):
        video_seg.decoder = factors[0]
        video_seg.name = factors[1]
        video_seg.fmt = factors[2]
        video_seg.factor = factors[3]
        video_seg.thread = factors[4]
        video_seg.dectime_base = f'dectime_{video_seg.decoder}'

        video_seg.quality_list = getattr(config, f'{video_seg.factor}_list')

        for video_seg.quality in video_seg.quality_list:
            times = util.collect_data(video_seg=video_seg)

    util.save_json(times, 'times.json')

    # graph_chunk_X_time_X_tile_rate()
    # graph2()
    # graph3()


#
#
#
# class Graph:
#     """
#     datalist é um dicionário com dicionários com dicionário com listas com dicionário com lista
#
#     um plot de uma linha possui uma legenda pra linha e dados com informações sobre os eixos:
#
#     Uma figura possui um título e várias linhas
#
#     datalist = {'fig1': {title: 'title of picture',
#                          lines: [{label: 'line label 1'
#                                   data: {x_leg: 'x axis legend',
#                                          x_axis: [x1, x2, ...],
#                                          y_leg: 'x axis legend',
#                                          y_axis: [y1, y2, ...]
#                                         },
#                                  {label: 'line label 2'
#                                   data: {x_leg: 'x axis legend',
#                                          x_axis: [x1, x2, ...],
#                                          y_leg: 'x axis legend',
#                                          y_axis: [y1, y2, ...]
#                                         },
#                            ...
#                            },
#                 'title2: ...,
#                 }
#
#         title é o título do grafico
#         line é a legenda da linha
#         eixo_x_leg e eixo_y_leg são as legendas dos eixos
#
#     :type datalist: dict(dict(dict(list())))
#     :param datalist:
#     :return:
#     """
#     w_bar = 0.2
#     idx = np.array([1., 2., 3., 4., 5.])
#
#     for title in datalist:
#         plt.close()
#         fig, ax = plt.subplots(1, 1, figsize=(8, 5))
#
#         line: dict
#         for line in datalist[title]:
#             x = line['x_axis']
#             y = line['y_axis']
#             ax.plot(x, y, label=line[')
#
#
# def graph_chunk_X_time_X_tile_rate():
#     decode_time = load_data('times.json')
#     destiny = 'graph_chunk_X_time_X_tile_rate'
#     os.makedirs(destiny, exist_ok=True)
#
#     # ctx = itertools.product(videos, range(1, m * n + 1), rate_list)
#
#     for (name) in videos:
#         for (rate) in rate_list:
#             for tile in tile_list:
#                 m, n = list(map(int, tile.split('x')))
#
#                 time = {}
#                 size = {}
#
#                 for (t) in range(1, m * n + 1):
#                     time[t] = []
#                     size[t] = []
#
#                     for chunk in range(1, duration + 1):
#                         chunk_time = (decode_time[name][tile][str(rate)][str(t)][str(chunk)]['time'])
#                         chunk_time = list(map(float, chunk_time))
#                         chunk_time = np.average(chunk_time)
#                         time[t].append(30 / float(chunk_time))
#                         chunk_size = float(decode_time[name][tile][str(rate)][str(t)][str(chunk)]['size'])
#                         size[t].append(chunk_size * 8)
#
#                     ax1.plot(time[t], label=f'tile={t}')
#                     ax2.plot(size[t], label=f'tile={t}')
#                 ax1.set_xlabel('Chunks')
#                 ax2.set_xlabel('Chunks')
#                 ax1.set_ylabel('Time')
#                 ax2.set_ylabel('Rate')
#                 ax1.set_title(f'{name} - Times by chunks, tile={tile}, rate={rate}')
#                 ax2.set_title(f'{name} - Rates by chunks, tile={tile}, rate={rate}')
#                 ax1.set_ylim(bottom=0)
#                 ax2.set_ylim(bottom=0)
#                 # ax1.legend(loc='upper center', ncol=int((m * n) / int((m *n)/6), bbox_to_anchor=(0.5, -0.25))
#                 # ax2.legend(loc='upper center', ncol=int((m * n) / int((m *n)/6), bbox_to_anchor=(0.5, -0.25))
#                 # plt.tight_layout()
#                 # plt.show()
#                 fig.savefig(f'{destiny}{sl}{name}_{rate}_{tile}')
#
#
# def graph2():
#     decode_time = load_data('times.json')
#     destiny = 'graph2_tileXtime_tile-rate'
#     os.makedirs(destiny, exist_ok=True)
#
#     # ctx = itertools.product(videos, range(1, m * n + 1), rate_list)
#     ref = [0, 0]
#     for (name) in videos:
#         for (rate) in rate_list:
#             for tile in tile_list:
#                 m, n = list(map(int, tile.split('x')))
#                 plt.close()
#
#                 fig, [ax1, ax2, ax3] = plt.subplots(3, 1, figsize=(8, 12))
#
#                 average_time = []
#                 average_size = []
#                 std_time = []
#                 std_size = []
#                 for (t) in range(1, m * n + 1):
#                     time = []
#                     size = []
#                     for chunk in range(1, duration + 1):
#                         chunk_time = (decode_time[name][tile][str(rate)][str(t)][str(chunk)]['time'])
#                         chunk_time = list(map(float, chunk_time))
#                         chunk_time = np.average(chunk_time)
#
#                         time.append(30 / float(chunk_time))
#                         chunk_size = float(decode_time[name][tile][str(rate)][str(t)][str(chunk)]['size'])
#                         size.append(chunk_size * 8)
#
#                     average_time.append(np.average(time))
#                     average_size.append(np.average(size))
#                     std_time.append(np.std(time))
#                     std_size.append(np.std(size))
#
#                 if tile in '1x1':
#                     ref[0] = average_time
#                     ref[1] = average_size
#
#                 x = list(range(1, (m * n) + 1))
#                 ax1.bar(x, average_time, yerr=std_time)
#                 ax1.plot(x, [ref[0]] * ((m * n)), 'g')
#
#                 ax2.bar(x, average_size, yerr=std_size)
#
#                 ax3.bar(x, average_size, yerr=std_size)
#                 ax3.plot(x, [ref[1]] * ((m * n)), 'g')
#                 ax3.plot(x, [np.sum(average_size)] * ((m * n)), 'b')
#
#                 ax1.set_xlabel('Tile')
#                 ax2.set_xlabel('Tile')
#                 ax3.set_xlabel('Tile')
#                 ax1.set_ylabel('Time')
#                 ax2.set_ylabel('Rate')
#                 ax3.set_ylabel('Rate')
#                 ax1.set_title(f'{name} - Times by Tile, tile={tile}, rate={rate}')
#                 ax2.set_title(f'{name} - Rates by Tile, tile={tile}, rate={rate}')
#                 ax3.set_title(f'{name} - Rates by Tile (compare), tile={tile}, rate={rate}')
#                 if tile in '1x1':
#                     ax1.set_xlim(left=0, right=2)
#                     ax2.set_xlim(left=0, right=2)
#                     ax3.set_xlim(left=0, right=2)
#                 ax1.set_ylim(bottom=0)
#                 ax2.set_ylim(bottom=0)
#                 ax3.set_ylim(bottom=0)
#                 # ax1.legend(loc='upper center', ncol=int((m * n) / int((m *n)/6), bbox_to_anchor=(0.5, -0.25))
#                 # ax2.legend(loc='upper center', ncol=int((m * n) / int((m *n)/6), bbox_to_anchor=(0.5, -0.25))
#                 # plt.tight_layout()
#                 # plt.show()
#                 fig.savefig(f'{destiny}{sl}{name}_{rate}_{tile}')
#
#
# def graph3():
#     # Esta função calcular apenas a taxa dos chunks com qp, já que não os tiles não foram decodificados.
#     decode_time = load_data('times.json')
#     destiny = 'graph2_tileXtime_tile-rate'
#     os.makedirs(destiny, exist_ok=True)
#
#     # ctx = itertools.product(videos, range(1, m * n + 1), rate_list)
#     ref = [0, 0]
#     for (name) in videos:
#         for (qp) in qp_list:
#             for tile in tile_list:
#                 m, n = list(map(int, tile.split('x')))
#
#                 plt.close()
#                 fig, [ax1, ax2, ax3] = plt.subplots(3, 1, figsize=(8, 12))
#
#                 average_time = []
#                 average_size = []
#                 std_time = []
#                 std_size = []
#                 for (t) in range(1, m * n + 1):
#                     time = []
#                     size = []
#                     for chunk in range(1, duration + 1):
#                         [chunk_time] = (decode_time[name][tile][str(rate)][str(t)][str(chunk)]['time'])
#                         time.append(30 / float(chunk_time))
#                         chunk_size = float(decode_time[name][tile][str(rate)][str(t)][str(chunk)]['size'])
#                         size.append(chunk_size * 8)
#
#                     average_time.append(np.average(time))
#                     average_size.append(np.average(size))
#                     std_time.append(np.std(time))
#                     std_size.append(np.std(size))
#
#                 if tile in '1x1':
#                     ref[0] = average_time
#                     ref[1] = average_size
#                 else:
#                     x = list(range(1, (m * n) + 1))
#                     ax1.bar(x, average_time, yerr=std_time)
#                     ax1.plot(x, [ref[0]] * ((m * n)), 'g')
#
#                 ax2.bar(x, average_size, yerr=std_size)
#
#                 ax3.bar(x, average_size, yerr=std_size)
#                 ax3.plot(x, [ref[1]] * ((m * n)), 'g')
#                 ax3.plot(x, [np.sum(average_size)] * ((m * n)), 'b')
#
#                 ax1.set_xlabel('Tile')
#                 ax2.set_xlabel('Tile')
#                 ax3.set_xlabel('Tile')
#                 ax1.set_ylabel('Time')
#                 ax2.set_ylabel('Rate')
#                 ax3.set_ylabel('Rate')
#                 ax1.set_title(f'{name} - Times by Tile, tile={tile}, rate={rate}')
#                 ax2.set_title(f'{name} - Rates by Tile, tile={tile}, rate={rate}')
#                 ax3.set_title(f'{name} - Rates by Tile (compare), tile={tile}, rate={rate}')
#                 if tile in '1x1':
#                     ax1.set_xlim(left=0, right=2)
#                     ax2.set_xlim(left=0, right=2)
#                     ax3.set_xlim(left=0, right=2)
#                 ax1.set_ylim(bottom=0)
#                 ax2.set_ylim(bottom=0)
#                 ax3.set_ylim(bottom=0)
#                 # ax1.legend(loc='upper center', ncol=int((m * n) / int((m *n)/6), bbox_to_anchor=(0.5, -0.25))
#                 # ax2.legend(loc='upper center', ncol=int((m * n) / int((m *n)/6), bbox_to_anchor=(0.5, -0.25))
#                 # plt.tight_layout()
#                 # plt.show()
#                 fig.savefig(f'{destiny}{sl}{name}_{rate}_{tile}')

# def load_data(filename='times.json'):
#     with open(filename, 'r') as f:
#         data = json.load(f)
#     return data
#
#
# def collect_data():
#     decode_time = {}
#
#     for name in videos:
#         decode_time[name] = {}
#
#         for tile in tile_list:
#             decode_time[name][tile] = {}
#             m, n = list(map(int, tile.split('x')))
#
#             for rate, qp in list(zip(rate_list, qp_list)):
#                 decode_time[name][tile][rate] = {}
#
#                 for t in range(1, m * n + 1):
#                     decode_time[name][tile][rate][t] = {}
#
#                     for chunk in range(1, duration + 1):
#                         decode_time[name][tile][rate][t][chunk] = {}
#                         decode_time[name][tile][rate][t][chunk]['time'] = []
#                         decode_time[name][tile][rate][t][chunk]['size'] = 0
#                         # basename_qp = f'{name}_{scale}_{fps}_{tile}_qp{quality}'
#                         basename_rate = f'{name}_{scale}_{fps}_{tile}_rate{rate}'
#
#                         dectime_folder_rate = f'dectime{sl}{basename_rate}'
#                         log_path = f'{dectime_folder_rate}{sl}{basename_rate}_tile{t}_{chunk:03}'
#                         video_path = f'dash{sl}{basename_rate}{sl}{basename_rate}_tile{t}_{chunk:03}'
#
#                         size = os.path.getsize(video_path + '.mp4')
#                         decode_time[name][tile][rate][t][chunk]['size'] = size
#                         with open(log_path + '.log', 'r') as f:
#                             for line in f:
#                                 ix = line.find('frames FPS')
#                                 if ix > 0:
#                                     ix += 11
#                                     time = line[ix:ix + 6].split(' ')[0]
#                                     decode_time[name][tile][rate][t][chunk]['time'].append(time)
#                                     print(f'{basename_rate}_tile{t}_{chunk:03} = time: [{time}], size: {size}')
#
#     _save_data(decode_time, filename=f'times.json')
#
#
# def _save_data(decode_time, filename='times.json'):
#     import json
#     with open(filename, 'w') as f:
#         json.dump(decode_time, f, indent=2)
#

if __name__ == "__main__":
    main()
