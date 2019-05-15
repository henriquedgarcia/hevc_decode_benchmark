import json
import os
import platform
import subprocess
import time

from utils.video_param import VideoParams


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


def list_videos(list_name):
    videos = {}

    try:
        f = open(list_name, 'r')
        videos = json.load(f)

    except IOError:
        exit(f'Arquivo {list_name} não encontrado')

    return videos


def run(command, hevc_video, ext, overwrite=False, log_mode='w'):
    if os.path.isfile(f'{hevc_video}.{ext}') and not overwrite:
        print(f'arquivo {hevc_video}.{ext} existe. Pulando.')

    else:
        attempts = 0
        while True:
            if attempts > 0:
                print('Tentando novamente.')
            elif attempts > 4:
                exit('[_run] Tentativas == 5. Alguma coisa está impedindo a criação log?')

            try:
                if log_mode is None:
                    subprocess.run(command, shell=True, stderr=subprocess.STDOUT)
                else:
                    with open(hevc_video + '.log', log_mode, encoding='utf-8') as f:
                        print(command)
                        subprocess.run(command, shell=True, stdout=f, stderr=subprocess.STDOUT)
                break
            except FileNotFoundError:
                print(f'Tentativa {attempts + 1}. Erro ao abrir o arquivo {hevc_video + ".log"}')
                attempts += 1
                time.sleep(5)


def encode(video: VideoParams, factor):
    """
    Codifica o vídeo usando o codificador especificado em encoder
    :type video: VideoParams
    :param video:
    :param factor:
    :return:
    """
    program = check_system()[video.encoder]

    if video.encoder in 'kvazaar':
        params_common = (f'--input {video.yuv_video} '
                         f'-n {int(video.duration * video.fps)} '
                         f'--input-res {video.scale} '
                         f'--input-fps {video.fps} '
                         f'-p {video.gop} '
                         '--no-tmvp '
                         '--no-open-gop ')

        if factor in 'qp':
            params_common += f'--qp {video.qp}'
        elif factor in 'rate':
            params_common += f'--bitrate {video.rate}'
        else:
            exit('Fator de qualidade só pode ser "qp" ou "rate"')

        if video.tile_format not in '1x1':
            tile_params = f' --tiles {video.tile_format} --slices tiles --mv-constraint frametilemargin'
            params_common += tile_params

        command = f'{program} {params_common} --output {video.hevc_video[factor]}.hevc'
        run(command, video.hevc_video[factor], 'hevc')

    elif video.encoder in 'ffmpeg':
        global_params = '-hide_banner -n'
        params_common = (f'-s {video.scale} '
                         f'-framerate {video.fps} '
                         f'-i {video.yuv_video} '
                         f'-t {video.duration} '
                         f'-codec libx265 '
                         f'-x265-params '
                         f'"keyint={video.gop}:'
                         f'min-keyint={video.gop}:'
                         f'open-gop=0:'
                         f'info=0:'
                         f'temporal-layers=0:'
                         f'temporal-mvp=0:')

        mp4_video = video.mp4_video[factor]
        video.mp4_video[factor] = {}

        tile_count = 0
        for x in range(0, video.width, video.tile_w):
            for y in range(0, video.height, video.tile_h):
                tile_count += 1
                video.mp4_video[factor][tile_count] = f'{mp4_video}_tile{tile_count}'

                filter_params = f'-vf "crop=w={video.tile_w}:h={video.tile_h}:x={x}:y={y}"'

                if factor in 'qp':
                    params_common += f'qp={video.qp}"'
                elif factor in 'rate':
                    params_common += f'bitrate={video.rate}"'
                else:
                    exit('Fator de qualidade só pode ser "qp" ou "rate"')

                command = (f'{program} {global_params} {params_common} {filter_params} '
                           f'{video.mp4_video[factor][tile_count]}.mp4')

                run(command, f'{video.mp4_video[factor][tile_count]}', 'mp4')

    else:
        exit('[encode] Encoder só pode ser "ffmpeg" ou "kvazaar"')


