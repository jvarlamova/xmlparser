import argparse
import os

from xmlparser import xml_generator
from xmlparser import xml_processor


CSV_EXTENSION = '.csv'


def generate(args):
    try:
        xml_generator.generate_zip_archives(args.directory,
                                            args.zip_count,
                                            args.xml_count)
    except Exception as e:
        print('Unexpected error: {}'.format(e))
    else:
        print('Successfully created .zip arcives with .xml files.')


def parse(args):
    for csv in (args.id_level_csv, args.id_objects_csv):
        if csv and os.path.splitext(csv)[1] != CSV_EXTENSION:
            print('Wrong file extension: {}. Should be .csv'.format(csv))
            return
    try:
        xml_processor.process_zip_archives(args.directory,
                                           args.id_level_csv,
                                           args.id_objects_csv)
    except Exception as e:
        print('Unexpected error: {}'.format(e))
    else:
        print('Successfully processed all valid .zip files and '
              'parsed all valid .xml files.')


def args_parser():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    generate_parser = subparsers.add_parser(
        'generate',
        help='Generate zip-archives with xml-files')
    generate_parser.add_argument(
        '--zip-count',
        type=int,
        default=50,
        help='Count of .zip archives to generate.')
    generate_parser.add_argument(
        '--xml-count',
        type=int,
        default=100,
        help='Count of .xml files per archive')
    generate_parser.set_defaults(func=generate)

    parse_parser = subparsers.add_parser(
        'parse',
        help='Parse xml files.')
    parse_parser.set_defaults(func=parse)
    parse_parser.add_argument(
        '--id-level-csv',
        default='id_level.csv',
        help='.csv file for id-level mapping.')
    parse_parser.add_argument(
        '--id-objects-csv',
        default='id_objects.csv',
        help='.csv file for id-objects mapping.')

    parser.add_argument('directory')
    return parser


def main():
    args = args_parser().parse_args()
    args.func(args)
