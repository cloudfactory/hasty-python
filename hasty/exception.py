class ValidationException(Exception):
    def __init__(self, message):
        self.message = message

    @classmethod
    def export_in_progress(cls):
        raise ValidationException("Export is still running")


class LimitExceededException(Exception):
    def __init__(self, message):
        self.message = message

    @classmethod
    def max_labels_per_batch(cls, got):
        return LimitExceededException(f"Max number of labels per batch is 100, got {got}")

    @classmethod
    def max_tags_per_batch(cls, got):
        return LimitExceededException(f"Max number of tags per batch is 100, got {got}")


class InferenceException(Exception):
    def __init__(self, message):
        self.message = message

    @classmethod
    def model_not_loaded(cls):
        return InferenceException("Model not loaded")
