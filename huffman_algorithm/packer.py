import os
import tarfile

class Packer:
    def __init__(self, archive_name: str):
        self.archive_name = archive_name

    def pack(self, sources: list):
        with tarfile.open(self.archive_name, "w") as tar:
            for source in sources:
                if os.path.exists(source):
                    clean_name = os.path.basename(source)
                    tar.add(source, arcname=clean_name)
                else:
                    print(f"Warning: '{source}' not found and skipped.")

    def unpack(self, output_folder: str = "."):
        os.makedirs(output_folder, exist_ok=True)

        with tarfile.open(self.archive_name, "r") as tar:
            try:
                tar.extractall(path=output_folder, filter='data')
            except TypeError:
                tar.extractall(path=output_folder)