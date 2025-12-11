import unittest
import os
import shutil
import tempfile

from huffman_algorithm.archiver import Archiver
from huffman_algorithm.unpacker import Unpacker


class TestHuffmanArchiver(unittest.TestCase):

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_text_file_cycle(self):
        original_content = b"Hello, world! 1234567890"
        input_file = os.path.join(self.test_dir, "input.txt")
        archive_file = os.path.join(self.test_dir, "archive.huff")
        output_file = os.path.join(self.test_dir, "restored.txt")

        with open(input_file, 'wb') as f:
            f.write(original_content)

        archiver = Archiver(input_file)
        archiver.compress(archive_file)

        self.assertTrue(os.path.exists(archive_file),
                        "Файл архива не был создан")

        unpacker = Unpacker(archive_file)
        unpacker.unpack(output_filename=output_file)

        with open(output_file, 'rb') as f:
            restored_content = f.read()

        self.assertEqual(original_content, restored_content,
                         "Содержимое распакованного файла не совпадает с оригиналом")

    def test_integrity_check(self):
        input_file = os.path.join(self.test_dir, "data.bin")
        archive_file = os.path.join(self.test_dir, "data.huff")

        original_data = bytes(range(256)) * 10
        with open(input_file, 'wb') as f:
            f.write(original_data)

        Archiver(input_file).compress(archive_file)

        output_file = os.path.join(self.test_dir, "data_out.bin")
        try:
            Unpacker(archive_file).unpack(output_file)
        except ValueError as e:
            self.fail(f"Распаковка упала с ошибкой хеша: {e}")

        with open(output_file, 'rb') as f:
            self.assertEqual(f.read(), original_data)

    def test_corrupted_archive(self):
        input_file = os.path.join(self.test_dir, "doc.txt")
        archive_file = os.path.join(self.test_dir, "doc.huff")

        with open(input_file, 'wb') as f:
            f.write(b"Secret data")

        Archiver(input_file).compress(archive_file)

        with open(archive_file, 'r+b') as f:
            f.seek(-1, os.SEEK_END)
            byte = f.read(1)
            new_byte = bytes([byte[0] ^ 0xFF])
            f.seek(-1, os.SEEK_END)
            f.write(new_byte)

        unpacker = Unpacker(archive_file)
        output_file = os.path.join(self.test_dir, "corrupted_out.txt")

        with self.assertRaises(ValueError) as cm:
            unpacker.unpack(output_file)

        self.assertIn("Integrity Check failed", str(cm.exception))


if __name__ == '__main__':
    unittest.main()