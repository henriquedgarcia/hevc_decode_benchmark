from SITI import siti


def main():
    siti.multi_plot('csv\\*.csv')
    siti.single_plot('csv\\*.csv')


if __name__ == "__main__":
    main()
