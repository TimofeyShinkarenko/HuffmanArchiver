import hashlib
import os


class Hasher:
    @staticmethod
    def get_file_hash(filename: str) -> bytes:
        sha256 = hashlib.sha256()

        with open(filename, 'rb') as f:
            while True:
                chunk = f.read(65536)
                if not chunk:
                    break
                sha256.update(chunk)

        return sha256.digest()