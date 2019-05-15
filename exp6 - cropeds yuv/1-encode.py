#!/bin/env python3
import os
import platform
import shlex
import subprocess


if platform.system() == 'Windows':
    slash = '\\'
    ffmpeg = 'ffmpeg.exe'
    mp4box = '"C:\Program Files\GPAC\MP4Box.exe"'

else:
    slash = '/'
    ffmpeg = 'ffmpeg'
    mp4box = 'MP4Box'


def main():

    video_list = dict(pac_man='yuv' + slash + 'pac_man.yuv',
                      clans='yuv' + slash + 'clans.yuv',
                      super_mario='yuv' + slash + 'super_mario.yuv',
                      rollercoaster='yuv' + slash + 'rollercoaster.yuv',
                      ski='yuv' + slash + 'ski.yuv',
                      surf='yuv' + slash + 'surf.yuv',
                      jaws='yuv' + slash + 'jaws.yuv',
                      lions='yuv' + slash + 'lions.yuv',
                      maldives='yuv' + slash + 'maldives.yuv',
                      om_nom='yuv' + slash + 'om_nom.yuv',
                      elephants='yuv' + slash + 'elephants.yuv',
                      ninja_turtles='yuv' + slash + 'ninja_turtles.yuv'
                      )

    size = '4320x2160'
    w, h = list(map(int, size.split('x')))
    fps = 30
    gop = fps
    rate_list = [1500000, 3000000, 6000000, 12000000, 24000000]
    # tile_list = ['1x1', '6x4', '12x8']
    tile_list = ['6x4', '12x8']

    for name in video_list:
        video_in = video_list[name]

        for tile in tile_list:
            m, n = list(map(int, tile.split('x')))
            tile_w = int(w / m)
            tile_h = int(h / n)

            for rate in rate_list:
                tile_rate = int(rate / (m * n))
                base_name = f'{name}_{tile}_{tile_rate}'
                hevc_folder = 'hevc' + slash + base_name
                os.makedirs(hevc_folder, exist_ok=True)

                tile_count = 0

                for x in range(0, w, tile_w):
                    for y in range(0, int(h), tile_h):
                        tile_count += 1
                        out_name = f'{base_name}_tile{tile_count}'

                        # Encode params
                        global_params = '-hide_banner -n'
                        in_params = (f'-s {size} '
                                     f'-framerate {fps} '
                                     f'-i {video_in}')
                        encode_params = (f'-codec libx265 -b:v {tile_rate} '
                                         f'-x265-params "keyint={gop}:min-keyint={gop}:open-gop=0:info=0"')
                        filter_params = f'-vf "crop=w={tile_w}:h={tile_h}:x={x}:y={y}"'
                        hevc_output = f'{hevc_folder}{slash}{out_name}.hevc'

                        command = f'{ffmpeg} {global_params} {in_params} {encode_params} {filter_params} {hevc_output}'
                        print(command)

                        #  print(f'Codificando {out_name}')
                        #  try:
                        #    with open(hevc_output, 'r') as f:
                        #         pass
                        #  except IOError:
                        #     continue

                        subprocess.call(command, shell=True)

                        # Puting hevc in mp4
                        in_param = f'-add {hevc_output}'
                        out_params = f'-new {hevc_folder}{slash}{out_name}.mp4'

                        command = f'{mp4box} {in_param} {out_params}'
                        print(command)
                        print(f'Multiplexando {out_name}')
                        subprocess.call(command, shell=True)
                        # run_command(command)


if __name__ == '__main__':
    main()
