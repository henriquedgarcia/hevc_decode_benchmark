import glob

from SITI import siti
from utils import util

sl = util.check_system()['sl']


def main():
    #for video in glob.glob(f'..{sl}yuv-full{sl}*.mp4'):
    #    siti.siti(filename=video)

    siti.multi_plot(f'..{sl}yuv-full{sl}*.csv', output_folder='todos_os_videos_ate_agora')
    siti.single_plot(f'..{sl}yuv-full{sl}*.csv', output_folder='todos_os_videos_ate_agora')


if __name__ == "__main__":
    main()
