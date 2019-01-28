#!/bin/python3
import os

import numpy as np

size = '3840x2160'
fps = 32
tiles = ['1x1', '2x3', '4x6', '6x9', '8x12']
gops = [32, 64, 96, 128]
qps = [20, 25, 30, 35, 40]
accells = ['nohwaccel', 'cuvid']


def main():
    # collect_data()
    graph1()
    # graph1a()
    # graph2()
    # graph2a()
    # graph3()
    # graph3a()
    # graph4()
    # graph4a()
    # graph5()
    # graph5a()
    # graph6()
    # graph6a()

def graph6():
    import matplotlib.pyplot as plt
    time_data = _load_data('times.json')

    for tile in tiles:
        for qp in qps:
            destiny = 'graph6_tile-qp-gop'
            plt.close()
            fig, ax = plt.subplots(figsize=(8, 5))
            w_bar = 0.2
            idx = np.array([1., 2., 3., 4.])
            idx2 = np.array([1., 2., 3., 4.])

            for accell in accells:
                real_time = []
                user_time = []
                sys_time = []

                for gop in gops:
                    real_time += [time_data[tile][str(gop)][str(qp)][accell]['real_time']]
                    user_time += [time_data[tile][str(gop)][str(qp)][accell]['user_time']]
                    sys_time += [time_data[tile][str(gop)][str(qp)][accell]['sys_time']]

                plt.bar(idx, sys_time, width=w_bar, label='Sys Time ' + accell)
                plt.bar(idx, user_time, width=w_bar, bottom=sys_time, label='User Time ' + accell)
                idx += w_bar
                plt.bar(idx, real_time, width=w_bar, label='Real Time ' + accell)
                idx += w_bar + 0.01

            # aqui fica o plot do gráfico
            ax.set_xlabel('GOP')
            ax.set_ylabel('Time (s)')
            ax.set_title('Times by GOP, tile {}, qp {}'.format(tile, str(qp)))
            ax.set_xticks(idx2 + 2 * w_bar)
            ax.set_xticklabels(('32', '64', '96', '128'))
            ax.legend()


            plt.yticks(np.arange(0, 0.2, 0.020))
            plt.legend(bbox_to_anchor=(1.05, 1),
                       loc='upper left',
                       borderaxespad=0.)
            #plt.show()

            os.makedirs(destiny, exist_ok=True)
            name = destiny + '/clans_{}_{}_{}_qp{}'.format(size,
                                                           str(fps),
                                                           tile,
                                                           str(qp))
            fig.savefig(name)
            print('ok')


def graph5():
    import matplotlib.pyplot as plt
    time_data = _load_data('times.json')

    for tile in tiles:
        for gop in gops:
            destiny = 'graph5_tile-gop-qp'
            plt.close()
            fig, ax = plt.subplots(figsize=(8, 5))
            w_bar = 0.2
            idx = np.array([1., 2., 3., 4., 5.])
            idx2 = np.array([1., 2., 3., 4., 5.])

            for accell in accells:
                real_time = []
                user_time = []
                sys_time = []

                for qp in qps:
                    real_time += [time_data[tile][str(gop)][str(qp)][accell]['real_time']]
                    user_time += [time_data[tile][str(gop)][str(qp)][accell]['user_time']]
                    sys_time += [time_data[tile][str(gop)][str(qp)][accell]['sys_time']]

                plt.bar(idx, sys_time, width=w_bar, label='Sys Time ' + accell)
                plt.bar(idx, user_time, width=w_bar, bottom=sys_time, label='User Time ' + accell)
                idx += w_bar
                plt.bar(idx, real_time, width=w_bar, label='Real Time ' + accell)
                idx += w_bar + 0.01

            # aqui fica o plot do gráfico
            ax.set_xlabel('QP')
            ax.set_ylabel('Time (s)')
            ax.set_title('Times by QP, tile {}, gop {}'.format(tile, str(gop)))
            ax.set_xticks(idx2 + 2 * w_bar)
            ax.set_xticklabels(('20', '25', '30', '35', '40'))
            ax.legend()

            plt.yticks(np.arange(0, 0.2, 0.020))
            plt.legend(bbox_to_anchor=(1.05, 1),
                       loc='upper left',
                       borderaxespad=0.)
            #plt.show()

            os.makedirs(destiny, exist_ok=True)
            name = destiny + '/clans_{}_{}_{}_gop{}'.format(size,
                                                            str(fps),
                                                            tile,
                                                            str(gop))
            fig.savefig(name)
            print('ok')


