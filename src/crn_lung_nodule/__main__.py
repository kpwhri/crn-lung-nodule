import argparse

from crn_lung_nodule.danforth_20130919 import extract
from crn_lung_nodule.util.constants import ALGORITHMS


def main():
    parser = argparse.ArgumentParser(fromfile_prefix_chars='@')
    parser.add_argument('-i', '--input-dir', required=True,
                        help='Name of input directory containing text files.')
    parser.add_argument('-o', '--output', required=True,
                        help='Name of output file.')
    parser.add_argument('-L', '--log-dir', default='log',
                        help='Directory to output log files.')
    parser.add_argument('-a', '--algorithm', choices=ALGORITHMS,
                        help='Algorithm to use: {}.'.format(', '.join(ALGORITHMS)))
    parser.add_argument('--psm', required=True,
                        help='Name of phrase search method to be used.')
    parser.add_argument('--r6psm', default=None,
                        help='Rule 6 phrase search method to be used '
                             '(defaults to psm).')
    parser.add_argument('--get-largest-nodule-size', action='store_true',
                        default=False,
                        help='Retrieve largest nodule size.')
    args = parser.parse_args()

    # todo: set logger
    if not args.r6psm:
        args.r6psm = args.psm

    extract(args.input_dir, args.psm, args.get_largest_nodule_size,
            args.r6psm, algorithm=args.algorithm, outfn=args.output)


if __name__ == '__main__':
    main()
