from SITI import siti
import glob


def main():
    for video in glob.glob('om_nom*.mp4'):
        siti.siti(filename=video, num_frames=300)
    #
    siti.multi_plot('*.csv', output_folder='graph3-om_nom')
    # siti.single_plot('*.csv', output_folder='graph3-om_nom')


if __name__ == "__main__":
    main()
