#!/bin/python3
# import time.wait
import numpy as np

size = '3840x2160'
fps = 32

average = {}
averages = {}
for gop in [32, 64, 96, 128]:
    for qp in [20, 25, 30, 35, 40]:
        for tile in ['1x1', '2x3', '4x6', '6x9', '8x12']:
            for accell in ['nohwaccel', 'cuvid']:
                name = 'clans_{}_{}_{}_gop{}_qp{}'.format(size, str(fps), tile, str(gop), str(qp))
                name = 'dectime/' + name + '_dectime_' + accell + '.txt'
               
                with open(name, 'rt') as f:

                    real_time = []
                    user_time = []
                    sys_time = []

                    for line in f:
                        # print('Conteúdo = ' + str(line), end='')
                        if line in '\n':
                            continue

                        elif 'real' in line:
                            real_time.append(float(line[:-2].split('m')[1]))

                        elif 'user'  in line:
                            user_time.append(float(line[:-2].split('m')[1]))

                        elif 'sys' in line:
                            sys_time.append(float(line[:-2].split('m')[1]))

                average[name] = {}
                average[name]['real_time'] = np.average(real_time)
                average[name]['user_time'] = np.average(user_time)
                average[name]['sys_time'] = np.average(sys_time)

                print('{} \nrt = {}\tut = {}\tst = {}'.format(name, average[name]['real_time'], average[name]['real_time'], average[name]['sys_time']))