def graph4():
    import matplotlib.pyplot as plt
    time_data = _load_data('times.json')

    for qp in qps:
        for tile in tiles:
            destiny = 'graph4_qp-tile-gop'
            plt.close()
            fig, ax = plt.subplots(figsize=(8, 5))
            w_bar = 0.2
            idx = np.array([1., 2., 3., 4.])
            idx2 = np.array([1., 2., 3., 4.])

            for accell in accells:
                real_time = []
                user_time = []
                sys_time = []

                for gop in gops:
                    real_time += [time_data[tile][str(gop)][str(qp)][accell]['real_time']]
                    user_time += [time_data[tile][str(gop)][str(qp)][accell]['user_time']]
                    sys_time += [time_data[tile][str(gop)][str(qp)][accell]['sys_time']]

                p_sys = plt.bar(idx, sys_time, width=w_bar, label='Sys Time ' + accell)
                p_user = plt.bar(idx, user_time, width=w_bar, bottom=sys_time, label='User Time ' + accell)
                idx += w_bar
                p_real = plt.bar(idx, real_time, width=w_bar, label='Real Time ' + accell)
                idx += w_bar + 0.01

            # aqui fica o plot do gráfico
            ax.set_xlabel('GOP')
            ax.set_ylabel('Time (s)')
            ax.set_title('Times by GOP, qp {}, tile {}'.format(str(qp), tile))
            ax.set_xticks(idx2 + 2 * w_bar)
            ax.set_xticklabels(('32', '64', '96', '128'))
            ax.legend()

            plt.yticks(np.arange(0, 0.2, 0.020))
            plt.legend(bbox_to_anchor=(1.05, 1),
                       loc='upper left',
                       borderaxespad=0.)
            #plt.show()

            os.makedirs(destiny, exist_ok=True)
            name = destiny + '/clans_{}_{}_{}_gop{}'.format(size,
                                                            str(fps),
                                                            tile,
                                                            str(qp))
            fig.savefig(name)
            print('ok')


def graph3():
    import matplotlib.pyplot as plt
    time_data = _load_data('times.json')
    for qp in qps:

        for gop in gops:
            destiny = 'graph3_qp-gop-tile'
            plt.close()
            fig, ax = plt.subplots(figsize=(8, 5))
            w_bar = 0.2
            idx = np.array([1., 2., 3., 4., 5.])
            idx2 = np.array([1., 2., 3., 4., 5.])

            for accell in accells:
                real_time = []
                user_time = []
                sys_time = []

                for tile in tiles:
                    real_time += [time_data[tile][str(gop)][str(qp)][accell]['real_time']]
                    user_time += [time_data[tile][str(gop)][str(qp)][accell]['user_time']]
                    sys_time += [time_data[tile][str(gop)][str(qp)][accell]['sys_time']]

                plt.bar(idx, sys_time, width=w_bar, label='Sys Time ' + accell)
                plt.bar(idx, user_time, width=w_bar, bottom=sys_time, label='User Time ' + accell)
                idx += w_bar
                plt.bar(idx, real_time, width=w_bar, label='Real Time ' + accell)
                idx += w_bar + 0.01

            # aqui fica o plot do gráfico
            ax.set_xlabel('Tiles')
            ax.set_ylabel('Time (s)')
            ax.set_title('Times by tiles, QP {}, GOP {}'.format(str(qp), str(gop)))
            ax.set_xticks(idx2 + 2 * w_bar)
            ax.set_xticklabels(('1x1', '2x3', '4x6', '6x9', '8x12'))
            ax.legend()

            plt.yticks(np.arange(0, 0.2, 0.020))
            plt.legend(bbox_to_anchor=(1.05, 1),
                       loc='upper left',
                       borderaxespad=0.)
            #plt.show()

            os.makedirs(destiny, exist_ok=True)
            name = destiny + '/clans_{}_{}_{}_gop{}'.format(size,
                                                            str(fps),
                                                            str(gop),
                                                            str(qp))
            fig.savefig(name)
            print('ok')


