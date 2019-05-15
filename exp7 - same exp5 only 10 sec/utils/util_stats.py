import json
import os
import platform
import subprocess
import time


def check_system():
    if platform.system() == 'Windows':
        sl = '\\'
        ffmpeg = 'ffmpeg.exe'
        mp4box = 'C:\\"Program Files"\\GPAC\\MP4Box.exe'
        mp4client = 'C:\\"Program Files"\\GPAC\\MP4Client.exe'
        kvazaar = 'bin\\kvazaar.exe'
        siti = 'bin\\SITI.exe'
        cp = 'copy /y'
    else:
        sl = '/'
        ffmpeg = 'ffmpeg'
        mp4box = 'MP4Box'
        kvazaar = 'kvazaar'
        siti = 'bin/siti'
        cp = 'cp'
        mp4client = 'MP4Client'

    programs = dict(sl=sl,
                    ffmpeg=ffmpeg,
                    mp4box=mp4box,
                    kvazaar=kvazaar,
                    siti=siti,
                    cp=cp,
                    mp4client=mp4client)

    return programs


def run(command, hevc_video, ext, overwrite=False, log_mode='w'):
    if os.path.isfile(f'{hevc_video}.{ext}') and not overwrite:
        print(f'arquivo {hevc_video}.{ext} existe. Pulando.')
    else:
        attempts = 0
        while attempts >= 0:
            if attempts > 0:
                print('Tentando novamente.')
            try:
                with open(hevc_video + '.log', log_mode, encoding='utf-8') as f:
                    print(command)
                    subprocess.run(command, shell=True, stdout=f, stderr=subprocess.STDOUT)
                break
            except FileNotFoundError:
                print(f'Tentativa {attempts + 1}. Erro ao abrir o arquivo {hevc_video + ".log"}')
                attempts += 1
                time.sleep(5)


def list_videos(list_name):
    videos = {}

    try:
        f = open(list_name, 'r')
        videos = json.load(f)

    except IOError:
        exit(f'Arquivo {list_name} não encontrado')

    return videos


def encode(name, scale, gop, fps, tile, yuv_video_name, quality, factor):
    kvazaar = check_system()['kvazaar']
    sl = check_system()['sl']

    params_common = ''
    hevc_video = ''
    hevc_folder = ''
    if factor in 'qp':
        basename = f'{name}_{scale}_{fps}_{tile}_qp{quality}'
        hevc_folder = f'hevc{sl}{basename}'
        hevc_video = f'{hevc_folder}{sl}{basename}'
        params_common = (f'--input {yuv_video_name}.yuv '
                         f'--input-res {scale} '
                         f'--input-fps {fps} '
                         f'-p {gop} '
                         '--no-tmvp '
                         '--no-open-gop '
                         f'--qp {quality}')
    elif factor in 'rate':
        basename = f'{name}_{scale}_{fps}_{tile}_rate{quality}'
        hevc_folder = f'hevc{sl}{basename}'
        hevc_video = f'{hevc_folder}{sl}{basename}'
        params_common = (f'--input {yuv_video_name}.yuv '
                         f'--input-res {scale} '
                         f'--input-fps {fps} '
                         f'-p {gop} '
                         '--no-tmvp '
                         '--no-open-gop '
                         f'--bitrate {quality}')
    else:
        exit('Fator de qualidade só pode ser "qp" ou "rate"')

    os.makedirs(f'{hevc_folder}', exist_ok=True)

    if tile is not '1x1':
        tile_params = f' --tiles {tile} --slices tiles --mv-constraint frametilemargin'
        params_common += tile_params

    command = f'{kvazaar} {params_common} --output {hevc_video}.hevc'
    run(command, hevc_video, 'hevc')
    return hevc_video


def encapsule(name, scale, fps, tile, hevc_video, quality, factor):
    mp4box = check_system()['mp4box']
    sl = check_system()['sl']

    basename = ''
    if factor in 'qp':
        basename = f'{name}_{scale}_{fps}_{tile}_qp{quality}'
    elif factor in 'rate':
        basename = f'{name}_{scale}_{fps}_{tile}_rate{quality}'
    else:
        exit('Fator de qualidade só pode ser "qp" ou "rate"')

    mp4_folder = f'mp4{sl}{basename}'
    os.makedirs(f'{mp4_folder}', exist_ok=True)
    mp4_video = f'{mp4_folder}{sl}{basename}'

    command = f'{mp4box} -add {hevc_video}.hevc:split_tiles -new {mp4_video}.mp4'
    run(command, mp4_video, 'mp4')
    return mp4_video


