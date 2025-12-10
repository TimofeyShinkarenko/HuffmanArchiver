import struct
from typing import BinaryIO
from huffman_algorithm.tree import FrequencyTree


class Unpacker:
    def __init__(self, filename: str):
        self.filename = filename

    def unpack(self, output_filename: str = None):
        with open(self.filename, "rb") as file_in:
            padding_bytes = file_in.read(1)
            if not padding_bytes:
                return
            padding = struct.unpack("B", padding_bytes)[0]

            filename_len_bytes = file_in.read(2)
            filename_len = struct.unpack("H", filename_len_bytes)[0]
            original_filename_bytes = file_in.read(filename_len)
            original_filename = original_filename_bytes.decode("utf-8")

            target_output = output_filename if output_filename else original_filename
            freq_dict = self.read_header(file_in)

            huff_tree = FrequencyTree(freq_dict)
            huff_tree.make_tree()
            root = huff_tree.root

            with open(target_output, "wb") as file_out:
                curr_node = root
                chunk = file_in.read(1)

                while chunk:
                    byte_val = struct.unpack("B", chunk)[0]

                    next_chunk = file_in.read(1)
                    is_last_byte = not next_chunk

                    limit = padding if is_last_byte else 0

                    for i in range(7, limit - 1, -1):
                        bit = (byte_val >> i) & 1

                        if bit == 0:
                            curr_node = curr_node.left
                        else:
                            curr_node = curr_node.right

                        if curr_node.left is None and curr_node.right is None:
                            file_out.write(bytes([curr_node.char]))
                            curr_node = root
                    chunk = next_chunk

    @staticmethod
    def read_header(file_in: BinaryIO) -> dict:
        freq_dict = {}

        dict_len_bytes = file_in.read(2)
        dict_len = struct.unpack("H", dict_len_bytes)[0]

        for _ in range(dict_len):
            symbol_byte = file_in.read(1)
            symbol = struct.unpack("B", symbol_byte)[0]  # Получаем int

            freq_bytes = file_in.read(4)
            freq = struct.unpack("I", freq_bytes)[0]

            freq_dict[symbol] = freq

        return freq_dict