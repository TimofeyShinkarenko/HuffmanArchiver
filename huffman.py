import argparse
import os
from huffman_algorithm.archiver import Archiver
from huffman_algorithm.unpacker import Unpacker
from huffman_algorithm.packer import Packer


def parse_arguments():
    huffman_parser = argparse.ArgumentParser(
        description='Huffman Archiver with Tar support'
    )

    group = huffman_parser.add_mutually_exclusive_group(required=True)

    group.add_argument(
        "-a", "--archive",
        nargs='+',
        help='Compress files or directories. Usage: -a file1.txt folder2 ...'
    )

    group.add_argument(
        "-u", "--unpack",
        type=str,
        help='Unpack a .huff archive. Usage: -u archive.tar.huff'
    )

    huffman_parser.add_argument(
        "-o", "--output",
        type=str,
        help='Output filename (optional)'
    )

    return huffman_parser.parse_args()


def run():
    try:
        args = parse_arguments()

        if args.archive:
            files_to_pack = args.archive

            if args.output:
                final_output_name = args.output
            else:
                base_name = os.path.basename(files_to_pack[0])
                final_output_name = f"{base_name}.tar.huff"

            temp_tar_name = "temp_intermediate.tar"

            packer = Packer(temp_tar_name)
            packer.pack(files_to_pack)

            archiver = Archiver(temp_tar_name)
            archiver.compress(final_output_name)

            if os.path.exists(temp_tar_name):
                os.remove(temp_tar_name)

        elif args.unpack:
            input_huff_file = args.unpack
            temp_tar_restored = "temp_restored.tar"

            unpacker = Unpacker(input_huff_file)
            unpacker.unpack(output_filename=temp_tar_restored)

            output_dir = args.output if args.output else "."

            packer = Packer(temp_tar_restored)
            packer.unpack(output_folder=output_dir)

            os.remove(temp_tar_restored)

    except Exception as e:
        print(e)
        if os.path.exists("temp_intermediate.tar"):
            os.remove("temp_intermediate.tar")
        if os.path.exists("temp_restored.tar"):
            os.remove("temp_restored.tar")


if __name__ == '__main__':
    run()