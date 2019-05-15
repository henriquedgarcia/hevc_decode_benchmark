#!/bin/python3
import os
import json
import numpy as np
import matplotlib.pyplot as plt

size = '3840x2160'
fps = 32
tiles = ['1x1', '2x3', '4x6', '6x9', '8x12']
gops = [32]  # , 64, 96, 128]
qps = [20, 25, 30, 35, 40]
accells = ['none']
threads = ['0']


def main():
    collect_data()
    graph1()
    graph2()


def graph1():
    decode_time = _load_data('times.json')

    for gop in gops:
        for qp in qps:
            destiny = 'graph1_gop-qp-tile'

            plt.close()
            fig, ax = plt.subplots(figsize=(8, 8))
            w_bar = 0.2
            idx = np.array([1., 2., 3., 4., 5.])
            idx2 = np.array([1., 2., 3., 4., 5.])

            for accell in accells:
                for thread in threads:
                    real_time_mean = []
                    user_time_mean = []
                    sys_time_mean = []
                    real_time_std = []
                    user_time_std = []
                    sys_time_std = []

                    for tile in tiles:
                        real_time_mean += [np.average(decode_time[tile][str(gop)][str(qp)][accell][thread]['real_time']) / 10]
                        user_time_mean += [np.average(decode_time[tile][str(gop)][str(qp)][accell][thread]['user_time']) / 10]
                        sys_time_mean += [np.average(decode_time[tile][str(gop)][str(qp)][accell][thread]['sys_time']) / 10]

                        real_time_std += [np.std(decode_time[tile][str(gop)][str(qp)][accell][thread]['real_time']) / 10]
                        user_time_std += [np.std(decode_time[tile][str(gop)][str(qp)][accell][thread]['user_time']) / 10]
                        sys_time_std += [np.std(decode_time[tile][str(gop)][str(qp)][accell][thread]['sys_time']) / 10]

                    plt.bar(idx, sys_time_mean, width=w_bar, label='Sys Time, acc={}, threads={}'.format(accell, thread), yerr=sys_time_std)
                    plt.bar(idx, user_time_mean, width=w_bar, bottom=sys_time_mean, label='User Time, acc={}, threads={}'.format(accell, thread), yerr=user_time_std)
                    idx += w_bar
                    plt.bar(idx, real_time_mean, width=w_bar, label='Real Time, acc={}, threads={}'.format(accell, thread), yerr=real_time_std)
                    idx += w_bar + 0.01

            # aqui fica o plot do gráfico
            ax.set_xlabel('Tiles')
            ax.set_ylabel('Time (s)')
            ax.set_title('Times by tiling, gop {}, qp {}'.format(str(gop), str(qp)))
            ax.set_xticks(idx2 + 2 * w_bar)
            ax.set_xticklabels(('1x1', '2x3', '4x6', '6x9', '8x12'))
            ax.legend()

            plt.yticks(np.arange(0, 2.6, 0.25))
            plt.legend(loc='best')
            # plt.show()
            os.makedirs(destiny, exist_ok=True)
            name = destiny + '/clans_{}_{}_{}_gop{}'.format(size,
                                                            str(fps),
                                                            str(gop),
                                                            str(qp))
            fig.savefig(name)


def graph2():
    decode_time = _load_data('times.json')

    for gop in gops:
        for tile in tiles:
            destiny = 'graph2_gop-tile-qp'
            plt.close()
            fig, ax = plt.subplots(figsize=(8, 8))
            w_bar = 0.2
            idx = np.array([1., 2., 3., 4., 5.])
            idx2 = np.array([1., 2., 3., 4., 5.])

            for accell in accells:
                for thread in threads:
                    real_time_mean = []
                    user_time_mean = []
                    sys_time_mean = []
                    real_time_std = []
                    user_time_std = []
                    sys_time_std = []

                    for qp in qps:
                        real_time_mean += [np.average(decode_time[tile][str(gop)][str(qp)][accell][thread]['real_time']) / 10]
                        user_time_mean += [np.average(decode_time[tile][str(gop)][str(qp)][accell][thread]['user_time']) / 10]
                        sys_time_mean += [np.average(decode_time[tile][str(gop)][str(qp)][accell][thread]['sys_time']) / 10]

                        real_time_std += [np.std(decode_time[tile][str(gop)][str(qp)][accell][thread]['real_time']) / 10]
                        user_time_std += [np.std(decode_time[tile][str(gop)][str(qp)][accell][thread]['user_time']) / 10]
                        sys_time_std += [np.std(decode_time[tile][str(gop)][str(qp)][accell][thread]['sys_time']) / 10]

                    plt.bar(idx, sys_time_mean, width=w_bar, label='Sys Time, acc={}, threads={}'.format(accell, thread), yerr=sys_time_std)
                    plt.bar(idx, user_time_mean, width=w_bar, bottom=sys_time_mean, label='User Time, acc={}, threads={}'.format(accell, thread), yerr=user_time_std)
                    idx += w_bar
                    plt.bar(idx, real_time_mean, width=w_bar, label='Real Time, acc={}, threads={}'.format(accell, thread), yerr=real_time_std)
                    idx += w_bar + 0.01

            # aqui fica o plot do gráfico
            ax.set_xlabel('QP')
            ax.set_ylabel('Time (s)')
            ax.set_title('Times by qp, gop {}, tile {}'.format(str(gop), tile))
            ax.set_xticks(idx2 + 2 * w_bar)
            ax.set_xticklabels(('20', '25', '30', '35', '40'))
            ax.legend()

            plt.yticks(np.arange(0, 2.6, 0.25))
            plt.legend(loc='best')
            # plt.show()

            os.makedirs(destiny, exist_ok=True)
            name = destiny + '/clans_{}_{}_{}_gop{}'.format(size,
                                                            str(fps),
                                                            tile,
                                                            str(gop))
            fig.savefig(name)
            # print('ok')


def _load_data(filename='times.json'):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def collect_data():
    decode_time = {}
    for tile in tiles:
        decode_time[tile] = {}
        for gop in gops:
            decode_time[tile][gop] = {}
            for qp in qps:
                decode_time[tile][gop][qp] = {}
                for accell in accells:
                    decode_time[tile][gop][qp][accell] = {}
                    for thread in threads:
                        decode_time[tile][gop][qp][accell][thread] = {}
                        name = 'clans_{}_{}_{}_gop{}_qp{}'.format(size, str(fps),
                                                                  tile, str(gop),
                                                                  str(qp))
                        name = 'dectime/{0}_dectime_{1}_{2}.txt'.format(name,
                                                                        accell,
                                                                        thread)

                        real_time = []
                        user_time = []
                        sys_time = []

                        with open(name, 'rt') as f:
                            for line in f:
                                if line in '\n':
                                    continue
                                elif 'real' in line:
                                    real_time.append(float(line[:-2].split('m')[1].replace(',', '.')))
                                elif 'user' in line:
                                    user_time.append(float(line[:-2].split('m')[1].replace(',', '.')))
                                elif 'sys' in line:
                                    sys_time.append(float(line[:-2].split('m')[1].replace(',', '.')))

                        decode_time[tile][gop][qp][accell][thread]['real_time'] = real_time
                        decode_time[tile][gop][qp][accell][thread]['user_time'] = user_time
                        decode_time[tile][gop][qp][accell][thread]['sys_time'] = sys_time

    _save_data(decode_time)


def _save_data(average, filename='times.json'):
    import json
    with open(filename, 'w') as f:
        json.dump(average, f, indent=2)


if __name__ == "__main__":
    main()
