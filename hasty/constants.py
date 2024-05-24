class ProjectType:
    Image = "IMAGES"
    Video = "VIDEOS"


class ImageStatus:
    New = "NEW"
    Done = "DONE"
    Skipped = "SKIPPED"
    InProgress = "IN PROGRESS"
    ToReview = "TO REVIEW"
    Completed = "COMPLETED"
    AutoLabelled = "AUTO-LABELLED"


class VideoStatus:
    New = ImageStatus.New
    InProgress = ImageStatus.InProgress
    ToReview = ImageStatus.ToReview
    Done = ImageStatus.Done
    Skipped = ImageStatus.Skipped
    Completed = ImageStatus.Completed


class ExportFormat:
    JSON_v11 = "json_v1.1"
    SEMANTIC_PNG = "semantic_png"
    JSON_COCO = "json_coco"
    IMAGES = "images"


class SemanticFormat:
    GS_DESC = "gs_desc"
    GS_ASC = "gs_asc"
    CLASS_COLOR = "class_color"


class SemanticOrder:
    Z_INDEX = "z_index"
    CLASS_TYPE = "class_type"
    CLASS_ORDER = "class_order"


WAIT_INTERVAL_SEC = 10

VALID_STATUSES = [ImageStatus.New, ImageStatus.Done, ImageStatus.Skipped, ImageStatus.InProgress, ImageStatus.ToReview,
                  ImageStatus.AutoLabelled, ImageStatus.Completed]
VALID_VIDEO_STATUSES = [VideoStatus.New, VideoStatus.Done, VideoStatus.Skipped, VideoStatus.InProgress, VideoStatus.ToReview,
                        VideoStatus.Completed]
VALID_EXPORT_FORMATS = [ExportFormat.JSON_v11, ExportFormat.SEMANTIC_PNG, ExportFormat.JSON_COCO, ExportFormat.IMAGES]
VALID_SEMANTIC_FORMATS = [SemanticFormat.GS_DESC, SemanticFormat.GS_ASC, SemanticFormat.CLASS_COLOR]
VALID_SEMANTIC_ORDER = [SemanticOrder.Z_INDEX, SemanticOrder.CLASS_TYPE, SemanticOrder.CLASS_ORDER]
