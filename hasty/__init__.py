from hasty.attribute import Attribute
from hasty.client import Client
from hasty.dataset import Dataset
from hasty.image import Image
from hasty.label import Label
from hasty.label_class import LabelClass
from hasty.project import Project
import hasty.label_utils as label_utils


def int_or_str(value):
    try:
        return int(value)
    except ValueError:
        return value


__version__ = '0.0.7'
VERSION = tuple(map(int_or_str, __version__.split('.')))

__all__ = [
    'Attribute',
    'Client',
    'Dataset',
    'LabelClass',
    'Project',
    'label_utils'
]
