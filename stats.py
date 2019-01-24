#!/bin/python3
import numpy as np

size = '3840x2160'
fps = 32
tiles = ['1x1', '2x3', '4x6', '6x9', '8x12']
gops = [32, 64, 96, 128]
qps = [20, 25, 30, 35, 40]
accells = ['nohwaccel', 'cuvid']


def main():
    # collect_data()
    make_graphs()


def make_graphs():
    import matplotlib.pyplot as plt
    time_data = _load_data('times.json')

    for gop in gops:
        for qp in qps:
            plt.close()
            fig, ax = plt.subplots(figsize=(8, 5))
            # plt.figure(figsize=(8, 5))
            w_bar = 0.2
            idx = np.array([1., 2., 3., 4., 5.]) #  - 2 * w_bar

            for accell in accells:
                real_time = []
                user_time = []
                sys_time = []

                for tile in tiles:
                    real_time += [time_data[tile][str(gop)][str(qp)][accell]['real_time']]
                    user_time += [time_data[tile][str(gop)][str(qp)][accell]['user_time']]
                    sys_time += [time_data[tile][str(gop)][str(qp)][accell]['sys_time']]

                p_user = plt.bar(idx, user_time, width=w_bar)
                p_sys = plt.bar(idx, sys_time, width=w_bar, bottom=user_time, label='User Time ' + accell)
                idx += w_bar
                p_real = plt.bar(idx, real_time, width=w_bar)
                idx += w_bar

                # plt.legend((p_sys, p_user, p_real),
                #            ('System Time ' + accell,
                #             'User Time ' + accell,
                #             'Real Time ' + accell))

            # aqui fica o plot do gráfico
            ax.set_xlabel('Tiles')
            ax.set_ylabel('Time (s)')
            ax.set_title('Times by tiling')
            ax.set_xticks(idx + w_bar / 2)
            ax.set_xticklabels(('1x1', '2x3', '4x6', '6x9', '8x12'))
            ax.legend()


            plt.ylabel('Time (s)')
            plt.title('Times by tiling')
            plt.xticks(idx, )
            ax.set_xticks(index + bar_width / 2)
            plt.yticks(np.arange(0, 0.2, 0.020))
            plt.legend(bbox_to_anchor=(1.05, 1),
                       loc='upper left',
                       borderaxespad=0.)
            plt.show()
            print('ok')


def collect_data():
    average = {}

    for tile in tiles:
        average[tile] = {}
        for gop in gops:
            average[tile][gop] = {}
            for qp in qps:
                average[tile][gop][qp] = {}
                for accell in accells:
                    average[tile][gop][qp][accell] = {}
                    name = 'clans_{}_{}_{}_gop{}_qp{}'.format(size, str(fps),
                                                              tile, str(gop),
                                                              str(qp))
                    name = 'dectime/' + name + '_dectime_' + accell + '.txt'

                    real_time = []
                    user_time = []
                    sys_time = []

                    with open(name, 'rt') as f:
                        for line in f:
                            if line in '\n':
                                continue
                            elif 'real' in line:
                                real_time.append(float(line[:-2].split('m')[1]))
                            elif 'user' in line:
                                user_time.append(float(line[:-2].split('m')[1]))
                            elif 'sys' in line:
                                sys_time.append(float(line[:-2].split('m')[1]))

                    average[tile][gop][qp][accell]['real_time'] = np.average(real_time)
                    average[tile][gop][qp][accell]['user_time'] = np.average(user_time)
                    average[tile][gop][qp][accell]['sys_time'] = np.average(sys_time)

    _save_data(average)


def _save_data(average, filename='times.json'):
    import json
    with open(filename, 'w') as f:
        json.dump(average, f, indent=2)


def _load_data(filename='times.json'):
    import json
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


if __name__ == "__main__":
    main()
