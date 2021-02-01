class ImageStatus:
    New = "NEW"
    Done = "DONE"
    Skipped = "SKIPPED"
    InProgress = "IN PROGRESS"
    ToReview = "TO REVIEW"
    AutoLabelled = "AUTO-LABELLED"


VALID_STATUSES = [ImageStatus.New, ImageStatus.Done, ImageStatus.Skipped, ImageStatus.InProgress, ImageStatus.ToReview,
                  ImageStatus.AutoLabelled]
