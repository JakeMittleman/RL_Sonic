class InnovationTracker:

    def __init__(self):
        self.innovation = 0

    def get_innovation(self):
        self.innovation += 1
        return self.innovation
