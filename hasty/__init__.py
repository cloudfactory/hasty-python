from hasty.activity import Activity, ActivityType
from hasty.attribute import Attribute
from hasty.client import Client
from hasty.dataset import Dataset
from hasty.export_job import ExportJob
from hasty.image import Image
from hasty.inference import Attributer, Detector, InstanceSegmentor, SemanticSegmentor
from hasty.label import Label
from hasty.label_class import LabelClass
from hasty.project import Project
from hasty.tag import Tag
from hasty.tag_class import TagClass
from hasty.video import Video
import hasty.label_utils as label_utils


def int_or_str(value):
    try:
        return int(value)
    except ValueError:
        return value


__version__ = '0.3.9'
VERSION = tuple(map(int_or_str, __version__.split('.')))

__all__ = [
    'Activity',
    'ActivityType'
    'Attribute',
    'Attributer',
    'Client',
    'Dataset',
    'Detector',
    'ExportJob',
    'Image',
    'InstanceSegmentor',
    'Label',
    'LabelClass',
    'Project',
    'SemanticSegmentor',
    'Tag',
    'TagClass',
    'Video',
    'label_utils',
]
