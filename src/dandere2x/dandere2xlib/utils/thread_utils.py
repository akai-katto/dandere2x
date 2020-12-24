class CancellationToken:
    def __init__(self):
        self.is_cancelled = False

    def cancel(self):
        self.is_cancelled = True
