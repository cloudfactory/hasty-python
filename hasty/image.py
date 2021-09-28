from collections import OrderedDict
from typing import Dict, List, Union
import os
import urllib.request

from .constants import VALID_STATUSES
from .hasty_object import HastyObject
from .helper import PaginatedList
from .exception import ValidationException
from .label import Label
from .label_class import LabelClass
from .tag import Tag
from .tag_class import TagClass


class Image(HastyObject):
    endpoint = '/v1/projects/{project_id}/images'
    endpoint_uploads = '/v1/projects/{project_id}/image_uploads'
    endpoint_image = '/v1/projects/{project_id}/images/{image_id}'

    def __repr__(self):
        return self.get__repr__(OrderedDict({"id": self._id, "dataset_name": self._dataset_name, "name": self._name,
                                             "width": self._width, "height": self._height}))

    @property
    def id(self):
        """
        :type: string
        """
        return self._id

    @property
    def name(self):
        """
        :type: string
        """
        return self._name

    @property
    def project_id(self):
        """
        :type: string
        """
        return self._project_id

    @property
    def dataset_id(self):
        """
        :type: string
        """
        return self._dataset_id

    @property
    def dataset_name(self):
        """
        :type: string
        """
        return self._dataset_name

    @property
    def width(self):
        """
        :type: int
        """
        return self._width

    @property
    def height(self):
        """
        :type: int
        """
        return self._height

    @property
    def status(self):
        """
        :type: string
        """
        return self._status

    @property
    def public_url(self):
        """
        :type: string
        """
        return self._public_url

    def _init_properties(self):
        self._id = None
        self._name = None
        self._project_id = None
        self._dataset_name = None
        self._width = None
        self._height = None
        self._status = None
        self._public_url = None

    def _set_prop_values(self, data):
        if "id" in data:
            self._id = data["id"]
        if "name" in data:
            self._name = data["name"]
        if "project_id" in data:
            self._project_id = data["project_id"]
        if "dataset_id" in data:
            self._dataset_id = data["dataset_id"]
        if "dataset_name" in data:
            self._dataset_name = data["dataset_name"]
        if "width" in data:
            self._width = data["width"]
        if "height" in data:
            self._height = data["height"]
        if "status" in data:
            self._status = data["status"]
        if "public_url" in data:
            self._public_url = data["public_url"]

    @staticmethod
    def _get_by_id(requester, project_id, image_id):
        data = requester.get(Image.endpoint_image.format(project_id=project_id, image_id=image_id))
        return Image(requester, data, {"project_id": project_id})

    @staticmethod
    def _generate_sign_url(requester, project_id):
        data = requester.post(Image.endpoint_uploads.format(project_id=project_id), json_data={"count": 1})
        return data["items"][0]

    @staticmethod
    def _upload_from_file(requester, project_id, dataset_id, filepath):
        filename = os.path.basename(filepath)
        url_data = Image._generate_sign_url(requester, project_id)
        with open(filepath, 'rb') as f:
            requester.put(url_data['url'], data=f.read(), content_type="image/*")
        res = requester.post(Image.endpoint.format(project_id=project_id),
                             json_data={"dataset_id": dataset_id,
                                        "filename": filename,
                                        "upload_id": url_data["id"]})
        return Image(requester, res, {"project_id": project_id,
                                      "dataset_id": dataset_id})

    @staticmethod
    def _upload_from_url(requester, project_id, dataset_id, filename, url, copy_original=True):
        res = requester.post(Image.endpoint.format(project_id=project_id),
                             json_data={"dataset_id": dataset_id,
                                        "filename": filename,
                                        "url": url,
                                        "copy_original": copy_original})
        return Image(requester, res, {"project_id": project_id,
                                      "dataset_id": dataset_id})

    def get_labels(self):
        """
        Returns image labels (list of `~hasty.Label` objects)
        """
        return PaginatedList(Label, self._requester,
                             Label.endpoint_image.format(project_id=self.project_id, image_id=self.id),
                             obj_params={"project_id": self.project_id})

    def create_label(self, label_class: Union[LabelClass, str], bbox: List[int] = None, polygon: List[List[int]] = None,
                     mask: List[int] = None, z_index: int = None):
        """
        Create label

        Args:
            label_class (LabelClass, str): Label class or label class ID of the label
            bbox (list of int): Coordinates of bounding box [x_min, y_min, x_max, y_max]
            polygon (list): List of x, y pairs [[x0, y0], [x1, y1], .... [x0, y0]]
            mask (list of int): RLE Encoded binary mask, (order right -> down)
            z_index (int): Z index of the label. A label with greater value is in front of a label with a lower one.
        """
        class_id = label_class
        if isinstance(label_class, LabelClass):
            class_id = label_class.id
        label = Label._create(self._requester, self._project_id, self._id, class_id, bbox, polygon, mask, z_index)
        return label

    def create_labels(self, labels):
        """
        Create multiple labels. Returns a list of `~hasty.Label` objects

        Args:
            labels (list of dict): List of labels, keys:
                    class_id: Label class ID of the label
                    bbox: Coordinates of bounding box [x_min, y_min, x_max, y_max]
                    polygon: List of x, y pairs [[x0, y0], [x1, y1], .... [x0, y0]]
                    mask: RLE Encoded binary mask, (order right -> down)
                    z_index: Z index of the label.
        """
        return Label._batch_create(self._requester, self._project_id, self._id, labels)

    def edit_labels(self, labels):
        """
        Updates multiple labels. Returns a list of `~hasty.Label` objects

        Args:
            labels (list of dict): List of labels, keys:
                    label_id: Label id
                    class_id: Label class ID of the label
                    bbox: Coordinates of bounding box [x_min, y_min, x_max, y_max]
                    polygon: List of x, y pairs [[x0, y0], [x1, y1], .... [x0, y0]]
                    mask: RLE Encoded binary mask, (order right -> down)
                    z_index: Z index of the label.
        """
        return Label._batch_update(self._requester, self._project_id, self._id, labels)

    def delete_labels(self, label_ids: List[str]):
        """
        Removes multiple labels

        Args:
            label_ids (list of str): Returns list of ids
        """
        Label._batch_delete(self._requester, self._project_id, self._id, label_ids)

    def set_status(self, status: str):
        """
        Set image status

        Args:
            status: New status one of ["NEW", "DONE", "SKIPPED", "IN PROGRESS", "TO REVIEW"]
        """
        if status not in VALID_STATUSES:
            raise ValidationException(f"Got {status}, expected on of {VALID_STATUSES}")
        self._requester.put(Image.endpoint_image.format(project_id=self.project_id,
                                                        image_id=self.id)+"/status",
                            json_data={"status": status})

    def download(self, filepath: str):
        """
        Downloads image to file

        Args:
            filepath (str): Local path
        """
        urllib.request.urlretrieve(self._public_url, filepath)

    def get_tags(self):
        """
        Returns image tags (list of `~hasty.Tag` objects)
        """
        return PaginatedList(Tag, self._requester,
                             Tag.endpoint.format(project_id=self.project_id, image_id=self.id),
                             obj_params={"project_id": self.project_id, "image_id": self.id})

    def add_tags(self, tags: List[Union[Dict, TagClass]]):
        """
        Create multiple tags. Returns a list of `~hasty.Tag` objects

        Args:
            tags (list of dict/`~hasty.TagClass`): List of tags, keys:
                    tag_class_id: Tag class ID
        """
        return Tag._batch_create(self._requester, self._project_id, self._id, tags)

    def delete_tags(self, tags: List[Union[Dict, Tag, TagClass]]):
        """
        Removes multiple tags

        Args:
            tags (list of dict/`~hasty.Tag`/`~hasty.TagClass`): List of tags, keys:
                    tag_id: Tag ID of the label (optional if tag_class_id is specified)
                    tag_class_id: Tag class ID of the label (optional if id is specified)
        """
        Tag._batch_delete(self._requester, self._project_id, self._id, tags)
