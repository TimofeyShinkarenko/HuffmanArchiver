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

    # 1. Архивация
    group.add_argument(
        "-a", "--archive",
        nargs='+',
        help='Compress files or directories.'
    )

    # 2. Распаковка
    group.add_argument(
        "-u", "--unpack",
        type=str,
        help='Unpack a .huff archive.'
    )

    # 3. НОВОЕ: Листинг
    group.add_argument(
        "-l", "--list",
        type=str,
        help='List contents of a .huff archive without extracting.'
    )

    huffman_parser.add_argument(
        "-o", "--output",
        type=str,
        help='Output filename (optional)'
    )

    return huffman_parser.parse_args()


def run():
    temp_tar_name = "temp.tar"

    try:
        args = parse_arguments()

        if args.archive:
            files_to_pack = args.archive
            if args.output:
                final_output_name = args.output
            else:
                base_name = os.path.basename(files_to_pack[0])
                final_output_name = f"{base_name}.tar.huff"

            packer = Packer(temp_tar_name)
            packer.pack(files_to_pack)

            archiver = Archiver(temp_tar_name)
            archiver.compress(final_output_name)


        elif args.unpack:
            input_huff_file = args.unpack

            unpacker = Unpacker(input_huff_file)
            unpacker.unpack(output_filename=temp_tar_name)

            output_dir = args.output if args.output else "."
            packer = Packer(temp_tar_name)
            packer.unpack(output_folder=output_dir)

        elif args.list:
            input_huff_file = args.list

            unpacker = Unpacker(input_huff_file)
            unpacker.unpack(output_filename=temp_tar_name)

            if os.path.exists(temp_tar_name):
                packer = Packer(temp_tar_name)
                packer.list_contents()
            else:
                print("Error: Could not read archive structure.")

    except Exception as e:
        print(e)

    finally:
        if os.path.exists(temp_tar_name):
            os.remove(temp_tar_name)


if __name__ == '__main__':
    run()