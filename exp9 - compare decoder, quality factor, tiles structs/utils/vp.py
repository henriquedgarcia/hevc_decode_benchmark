import platform
import os
import sys

class Atribs:
    def __init__(self):
        self.config = Config
        self.encoder = ''
        self.project = ''
        self.sl = ''

        # imutable stats
        self.scale = ''
        self.fps = 0
        self.gop = 0
        self.duration = 0

        # mutable stats
        self._name = ''
        self.fmt = ''
        self.factor = ''
        self._quality = 0

        # folders
        self.yuv = ''
        self.hevc = ''
        self.mp4 = ''
        self.segment = ''
        self.dectime = ''

        # names
        self.basename = ''
        self.yuv_video = ''

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value
        self.yuv_video = f'{self.yuv}{self.sl}{self._name}'

    @property
    def quality(self):
        return self._quality

    @quality.setter
    def quality(self,value):
        self._quality = value
        self.basename = f'{self.name}_{self.scale}_{self.fps}_{self.fmt}_{self.factor}{self._quality}'


class VideoParams(Atribs):
    def __init__(self, config: util.Config, yuv, hevc, mp4, segment, dectime):
        super().__init__()
        # Initial actions
        self.config = config
        self.sl = self.check_system()['slash']

        self.scale = config.scale
        self.fps = config.fps
        self.gop = config.gop
        self.duration = config.duration

        self._name = ''
        self.fmt = ''
        self.factor = ''
        self.quality_list = []

        self.encoder = encoder
        self.project = project

        self.yuv = f'{yuv}'
        self.hevc = f'{project}{self.sl}{hevc}'
        self.mp4 = f'{project}{self.sl}{mp4}'
        self.segment = f'{project}{self.sl}{segment}'
        self.dectime = f'{project}{self.sl}{dectime}'

    @staticmethod
    def check_system() -> dict:
        if platform.system() == 'Windows':
            sl = '\\'
            ffmpeg = 'ffmpeg.exe'
            mp4box = 'C:\\"Program Files"\\GPAC\\MP4Box.exe'
            mp4client = 'C:\\"Program Files"\\GPAC\\MP4Client.exe'
            kvazaar = 'bin\\kvazaar.exe'
            siti = 'bin\\SITI.exe'
        else:
            sl = '/'
            ffmpeg = 'ffmpeg'
            mp4box = 'MP4Box'
            kvazaar = 'kvazaar'
            siti = 'bin/siti'
            mp4client = 'MP4Client'

        programs = dict(sl=sl,
                        ffmpeg=ffmpeg,
                        mp4box=mp4box,
                        kvazaar=kvazaar,
                        siti=siti,
                        mp4client=mp4client)
        return programs
