#!/usr/bin/env python3
import argparse
from archiver import Archiver
from unpacker import Unpacker


def parse_arguments():
    huffman_parser = argparse.ArgumentParser(
        description='Huffman Code Generator'
    )

    huffman_parser.add_argument(
        "-u", "--unpack",
        action="store_true",
        help="unpack file"
    )
    huffman_parser.add_argument(
        "-a", "--archive",
        action="store_true",
        help='archive file'
    )
    huffman_parser.add_argument(
        'filename',
        type=str,
        help='input filename'
    )

    return huffman_parser.parse_args()


def run():
    try:
        args = parse_arguments()

        if args.unpack:
            unpacker = Unpacker(args.filename)
            unpacker.unpack()
            print(f"File {args.filename} unpacked successfully.")

        elif args.archive:
            archiver = Archiver(args.filename)
            output_filename = args.filename + ".huff"
            archiver.compress(output_filename)
            print(f"File {args.filename} archived to {output_filename}")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == '__main__':
    run()