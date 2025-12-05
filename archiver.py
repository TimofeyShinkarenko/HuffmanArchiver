import struct
import os  # Добавили импорт
from typing import BinaryIO
from tree import FrequencyTree
from counter import FrequencyCounter


class Archiver:
    def __init__(self, filename: str):
        self.filename = filename
        self.counter = FrequencyCounter(filename)
        self.freq_dict = self.counter.get_frequency_dict()
        self.tree = FrequencyTree(self.freq_dict)
        self.tree.make_tree()
        self.codes = self.tree.generate_codes()

    def compress(self, output_filename: str):
        with (open(self.filename, 'r', encoding='utf-8') as file_in, open(
                output_filename, 'wb') as file_out):
            file_out.write(struct.pack('B', 0))
            self.write_header(file_out)

            buffer = 0
            bit_count = 0

            while True:
                chunk = file_in.read(4096)
                if not chunk:
                    break

                for char in chunk:
                    code = self.codes[char]

                    for bit in code:
                        buffer = (buffer << 1) | int(bit)
                        bit_count += 1

                        if bit_count == 8:
                            file_out.write(struct.pack('B', buffer))
                            buffer = 0
                            bit_count = 0

            padding = 0
            if bit_count > 0:
                padding = 8 - bit_count
                buffer = buffer << padding
                file_out.write(struct.pack('B', buffer))

            file_out.seek(0)
            file_out.write(struct.pack('B', padding))

            return file_out

    def write_header(self, file_out: BinaryIO):
        # 1. Записываем оригинальное имя файла
        base_filename = os.path.basename(self.filename)
        filename_bytes = base_filename.encode('utf-8')
        # H - unsigned short (2 байта), длины имени хватит до 65535 символов
        file_out.write(struct.pack('H', len(filename_bytes)))
        file_out.write(filename_bytes)

        # 2. Записываем словарь частот
        file_out.write(struct.pack('H', len(self.freq_dict)))

        for char, freq in self.freq_dict.items():
            char_bytes = char.encode('utf-8')
            file_out.write(struct.pack('B', len(char_bytes)))
            file_out.write(char_bytes)
            file_out.write(struct.pack('I', freq))