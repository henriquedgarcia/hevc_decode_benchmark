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


def run(command, hevc_video, ext, overwrite=False, mode='w'):
    if os.path.isfile(f'{hevc_video}.{ext}') and not overwrite:
        print(f'arquivo {hevc_video}.{ext} existe. Pulando.')
    else:
        attempts = 0
        while attempts >= 0:
            if attempts > 0:
                print('Tentando novamente.')
            try:
                with open(hevc_video + '.log', mode, encoding='utf-8') as f:
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