def encapsule(video, factor):
    """
    Codifica o vídeo usando o codificador especificado em encoder
    :type video: VideoParams
    :param video:
    :param factor:
    :return:
    """

    if video.encoder in 'ffmpeg':
        pass
    elif video.encoder in 'kvazaar':
        mp4box = check_system()['mp4box']

        command = f'{mp4box} -add {video.hevc_video[factor]}.hevc:split_tiles -new {video.mp4_video[factor]}.mp4'
        run(command, video.mp4_video[factor], 'mp4')
    else:
        exit('[encapsule] Opção de encoder inválida.')


def extract_tile(video, factor):
    """
    Codifica o vídeo usando o codificador especificado em encoder
    :type video: VideoParams
    :param video:
    :param factor:
    :return:
    """

    if video.encoder in 'ffmpeg':
        pass
    elif video.encoder in 'kvazaar':
        mp4box = check_system()['mp4box']

        for tile_count in range(1, video.number_tiles + 1):
            hevc_tiled_video = f'{video.hevc_video[factor]}_tile{tile_count}.hevc'
            mp4_tiled_video = f'{video.mp4_video[factor]}_tile{tile_count}.mp4'

            # Extract desired track
            track = tile_count + 1
            if video.tile_format in '1x1':
                track = 1

            command = f'{mp4box} -raw {track} {video.mp4_video[factor]}.mp4 -out {hevc_tiled_video}.hevc'
            run(command, hevc_tiled_video, 'hevc')

            # Add resulting track in new mp4
            command = f'{mp4box} -add {hevc_tiled_video}.hevc -new {mp4_tiled_video}.mp4'
            run(command, mp4_tiled_video, 'mp4')


def make_segments(video, factor):
    """
    Codifica o vídeo usando o codificador especificado em encoder
    :type video: VideoParams
    :param video:
    :param factor:
    :return:
    """
    mp4box = check_system()['mp4box']

    mp4_tiled_video = ''
    segment_log = ''

    for tile_count in range(1, video.number_tiles + 1):
        if video.encoder in 'ffmpeg':
            mp4_tiled_video = f'{video.mp4_video[factor][tile_count]}'
            segment_log = f'{video.segment_folder[factor]}{video.sl}{video.basename[factor]}'

        elif video.encoder in 'kvazaar':
            mp4_tiled_video = f'{video.mp4_video[factor]}_tile{tile_count}.mp4'
            segment_log = f'{video.segment_folder[factor]}{video.sl}{video.basename[factor]}_tile{tile_count}'

        # Segment tiles in chunks
        command = f'{mp4box} -split 1 {mp4_tiled_video}.mp4 -out {video.segment_folder[factor]}{video.sl}'
        run(command, segment_log, 'log')


def decode(video, decoder, factor, multithread=True):
    """
    :type video: VideoParams
    :param video:
    :param decoder:
    :param factor:
    :param multithread:
    :return:
    """

    program = check_system()[decoder]  # pode ser mp4client ou ffmpeg
    command = ''
    for tile in range(1, video.number_tiles):
        for chunk in range(1, video.duration + 1):
            video_path = f'{video.segment_folder[factor]}{video.sl}{video.basename[factor]}_tile{tile}_{chunk:03}'
            dectime_log = f'{video.dectime_folder[factor]}{video.sl}{video.basename[factor]}_tile{tile}_{chunk:03}'
            if program in 'ffmpeg':
                if multithread:
                    command = (f'powershell -command "& {{'
                               f'Measure-Command -expression {{'
                               f'{program} -benchmark -threads 0 -codec hevc -i {video_path} -f null -}}'
                               f'"')
                else:
                    command = (f'powershell -command "& {{'
                               f'Measure-Command -expression {{'
                               f'{program} -benchmark -threads 1 -codec hevc -i {video_path} -f null -}}'
                               f'"')

            elif program in 'mp4client':
                command = f'{program} -bench {video_path}'

                if multithread:
                    command = f'start /b /wait {command}'
                else:
                    command = f'start /b /wait /affinity 0x800 {command}'

            else:
                exit('Decoders disponíveis são mp4client e ffmpeg.')

            _run_bench(command, dectime_log, 'log')


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
            print(f'Returncode = {return_code}')

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
