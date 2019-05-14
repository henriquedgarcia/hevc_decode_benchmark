import json
import os
import platform
import queue
import subprocess


def check_system():
    if platform.system() == 'Windows':
        sl = '\\'
        ffmpeg = 'ffmpeg.exe'
        mp4box = '"C:\\Program Files\\GPAC\\MP4Box.exe"'
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

    programs = dict(sl=sl,
                    ffmpeg=ffmpeg,
                    mp4box=mp4box,
                    kvazaar=kvazaar,
                    siti=siti,
                    cp=cp)

    return programs


def worker_encode(queue_command):
    """
    Um processo separado que executa os comandos da fila compartilhada
    :type queue_command: multiprocessing.queues.Queue
    :param queue_command: Uma lista de commandos
    :return: None
    """
    while not queue_command.empty():
        try:
            command_context = queue_command.get(timeout=1)
        except queue.Empty:
            break

        command = command_context['command']
        filepath = command_context['filepath']
        filepath = filepath.split('.')[0]
        print(f'Processando {filepath}.')

        folder_out = command_context['folder_out']
        os.makedirs(folder_out, exist_ok=True)

        with open(filepath + '.log', 'w', encoding='utf-8') as f:
            subprocess.run(command, stdout=f, stderr=subprocess.STDOUT)


def prepare_command(name, tile, rate, qp, video_params, programs, tile_count):
    scale = video_params['scale']
    fps = video_params['fps']
    gop = video_params['gop']

    sl = programs['sl']
    kvazaar = programs['kvazaar']

    # Prepare path
    name_base = f'{name}_{scale}_{fps}'
    folder_name = f'{name_base}_{tile}'

    folder_in = f'yuv{sl}{folder_name}'
    name_in = f'{folder_name}_tile{tile_count}'
    filepath_in = f'{folder_in}{sl}{name_in}.yuv'

    folder_out = f'hevc{sl}{folder_name}'
    name_out_rate = f'{folder_name}_rate{rate}_tile{tile_count}'
    name_out_qp = f'{folder_name}_qp{qp}_tile{tile_count}'
    filepath_out_rate = f'{folder_out}{sl}{name_out_rate}.hevc'
    filepath_out_qp = f'{folder_out}{sl}{name_out_qp}.hevc'

    # Encode params
    params_common = (f'--input-res {scale} '
                     f'--input-fps {fps} '
                     f'--input {filepath_in} '
                     f'-p {gop} '
                     '--no-tmvp '
                     '--no-open-gop')
    params_out_rate = f'{params_common} --bitrate {rate} --output {filepath_out_rate}'
    params_out_qp = f'{params_common} --qp {qp} --output {filepath_out_qp}'
    params_tile = (f"--tiles {tile} "
                   "--slices tiles "
                   "--mv-constraint frametilemargin")

    if tile not in "1x1":
        params_out_rate = f'{params_tile} {params_out_rate}'
        params_out_qp = f'{params_tile} {params_out_qp}'

    command_rate = f'{kvazaar} {params_out_rate}'
    command_qp = f'{kvazaar} {params_out_qp}'

    over_rate = dict(command=command_rate,
                     filepath=filepath_out_rate,
                     folder_out=folder_out)
    over_qp = dict(command=command_qp,
                   filepath=filepath_out_qp,
                   folder_out=folder_out)

    return over_rate, over_qp


def list_videos(list_name):
    videos = {}

    try:
        f = open(list_name, 'r')
        videos = json.load(f)

    except IOError:
        exit(f'Arquivo {list_name} não encontrado')

    return videos
