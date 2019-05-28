from utils import util
import subprocess

config = util.Config('config.json')
system = util.check_system()
sl = system['sl']
program = system['ffmpeg']


def main():
    for name in config.videos_list:
        params_in = (f'-n -v quiet -stats -ss {config.videos_list[name]["time"]} '
                     f'-i ..{sl}original{sl}{name}.mp4')
        params_out = (f'-t 60 -r 30 -s 4160x2080 -crf 17 '
                      f'..{sl}yuv-full{sl}{name}.mp4')

        print(f'{program} {params_in} {params_out}')
        subprocess.run(f'{program} {params_in} {params_out}', shell=True)


if __name__ == '__main__':
    main()
