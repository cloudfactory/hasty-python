class ValidationException(Exception):
    def __init__(self, message):
        self.message = message


class LimitExceededException(Exception):
    def __init__(self, message):
        self.message = message

    @classmethod
    def max_labels_per_batch(cls, got):
        return LimitExceededException(f"Max number of labels per batch is 100, got {got}")