def graph2():
    import matplotlib.pyplot as plt
    time_data = _load_data('times.json')

    for gop in gops:
        for tile in tiles:
            destiny = 'graph2_gop-tile-qp'
            plt.close()
            fig, ax = plt.subplots(figsize=(8, 5))
            w_bar = 0.2
            idx = np.array([1., 2., 3., 4., 5.])
            idx2 = np.array([1., 2., 3., 4., 5.])

            for accell in accells:
                real_time = []
                user_time = []
                sys_time = []

                for qp in qps:
                    real_time += [time_data[tile][str(gop)][str(qp)][accell]['real_time']]
                    user_time += [time_data[tile][str(gop)][str(qp)][accell]['user_time']]
                    sys_time += [time_data[tile][str(gop)][str(qp)][accell]['sys_time']]

                plt.bar(idx, sys_time, width=w_bar, label='Sys Time ' + accell)
                plt.bar(idx, user_time, width=w_bar, bottom=sys_time, label='User Time ' + accell)
                idx += w_bar
                plt.bar(idx, real_time, width=w_bar, label='Real Time ' + accell)
                idx += w_bar + 0.01

            # aqui fica o plot do gráfico
            ax.set_xlabel('QP')
            ax.set_ylabel('Time (s)')
            ax.set_title('Times by qp, gop {}, tile {}'.format(str(gop), tile))
            ax.set_xticks(idx2 + 2 * w_bar)
            ax.set_xticklabels(('20', '25', '30', '35', '40'))
            ax.legend()

            plt.yticks(np.arange(0, 0.2, 0.020))
            plt.legend(bbox_to_anchor=(1.05, 1),
                       loc='upper left',
                       borderaxespad=0.)
            #plt.show()

            os.makedirs(destiny, exist_ok=True)
            name = destiny + '/clans_{}_{}_{}_gop{}'.format(size,
                                                            str(fps),
                                                            tile,
                                                            str(gop))
            fig.savefig(name)
            print('ok')


def graph1():
    import matplotlib.pyplot as plt
    time_data = _load_data('times.json')

    for gop in gops:
        for qp in qps:
            destiny = 'graph1_gop-qp-tile'

            plt.close()
            fig, ax = plt.subplots(figsize=(8, 5))
            w_bar = 0.2
            idx = np.array([1., 2., 3., 4., 5.])
            idx2 = np.array([1., 2., 3., 4., 5.])

            for accell in accells:
                real_time = []
                user_time = []
                sys_time = []

                for tile in tiles:
                    real_time += [time_data[tile][str(gop)][str(qp)][accell]['real_time']]
                    user_time += [time_data[tile][str(gop)][str(qp)][accell]['user_time']]
                    sys_time += [time_data[tile][str(gop)][str(qp)][accell]['sys_time']]

                plt.bar(idx, sys_time, width=w_bar, label='Sys Time ' + accell)
                plt.bar(idx, user_time, width=w_bar, bottom=sys_time, label='User Time ' + accell)
                idx += w_bar
                plt.bar(idx, real_time, width=w_bar, label='Real Time ' + accell)
                idx += w_bar + 0.01

            # aqui fica o plot do gráfico
            ax.set_xlabel('Tiles')
            ax.set_ylabel('Time (s)')
            ax.set_title('Times by tiling, gop {}, qp {}'.format(str(gop), str(qp)))
            ax.set_xticks(idx2 + 2 * w_bar)
            ax.set_xticklabels(('1x1', '2x3', '4x6', '6x9', '8x12'))
            ax.legend()

            plt.yticks(np.arange(0, 0.2, 0.020))
            plt.legend(bbox_to_anchor=(1.05, 1),
                       loc='upper left',
                       borderaxespad=0.)
            plt.show()
            os.makedirs(destiny, exist_ok=True)
            name = destiny + '/clans_{}_{}_{}_gop{}'.format(size,
                                                            str(fps),
                                                            str(gop),
                                                            str(qp))
            fig.savefig(name)
            print('ok')


