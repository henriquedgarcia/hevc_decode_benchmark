#!/bin/python3
import itertools.product as it:

from utils import util


def main():
    # stats()
    graph()


def graph():
    config = util.Config('config.json')
    times = util.load_json('times.json')
    video_graph = util.VideoSegment(config=config, dectime=times)

    decoder = ['ffmpeg', 'mp4client']
    factor = ['rate', 'qp']
    multithread = ['multi', 'single']

    for (video_graph.decoder,
         video_graph.name,
         video_graph.fmt,
         video_graph.factor,
         video_graph.multithread) in it(decoder,
                                        config.videos_list,
                                        config.tile_list,
                                        factor,
                                        multithread):

        # Ignore
        if video_graph.name not in ('om_nom',
                                    'lions',
                                    'pac_man',
                                    'rollercoaster'): continue

        for video_graph.quality in getattr(config, f'{video_graph.factor}_list'):
            for tiles in range(1, video_graph.num_tiles + 1):
                video_graph.tile = tiles
                for chunks in range(1, video_graph.duration * video_graph.fps + 1):
                    video_graph.chunk = chunks

                    size = video_graph.size
                    ut = video_graph.times['ut']
                    st = video_graph.times['st']
                    rt = video_graph.times['rt']



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
    multithreads = [False, True]

    for factors in it(decoders, videos_list, tile_list, q_factors, multithreads):
        video_seg.decoder = factors[0]
        video_seg.name = factors[1]
        video_seg.fmt = factors[2]
        video_seg.factor = factors[3]
        video_seg.multithread = factors[4]
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
