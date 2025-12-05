class FrequencyCounter:
    def __init__(self, filename: str):
        self.inclusions = {}
        self.filename = filename

    def count_in_text(self, text: str):
        for symbol in text:
            if symbol not in self.inclusions:
                self.inclusions[symbol] = 0
            self.inclusions[symbol] += 1

    def get_frequency_dict(self):
        with open(self.filename, 'r') as f:
            while True:
                chunk = f.read(4096)
                if not chunk:
                    break

                self.count_in_text(chunk)

        return self.inclusions