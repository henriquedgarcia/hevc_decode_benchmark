import json
import os
import platform
import subprocess
import time


class Atribs:
    # Special params
    _tile_format = ''
    _scale = ''
    _rate = 0
    _qp = 0

    # commons params
    fps = 0
    gop = 0
    duration = 0
    width = 0
    height = 0
    tile_w = 0
    tile_h = 0
    number_tiles = 0

    # file properties
    project = ''
    name = ''
    _basic = ''

    basename = {}

    yuv = ''
    hevc = ''
    mp4 = ''
    segment = ''
    dectime = ''

    yuv_video = ''
    hevc_video = {}
    mp4_video = {}

    yuv_folder = ''
    _hevc_folder = ''
    _mp4_folder = ''
    segment_folder = {}
    dectime_folder = {}

    # Other
    encoder = ''
    _decoder = ''
    sl = ''

    @property
    def scale(self):
        return self._scale

    @scale.setter
    def scale(self, value):
        self._scale = value
        self.width, self.height = list(map(int, value.split('x')))

    @property
    def tile_format(self):
        return self._tile_format

    @tile_format.setter
    def tile_format(self, value):
        if self.name == '':
            exit('[VideoParam] É preciso definir o nome antes.')

        self._tile_format = value
        m, n = list(map(int, value.split('x')))
        self.tile_w = int(self.width / m)
        self.tile_h = int(self.height / n)
        self.number_tiles = m * n

        self._basic = f'{self.name}_{self.scale}_{self.fps}_{self._tile_format}'

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, value):
        if self._tile_format == '':
            exit('É preciso definir o formato dos tiles antes. == ')

        self._rate = value
        self.basename["rate"] = f'{self._basic}_rate{value}'
        self.hevc_video["rate"] = f'{self.hevc_folder}{self.sl}{self.basename["rate"]}'
        self.mp4_video["rate"] = f'{self.mp4_folder}{self.sl}{self.basename["rate"]}'
        self.dectime_folder["rate"] = f'{self.dectime}{self.sl}{self.basename["rate"]}'
        self.segment_folder["rate"] = f'{self.segment}{self.sl}{self.basename["rate"]}'
        os.makedirs(f'{self.segment_folder["rate"]}', exist_ok=True)

    @property
    def qp(self):
        return self._qp

    @qp.setter
    def qp(self, value):
        if self._tile_format == '':
            exit('É preciso definir o formato dos tiles antes.')

        self._qp = value
        self.basename["qp"] = f'{self._basic}_qp{value}'
        self.hevc_video["qp"] = f'{self.hevc_folder}{self.sl}{self.basename["qp"]}'
        self.mp4_video["qp"] = f'{self.mp4_folder}{self.sl}{self.basename["qp"]}'
        self.dectime_folder["qp"] = f'{self.dectime}{self.sl}{self.basename["qp"]}'
        self.segment_folder["qp"] = f'{self.segment}{self.sl}{self.basename["qp"]}'
        os.makedirs(f'{self.segment_folder["qp"]}', exist_ok=True)

    @property
    def decoder(self) -> str:
        return self._decoder

    @property
    def hevc_folder(self):
        self._hevc_folder = f'{self.hevc}{self.sl}{self._basic}'
        os.makedirs(f'{self._hevc_folder}', exist_ok=True)
        return self._hevc_folder

    @property
    def mp4_folder(self):
        self._mp4_folder = f'{self.mp4}{self.sl}{self._basic}'
        os.makedirs(f'{self._mp4_folder}', exist_ok=True)
        return self._mp4_folder

    @decoder.setter
    def decoder(self, value: str):
        if self._qp == 0 and self._rate == 0:
            exit('É preciso definir o QP ou a taxa antes.')

        self._decoder = value

        if self._qp != 0:
            os.makedirs(f'{self.dectime_folder["qp"]}', exist_ok=True)
        elif self._rate != 0:
            os.makedirs(f'{self.dectime_folder["rate"]}', exist_ok=True)
        else:
            exit('É preciso definir o quantização ou taxa antes.')


