
class Bar():
    def __init__(self, last:float):

        self.open:float = last
        self.high:float = last
        self.low:float = last
        self.close:float = last

    def sort(self, last):
        self.close = last

        if last > self.high:
            self.high = last

        if last < self.low:
            self.low = last




