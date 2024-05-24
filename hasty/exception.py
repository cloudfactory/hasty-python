class ValidationException(Exception):
    def __init__(self, message):
        self.message = message

    @classmethod
    def export_in_progress(cls):
        return ValidationException("Export is still running")

    @classmethod
    def video_not_ready(cls):
        return ValidationException("Video is not ready")

    @classmethod
    def invalid_activities(cls):
        return ValidationException("activities must be a non-empty list of ActitivityType objects or IDs")

class AuthenticationException(Exception):
    def __init__(self, message):
        self.message = message

    @classmethod
    def failed_authentication(cls):
        return AuthenticationException("Authentication failed, check your API key")


class AuthorisationException(Exception):
    def __init__(self, message):
        self.message = message

    @classmethod
    def permission_denied(cls):
        return AuthorisationException("Looks like service account doesn't have a permission to perform this operation")


class InsufficientCredits(Exception):
    def __init__(self, message):
        self.message = message

    @classmethod
    def insufficient_credits(cls):
        return InsufficientCredits("Looks like you out of credits, please top up your account or contact Hasty")


class NotFound(Exception):
    def __init__(self, message):
        self.message = message

    @classmethod
    def object_not_found(cls):
        return NotFound("Referred object not found, please check your script")


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