def graph6a():
    import matplotlib.pyplot as plt
    time_data = _load_data('times.json')

    for tile in tiles:
        for qp in qps:
            destiny = 'graph6a_tile-qp-gop'
            plt.close()
            fig, ax = plt.subplots(figsize=(8, 5))
            w_bar = 0.2
            idx = np.array([1., 2., 3., 4.])
            idx2 = np.array([1., 2., 3., 4.])

            for accell in accells:
                user_time = []

                for gop in gops:
                    user_time += [time_data[tile][str(gop)][str(qp)][accell]['user_time']]

                plt.bar(idx, user_time, width=w_bar, label='User Time ' + accell)
                idx += w_bar

            # aqui fica o plot do gráfico
            ax.set_xlabel('GOP')
            ax.set_ylabel('Time (s)')
            ax.set_title('Times by GOP, tile {}, qp {}'.format(tile, str(qp)))
            ax.set_xticks(idx2 + 2 * w_bar)
            ax.set_xticklabels(('32', '64', '96', '128'))
            ax.legend()

            plt.yticks(np.arange(0, 0.040, 0.004))
            plt.legend(bbox_to_anchor=(1.05, 1),
                       loc='upper left',
                       borderaxespad=0.)
            #plt.show()

            os.makedirs(destiny, exist_ok=True)
            name = destiny + '/clans_{}_{}_{}_qp{}'.format(size,
                                                           str(fps),
                                                           tile,
                                                           str(qp))
            fig.savefig(name)
            print('ok')


def graph5a():
    import matplotlib.pyplot as plt
    time_data = _load_data('times.json')

    for tile in tiles:
        for gop in gops:
            destiny = 'graph5a_tile-gop-qp'
            plt.close()
            fig, ax = plt.subplots(figsize=(8, 5))
            w_bar = 0.2
            idx = np.array([1., 2., 3., 4., 5.])
            idx2 = np.array([1., 2., 3., 4., 5.])

            for accell in accells:
                user_time = []

                for qp in qps:
                    user_time += [time_data[tile][str(gop)][str(qp)][accell]['user_time']]

                plt.bar(idx, user_time, width=w_bar, label='User Time ' + accell)
                idx += w_bar

            # aqui fica o plot do gráfico
            ax.set_xlabel('QP')
            ax.set_ylabel('Time (s)')
            ax.set_title('Times by QP, tile {}, gop {}'.format(tile, str(gop)))
            ax.set_xticks(idx2 + 2 * w_bar)
            ax.set_xticklabels(('20', '25', '30', '35', '40'))
            ax.legend()

            plt.yticks(np.arange(0, 0.040, 0.004))
            plt.legend(bbox_to_anchor=(1.05, 1),
                       loc='upper left',
                       borderaxespad=0.)
            #plt.show()

            os.makedirs(destiny, exist_ok=True)
            name = destiny + '/clans_{}_{}_{}_gop{}'.format(size,
                                                            str(fps),
                                                            tile,
                                                            str(gop))
            fig.savefig(name)
            print('ok')


def graph4a():
    import matplotlib.pyplot as plt
    time_data = _load_data('times.json')

    for qp in qps:
        for tile in tiles:
            destiny = 'graph4a_qp-tile-gop'
            plt.close()
            fig, ax = plt.subplots(figsize=(8, 5))
            w_bar = 0.2
            idx = np.array([1., 2., 3., 4.])
            idx2 = np.array([1., 2., 3., 4.])

            for accell in accells:
                user_time = []

                for gop in gops:
                    user_time += [time_data[tile][str(gop)][str(qp)][accell]['user_time']]

                p_user = plt.bar(idx, user_time, width=w_bar, label='User Time ' + accell)
                idx += w_bar

            # aqui fica o plot do gráfico
            ax.set_xlabel('GOP')
            ax.set_ylabel('Time (s)')
            ax.set_title('Times by GOP, qp {}, tile {}'.format(str(qp), tile))
            ax.set_xticks(idx2 + 2 * w_bar)
            ax.set_xticklabels(('32', '64', '96', '128'))
            ax.legend()
            plt.yticks(np.arange(0, 0.040, 0.004))

            plt.legend(bbox_to_anchor=(1.05, 1),
                       loc='upper left',
                       borderaxespad=0.)
            #plt.show()

            os.makedirs(destiny, exist_ok=True)
            name = destiny + '/clans_{}_{}_{}_gop{}'.format(size,
                                                            str(fps),
                                                            tile,
                                                            str(qp))
            fig.savefig(name)
            print('ok')