def extract_segment(name, scale, fps, tile, mp4_video, quality, factor):
    mp4box = check_system()['mp4box']
    sl = check_system()['sl']
    m, n = list(map(int, tile.split('x')))

    basename = ''
    if factor in 'qp':
        basename = f'{name}_{scale}_{fps}_{tile}_qp{quality}'
    elif factor in 'rate':
        basename = f'{name}_{scale}_{fps}_{tile}_rate{quality}'
    else:
        exit('Fator de qualidade só pode ser "qp" ou "rate"')

    mp4_folder = f'mp4{sl}{basename}'
    segments_folder = f'dash{sl}{basename}'
    os.makedirs(f'{mp4_folder}', exist_ok=True)
    os.makedirs(f'{segments_folder}', exist_ok=True)

    for tile_count in range(1, m * n + 1):
        mp4_video_tile = f'{mp4_folder}{sl}{basename}_tile{tile_count}'

        # Extract desired track
        command = f'{mp4box} -raw {tile_count + 1} {mp4_video}.mp4 -out {mp4_video_tile}.hevc'
        run(command, mp4_video_tile, 'hevc')

        # Add resulting track in new mp4
        command = f'{mp4box} -add {mp4_video_tile}.hevc -new {mp4_video_tile}.mp4'
        run(command, mp4_video_tile, 'mp4', log_mode='a')

        # Segment tiles in chunks
        command = f'{mp4box} -split 1 {mp4_video_tile}.mp4 -out {segments_folder}{sl}'
        run(command, f'{segments_folder}{sl}{basename}_tile{tile_count}', 'log')


def decode(name, scale, fps, tile, duration, quality, factor):
    sl = check_system()['sl']
    mp4client = check_system()['mp4client']
    # m, n = list(map(int, tile.split('x')))

    basename = ''
    if factor in 'qp':
        basename = f'{name}_{scale}_{fps}_{tile}_qp{quality}'
    elif factor in 'rate':
        basename = f'{name}_{scale}_{fps}_{tile}_rate{quality}'
    else:
        exit('Fator de qualidade só pode ser "qp" ou "rate"')
    hevc_folder = f'hevc{sl}{name}_{scale}_{fps}_{tile}'
    dectime_folder = f'dectime'
    os.makedirs(f'{dectime_folder}', exist_ok=True)

    video_path = f'{hevc_folder}{sl}{basename}'
    log_path = f'{dectime_folder}{sl}{basename}'

    command = f'taskset -c 0 {mp4client} -bench {video_path}.mp4'
    _run_bench(command, log_path, 'log')

    # for t in range(1, m * n + 1):
    #     for chunk in range(1, duration + 1):
            # video_path = f'{hevc_folder}{sl}{basename}_tile{t}_{chunk:03}'
            # log_path = f'{dectime_folder}{sl}{basename}_tile{t}_{chunk:03}'

            # command = f'taskset -c 0 {mp4client} -bench {video_path}.mp4'
            # _run_bench(command, log_path, 'log')


def _run_bench(command, log_path, ext, overwrite=True, log_mode='a'):
    if os.path.isfile(f'{log_path}.{ext}') and not overwrite:
        print(f'arquivo {log_path}.{ext} existe. Pulando.')
    else:
        attempts = 1
        while True:
            try:
                f = open('temp.tmp', 'w', encoding='utf-8')
                break
            except FileNotFoundError:
                print(f'Tentativa {attempts}. Erro ao abrir o arquivo {"temp.tmp" + ".log"}')
                attempts += 1
                time.sleep(5)
                print('Tentando novamente.')

        attempts = 1
        while True:
            print(command)
            p = subprocess.run(command, shell=True, stdout=f, stderr=subprocess.STDOUT)
            f.close()
            return_code = p.returncode
            print(f'returncode = {return_code}')

            if return_code != 0:
                print(f'Tentativa {attempts}. Erro. Exitcode == {p.returncode}. Tentando novamente.')
                attempts += 1
                continue
            else:
                attempts = 1
                while True:
                    try:
                        f1 = open('temp.tmp', 'r', encoding='utf-8')
                        f2 = open(f'{log_path}.log', log_mode, encoding='utf-8')
                        break
                    except FileNotFoundError:
                        print(f'Tentativa {attempts}. Erro ao abrir o arquivo temp.tmp ou {log_path}.log')
                        attempts += 1
                        time.sleep(5)
                        print('Tentando novamente.')

                f2.write(f1.read())
                f1.close()
                f2.close()
                break
