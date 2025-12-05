class FrequencyCounter:
    def __init__(self, filename: str):
        self.inclusions = {}
        self.filename = filename

    def count_in_text(self, text: bytes):
        for byte_val in text:
            if byte_val not in self.inclusions:
                self.inclusions[byte_val] = 0
            self.inclusions[byte_val] += 1

    def get_frequency_dict(self):
        with open(self.filename, 'rb') as f:
            while True:
                chunk = f.read(4096)
                if not chunk:
                    break

                self.count_in_text(chunk)

        return self.inclusions