def graph3a():
    import matplotlib.pyplot as plt
    time_data = _load_data('times.json')
    for qp in qps:

        for gop in gops:
            destiny = 'graph3a_qp-gop-tile'
            plt.close()
            fig, ax = plt.subplots(figsize=(8, 5))
            w_bar = 0.2
            idx = np.array([1., 2., 3., 4., 5.])
            idx2 = np.array([1., 2., 3., 4., 5.])

            for accell in accells:
                user_time = []

                for tile in tiles:
                    user_time += [time_data[tile][str(gop)][str(qp)][accell]['user_time']]

                plt.bar(idx, user_time, width=w_bar, label='User Time ' + accell)
                idx += w_bar

            # aqui fica o plot do gráfico
            ax.set_xlabel('Tiles')
            ax.set_ylabel('Time (s)')
            ax.set_title('Times by tiles, QP {}, GOP {}'.format(str(qp), str(gop)))
            ax.set_xticks(idx2 + 2 * w_bar)
            ax.set_xticklabels(('1x1', '2x3', '4x6', '6x9', '8x12'))
            ax.legend()
            plt.yticks(np.arange(0, 0.040, 0.004))

            plt.legend(bbox_to_anchor=(1.05, 1),
                       loc='upper left',
                       borderaxespad=0.)
            #plt.show()

            os.makedirs(destiny, exist_ok=True)
            name = destiny + '/clans_{}_{}_{}_gop{}'.format(size,
                                                            str(fps),
                                                            str(gop),
                                                            str(qp))
            fig.savefig(name)
            print('ok')


def graph2a():
    import matplotlib.pyplot as plt
    time_data = _load_data('times.json')

    for gop in gops:
        for tile in tiles:
            destiny = 'graph2a_gop-tile-qp'
            plt.close()
            fig, ax = plt.subplots(figsize=(8, 5))
            w_bar = 0.2
            idx = np.array([1., 2., 3., 4., 5.])
            idx2 = np.array([1., 2., 3., 4., 5.])

            for accell in accells:
                user_time = []

                for qp in qps:
                    user_time += [time_data[tile][str(gop)][str(qp)][accell]['user_time']]

                plt.bar(idx, user_time, width=w_bar, label='User Time ' + accell)
                idx += w_bar

            # aqui fica o plot do gráfico
            ax.set_xlabel('QP')
            ax.set_ylabel('Time (s)')
            ax.set_title('Times by qp, gop {}, tile {}'.format(str(gop), tile))
            ax.set_xticks(idx2 + 2 * w_bar)
            ax.set_xticklabels(('20', '25', '30', '35', '40'))
            ax.legend()

            plt.yticks(np.arange(0, 0.040, 0.004))
            plt.legend(bbox_to_anchor=(1.05, 1),
                       loc='upper left',
                       borderaxespad=0.)
            #plt.show()

            os.makedirs(destiny, exist_ok=True)
            name = destiny + '/clans_{}_{}_{}_gop{}'.format(size,
                                                            str(fps),
                                                            tile,
                                                            str(gop))
            fig.savefig(name)
            print('ok')


def graph1a():
    import matplotlib.pyplot as plt
    time_data = _load_data('times.json')

    for gop in gops:
        for qp in qps:
            destiny = 'graph1a_gop-qp-tile'

            plt.close()
            fig, ax = plt.subplots(figsize=(8, 5))
            w_bar = 0.2
            idx = np.array([1., 2., 3., 4., 5.])
            idx2 = np.array([1., 2., 3., 4., 5.])

            for accell in accells:
                user_time = []

                for tile in tiles:
                    user_time += [time_data[tile][str(gop)][str(qp)][accell]['user_time']]

                plt.bar(idx, user_time, width=w_bar, label='User Time ' + accell)
                idx += w_bar

            # aqui fica o plot do gráfico
            ax.set_xlabel('Tiles')
            ax.set_ylabel('Time (s)')
            ax.set_title('Times by tiling, gop {}, qp {}'.format(str(gop), str(qp)))
            ax.set_xticks(idx2 + 2 * w_bar)
            ax.set_xticklabels(('1x1', '2x3', '4x6', '6x9', '8x12'))
            ax.legend()

            plt.yticks(np.arange(0, 0.040, 0.004))
            plt.legend(bbox_to_anchor=(1.05, 1),
                       loc='upper left',
                       borderaxespad=0.)
            #plt.show()
            os.makedirs(destiny, exist_ok=True)
            name = destiny + '/clans_{}_{}_{}_gop{}'.format(size,
                                                            str(fps),
                                                            str(gop),
                                                            str(qp))
            fig.savefig(name)
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