class Actions(Atribs):
    @staticmethod
    def _run(command, hevc_video, ext, overwrite=False, log_mode='w'):
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
                    with open(hevc_video + '.log', log_mode, encoding='utf-8') as f:
                        print(command)
                        subprocess.run(command, shell=True, stdout=f, stderr=subprocess.STDOUT)
                    break
                except FileNotFoundError:
                    print(f'Tentativa {attempts + 1}. Erro ao abrir o arquivo {hevc_video + ".log"}')
                    attempts += 1
                    time.sleep(5)

    @staticmethod
    def _check_system(program):
        if platform.system() == 'Windows':
            sl = '\\'
            ffmpeg = 'C:\\ffmpeg\\bin\\ffmpeg.exe'
            kvazaar = 'bin\\kvazaar.exe'
            mp4box = 'C:\\"Program Files"\\GPAC\\MP4Box.exe'
            mp4client = 'C:\\"Program Files"\\GPAC\\MP4Client.exe'
        else:
            sl = '/'
            ffmpeg = 'ffmpeg'
            kvazaar = 'kvazaar'
            mp4box = 'MP4Box'
            mp4client = 'MP4Client'

        programs = dict(slash=sl,
                        ffmpeg=ffmpeg,
                        mp4box=mp4box,
                        kvazaar=kvazaar,
                        mp4client=mp4client)

        return programs[program]

    @staticmethod
    def load_json(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
                return json_data

        except IOError:
            exit(f'Arquivo {filename} não encontrado')

    def encode(self, factor: str):
        """
        Codifica o vídeo usando o codificador especificado em encoder
        :param factor:
        :return:
        """

        if self.encoder in 'kvazaar':
            self._encode_kvazaar(factor=factor)

        elif self.encoder in 'ffmpeg':
            self._encode_ffmpeg(factor=factor)

        else:
            print('[encode] Encoder só pode ser "ffmpeg" ou "kvazaar"')

    def _encode_ffmpeg(self, factor):
        program = self._check_system(self.encoder)
        global_params = '-hide_banner -y'
        param_in = (f'-s {self.scale} '
                    f'-framerate {self.fps} '
                    f'-i {self.yuv_video}')
        param_out = (f'-codec libx265 '
                     f'-t {self.duration} '
                     f'-x265-params '
                     f'"keyint={self.gop}'
                     f':min-keyint={self.gop}'
                     f':open-gop=0'
                     f':info=0'
                     f':temporal-layers=0'
                     f':temporal-mvp=0'
                     f':log-level=3')

        if factor in 'qp':
            param_out += (f':qp={self.qp}'
                          f':qpmin={self.qp}'
                          f':qpmax={self.qp}"')
        elif factor in 'rate':
            rate = int(self.rate / self.number_tiles)
            param_out = f'-b:v {rate} {param_out}'
        else:
            exit('Fator de qualidade só pode ser "qp" ou "rate"')

        tile_count = 0
        for x in range(0, self.width, self.tile_w):
            for y in range(0, self.height, self.tile_h):
                tile_count += 1
                mp4_video = f'{self.mp4_video[factor]}_tile{tile_count}'

                filter_params = f'-vf "crop=w={self.tile_w}:h={self.tile_h}:x={x}:y={y}"'

                if factor in 'rate':
                    # 1-pass
                    command = (f'{program} {global_params} {param_in} {param_out}:pass=1" {filter_params} -f mp4 '
                               f'nul')
                    self._run(command, f'{mp4_video}', 'mp4')

                    # 2-pass
                    command = (f'{program} {global_params} {param_in} {param_out}:pass=2" {filter_params} -f mp4 '
                               f'{mp4_video}.mp4')
                    self._run(command, f'{mp4_video}', 'mp4')

                elif factor in 'qp':
                    command = (f'{program} {global_params} {param_in} {param_out} {filter_params} '
                               f'{mp4_video}.mp4')

                    self._run(command, f'{mp4_video}', 'mp4')

    def _encode_kvazaar(self, factor):
        program = self._check_system(self.encoder)
        params_common = (f'--input {self.yuv_video} '
                         f'-n {self.duration * self.fps} '
                         f'--input-res {self.scale} '
                         f'--input-fps {self.fps} '
                         f'-p {self.gop} '
                         '--no-tmvp '
                         '--no-open-gop ')

        if factor in 'qp':
            params_common += f'--qp {self.qp}'
        elif factor in 'rate':
            params_common += f'--bitrate {self.rate}'
        else:
            exit('Fator de qualidade só pode ser "qp" ou "rate"')

        if self.tile_format not in '1x1':
            tile_params = f' --tiles {self.tile_format} --slices tiles --mv-constraint frametilemargin'
            params_common += tile_params

        command = f'{program} {params_common} --output {self.hevc_video[factor]}.hevc'
        self._run(command, self.hevc_video[factor], 'hevc')

    def encapsule(self, factor: str):
        """
        Encapsula o vídeo usando o MP4Box quando codificado com kvazaar
        :param factor:
        :return:
        """

        if self.encoder in 'ffmpeg':
            pass
        elif self.encoder in 'kvazaar':
            mp4box = self._check_system('mp4box')
            command = f'{mp4box} -add {self.hevc_video[factor]}.hevc:split_tiles -new {self.mp4_video[factor]}.mp4'
            self._run(command, self.mp4_video[factor], 'mp4')
        else:
            print('[encapsule] Opção de encoder inválida.')

    def extract_tile(self, factor):
        """
        Extrai os tiles do vídeo quando codificado com o kvazaar com a opção -tile
        :param factor:
        :return:
        """
        if self.encoder in 'ffmpeg':
            pass
        elif self.encoder in 'kvazaar':
            mp4box = self._check_system('mp4box')

            for tile_count in range(1, self.number_tiles + 1):
                hevc_tiled_video = f'{self.mp4_video[factor]}_tile{tile_count}'
                mp4_tiled_video = f'{self.mp4_video[factor]}_tile{tile_count}'

                # Extract desired track
                track = tile_count + 1
                if self.tile_format in '1x1':
                    track = 1

                command = f'{mp4box} -raw {track} {self.mp4_video[factor]}.mp4 -out {hevc_tiled_video}.hevc'
                self._run(command, hevc_tiled_video, 'hevc')

                # Add resulting track in new mp4
                command = f'{mp4box} -add {hevc_tiled_video}.hevc -new {mp4_tiled_video}.mp4'
                self._run(command, mp4_tiled_video, 'mp4', log_mode='a')

    def make_segments(self, factor):
        """
        Codifica o vídeo usando o codificador especificado em encoder
        :type video: VideoParams
        :param video:
        :param factor:
        :return:
        """
        mp4box = self._check_system('mp4box')

        for tile_count in range(1, self.number_tiles + 1):
            mp4_tiled_video = f'{self.mp4_video[factor]}_tile{tile_count}'
            segment_log = f'{self.segment_folder[factor]}{self.sl}{self.basename[factor]}_tile{tile_count}'

            # Segment tiles in chunks
            command = f'{mp4box} -split 1 {mp4_tiled_video}.mp4 -out {self.segment_folder[factor]}{self.sl}'
            self._run(command, segment_log, 'log')


class VideoParams(Actions):
    def __init__(self, project, encoder, config, yuv, hevc, mp4, segment, dectime):
        # Initial actions
        self.sl = self._check_system('slash')
        self.scale = config['scale']
        self.fps = config['fps']
        self.gop = config['gop']
        self.duration = config['duration']

        self.encoder = encoder
        self.project = project
        self.yuv = f'{yuv}'
        self.hevc = f'{project}{self.sl}{hevc}'
        self.mp4 = f'{project}{self.sl}{mp4}'
        self.segment = f'{project}{self.sl}{segment}'
        self.dectime = f'{project}{self.sl}{dectime}'
