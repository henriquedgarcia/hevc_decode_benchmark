#!/bin/env python3
import os
import shutil
from utils import util

# Configuration
proc_num = 4
duration = 10,
scale = '4320x2160'
w = 4320
h = 2160
fps = 30
gop = 30

qp_list = [20, 25, 30, 35, 40]
rate_list = [2000000, 4000000, 8000000, 16000000, 24000000]
# tile_list = ['1x1', '6x4', '12x8']
tile_list = ['6x4', '12x8']


def main():
    programs = util.check_system()
    kvazaar = programs['kvazaar']
    mp4box = programs['mp4box']
    sl = programs['sl']

    # videos = util.list_videos('input.json')

    videos = {"pac_man": 0,
              "rollercoaster": 0,
              "lions": 0,
              "om_nom": 0}

    yuv_folder = 'yuv'
    hevc_base_folder = 'hevc'
    mp4_base_folder = 'mp4'
    dash_folder = 'dash'

    for name in videos:
        for tile in tile_list:
            m, n = list(map(int, tile.split('x')))
            for rate, qp in list(zip(rate_list, qp_list)):
                basename = f'{name}_{scale}_{fps}_{tile}'

                # ----------------------------------------------
                # Encode
                # ----------------------------------------------
                yuv_video_name = f'{yuv_folder}{sl}{name}_{scale}_{fps}'

                hevc_folder = f'{hevc_base_folder}{sl}{basename}'
                hevc_video_qp = f'{hevc_folder}{sl}{basename}_qp{qp}'
                hevc_video_rate = f'{hevc_folder}{sl}{basename}_rate{rate}'

                os.makedirs(f'{hevc_folder}', exist_ok=True)

                params_common = (f'--input {yuv_video_name}.yuv '
                                 f'--input-res {scale} '
                                 f'--input-fps {fps} '
                                 f'-p {gop} '
                                 '--no-tmvp '
                                 '--no-open-gop')
                params_qp = f'{params_common} --qp {qp} --output {hevc_video_qp}.hevc'
                params_rate = f'{params_common} --bitrate {rate} --output {hevc_video_rate}.hevc'

                if tile is not '1x1':
                    tile_params = f' --tiles {tile} --slices tiles --mv-constraint frametilemargin'
                    params_qp += tile_params
                    params_rate += tile_params

                # command = f'{kvazaar} {params_qp}'
                # util.run(command, hevc_video_qp, 'hevc')

                # command = f'{kvazaar} {params_rate}'
                # util.run(command, hevc_video_rate, 'hevc')

                # ----------------------------------------------
                # Encapsule
                # ----------------------------------------------
                mp4_folder = f'{mp4_base_folder}{sl}{basename}'
                mp4_video_qp = f'{mp4_folder}{sl}{basename}_qp{qp}'
                mp4_video_rate = f'{mp4_folder}{sl}{basename}_rate{rate}'

                os.makedirs(f'{mp4_folder}', exist_ok=True)

                # command = f'{mp4box} -add {hevc_video_qp}.hevc:split_tiles -new {mp4_video_qp}.mp4'
                # util.run(command, mp4_video_qp, 'mp4')
                #
                # command = f'{mp4box} -add {hevc_video_rate}.hevc:split_tiles -new {mp4_video_rate}.mp4'
                # util.run(command, mp4_video_rate, 'mp4')

                # # ----------------------------------------------
                # # Extract Tiles
                # # ----------------------------------------------
                for tile_count in range(1, m * n + 1):
                    track = tile_count + 1
                    mp4_tile_video_qp_folder = f'{dash_folder}{sl}{basename}_qp{qp}'
                    mp4_tile_video_rate_folder = f'{dash_folder}{sl}{basename}_rate{rate}'
                    os.makedirs(f'{mp4_tile_video_qp_folder}', exist_ok=True)
                    os.makedirs(f'{mp4_tile_video_rate_folder}', exist_ok=True)

                    mp4_video_tile_qp = f'{mp4_tile_video_qp_folder}{sl}{name}_tile{tile_count}'
                    mp4_video_tile_rate = f'{mp4_tile_video_rate_folder}{sl}{name}_tile{tile_count}'

                    mp4_video_segment_qp_folder = f'{mp4_tile_video_qp_folder}{sl}segments'
                    mp4_video_segment_rate_folder = f'{mp4_tile_video_rate_folder}{sl}segments'
                    os.makedirs(f'{mp4_video_segment_qp_folder}', exist_ok=True)
                    os.makedirs(f'{mp4_video_segment_rate_folder}', exist_ok=True)

                    mp4_video_segment_qp = f'{mp4_video_segment_qp_folder}{sl}{name}_tile{tile_count}_track{track}_001'
                    mp4_video_segment_rate = f'{mp4_video_segment_rate_folder}{sl}{name}_tile{tile_count}_track{track}_001'

                    mp4_video_tile_track_qp = f'{mp4_video_tile_qp}_track{track}'
                    mp4_video_tile_track_rate = f'{mp4_video_tile_rate}_track{track}'

                    # Se tile == 1x1 (pois não tem base track) apenas copiar arquivo para destino
                    if tile in '1x1':
                        # mp4_video_segment_qp = f'{mp4_video_segment_qp_folder}{sl}{name}_tile{tile_count}_001'
                        # mp4_video_segment_rate = f'{mp4_video_segment_rate_folder}{sl}{name}_tile{tile_count}_001'

                        if os.path.isfile(f'{mp4_video_tile_track_qp}.mp4'):
                            print(f'O arquivo {mp4_video_tile_track_qp}.mp4 existe. Pulando.')
                        else:
                            shutil.copyfile(f'{mp4_video_qp}.mp4', f'{mp4_video_tile_track_qp}.mp4')

                        if os.path.isfile(f'{mp4_video_tile_track_rate}.mp4'):
                            print(f'O arquivo {mp4_video_tile_track_rate}.mp4 existe. Pulando.')
                        else:
                            shutil.copyfile(f'{mp4_video_rate}.mp4', f'{mp4_video_tile_track_rate}.mp4')

                        # Segment track
                        command = f'{mp4box} -split 1 {mp4_video_tile_track_qp}.mp4 -out {mp4_video_segment_qp_folder}{sl}'
                        util.run(command, mp4_video_segment_qp, 'mp4', overwrite=False)

                        command = f'{mp4box} -split 1 {mp4_video_tile_track_rate}.mp4 -out {mp4_video_segment_rate_folder}{sl}'
                        util.run(command, mp4_video_segment_rate, 'mp4', overwrite=False)

                    else:
                        # Remove undesired track
                        rem_option = ''
                        for tile_removed in range(2, (m * n) + 2):
                            if tile_removed == track:
                                continue
                            rem_option += f'-rem {tile_removed} '

                        command = f'{mp4box} {rem_option} {mp4_video_qp}.mp4 -out {mp4_video_tile_qp}.mp4'
                        print(command)
                        util.run(command, mp4_video_tile_qp, 'mp4')

                        command = f'{mp4box} {rem_option} {mp4_video_rate}.mp4 -out {mp4_video_tile_rate}.mp4'
                        util.run(command, mp4_video_tile_rate, 'mp4')

                        # Extract track desired (track) only for stats, and track 1, the resulting track.
                        # command = f'{mp4box} -raw {track} -raw 1 {mp4_video_tile_qp}.mp4'
                        command = f'{mp4box} -raw {track} {mp4_video_tile_qp}.mp4'
                        util.run(command, mp4_video_tile_track_qp, 'hvc')

                        # command = f'{mp4box} -raw {track} -raw 1 {mp4_video_tile_rate}.mp4'
                        command = f'{mp4box} -raw {track} {mp4_video_tile_rate}.mp4'
                        util.run(command, mp4_video_tile_track_rate, 'hvc')

                        # Add resulting track in new mp4
                        command = f'{mp4box} -add {mp4_video_tile_track_qp}.hvc -new {mp4_video_tile_track_qp}.mp4'
                        util.run(command, mp4_video_tile_track_qp, 'mp4', overwrite=False)

                        command = f'{mp4box} -add {mp4_video_tile_track_rate}.hvc -new {mp4_video_tile_track_rate}.mp4'
                        util.run(command, mp4_video_tile_track_rate, 'mp4', overwrite=False)

                        # Segment track
                        command = f'{mp4box} -split 1 {mp4_video_tile_track_qp}.mp4 -out {mp4_video_segment_qp_folder}{sl}'
                        util.run(command, f'{mp4_video_segment_qp}', 'mp4')

                        command = f'{mp4box} -split 1 {mp4_video_tile_track_rate}.mp4 -out {mp4_video_segment_rate_folder}{sl}'
                        util.run(command, f'{mp4_video_segment_rate}', 'mp4')


if __name__ == '__main__':
    main()
