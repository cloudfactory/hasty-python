from collections import OrderedDict
from uuid import UUID
import numbers

from .attribute import Attribute
from .hasty_object import HastyObject
from .helper import PaginatedList
from .exception import LimitExceededException, ValidationException
from .label_attribute import LabelAttribute
from .label_class import LabelClass
from .label_utils import check_bbox_format, check_rle_mask


C_LABELS_LIMIT = 100
C_LABELS_TOOL_USED = "api"


class Label(HastyObject):
    endpoint_image = '/v1/projects/{project_id}/images/{image_id}/labels'
    endpoint_project = '/v1/projects/{project_id}/labels'

    def __repr__(self):
        return self.get__repr__(OrderedDict({"id": self._id, "bbox": self._bbox, "polygon": self._polygon}))

    def __iter__(self):
        yield 'id', self._id
        yield 'project_id', self._project_id
        yield 'image_id', self._image_id
        yield 'class_id', self._class_id
        yield 'bbox', self._bbox
        yield 'polygon', self._polygon
        yield 'mask', self._mask
        yield 'z_index', self._z_index

    @property
    def id(self):
        """
        :type: string
        """
        return self._id

    @property
    def project_id(self):
        """
        :type: string
        """
        return self._project_id

    @property
    def image_id(self):
        """
        :type: string
        """
        return self._image_id

    @property
    def class_id(self):
        """
        :type: string
        """
        return self._class_id

    @property
    def bbox(self):
        """
        :type: string
        """
        return self._bbox

    @property
    def polygon(self):
        """
        :type: string
        """
        return self._polygon

    @property
    def mask(self):
        """
        :type: string
        """
        return self._mask

    @property
    def z_index(self):
        """
        :type: string
        """
        return self._z_index

    @property
    def external_id(self):
        """
        :type: string
        """
        return self._external_id

    def _init_properties(self):
        self._id = None
        self._project_id = None
        self._image_id = None
        self._class_id = None
        self._bbox = None
        self._polygon = None
        self._mask = None
        self._z_index = None
        self._external_id = None

    def _set_prop_values(self, data):
        if "id" in data:
            self._id = data["id"]
        if "project_id" in data:
            self._project_id = data["project_id"]
        if "image_id" in data:
            self._image_id = data["image_id"]
        if "class_id" in data:
            self._class_id = data["class_id"]
        if "bbox" in data:
            self._bbox = data["bbox"]
        if "polygon" in data:
            self._polygon = data["polygon"]
        if "mask" in data:
            self._mask = data["mask"]
        if "z_index" in data:
            self._z_index = data["z_index"]
        if "external_id" in data:
            self._external_id = data["external_id"]

    @staticmethod
    def _validate_label(class_id, bbox=None, polygon=None, mask=None, z_index=None):
        try:
            class_id = UUID(class_id)
        except Exception:
            raise ValidationException(f"Invalid UUID - {class_id}")
        # Check bbox
        if bbox is not None:
            if not check_bbox_format(bbox):
                raise ValidationException(f"Invalid bbox format - {bbox}")
        # Check polygon
        if polygon is not None:
            if not isinstance(polygon, list):
                raise ValidationException(f"Polygon must be a list of [x, y] pairs - {polygon}")
            for v in polygon:
                if not isinstance(v, list) and not isinstance(v, tuple):
                    raise ValidationException(f"Polygon vertex must be a list of [x, y] - {polygon}")
                if len(v) != 2:
                    raise ValidationException(f"Polygon vertex must be a list of [x, y] - {polygon}")
        else:
            if bbox is None:
                raise ValidationException("Polygon or bounding box must be provided")
        # Check mask
        if mask is not None:
            if not check_rle_mask(bbox, mask):
                raise ValidationException(f"Invalid mask - ({bbox}, {mask})")

        if z_index:
            if not isinstance(z_index, numbers.Number):
                raise ValidationException(f"Z Index must be None or numeric, got - {z_index}")

    @staticmethod
    def _create(requester, project_id, image_id, class_id, bbox=None, polygon=None, mask=None, z_index=None,
                external_id=None):
        new_labels = Label._batch_create(requester, project_id, image_id,
                                         [{"class_id": class_id,
                                           "bbox": bbox,
                                           "polygon": polygon,
                                           "mask": mask,
                                           "z_index": z_index,
                                           "external_id": external_id}])
        return new_labels[0]

    @staticmethod
    def _batch_create(requester, project_id, image_id, labels):
        if len(labels) == 0:
            return []
        data = []
        if len(labels) > C_LABELS_LIMIT:
            raise LimitExceededException.max_labels_per_batch(len(labels))
        for label in labels:
            Label._validate_label(label["class_id"], label.get("bbox"), label.get("polygon"),
                                  label.get("mask"), label.get("z_index"))
            data.append({"class_id": label["class_id"],
                         "bbox": label.get("bbox"),
                         "polygon": label.get("polygon"),
                         "mask": label.get("mask"),
                         "z_index": label.get("z_index"),
                         "external_id": label.get("external_id"),
                         "tool_used": C_LABELS_TOOL_USED})
        res = requester.post(Label.endpoint_image.format(project_id=project_id, image_id=image_id), json_data=data)
        new_labels = []
        for label in res["items"]:
            new_labels.append(Label(requester, label, {"project_id": project_id, "image_id": image_id}))
        return new_labels

    @staticmethod
    def _batch_update(requester, project_id, image_id, labels):
        data = []
        if len(labels) > 100:
            raise LimitExceededException.max_labels_per_batch(len(labels))
        for label in labels:
            Label._validate_label(label["class_id"], label.get("bbox"), label.get("polygon"),
                                  label.get("mask"), label.get("z_index"))
            data.append({"label_id": label["label_id"],
                         "class_id": label["class_id"],
                         "bbox": label.get("bbox"),
                         "polygon": label.get("polygon"),
                         "mask": label.get("mask"),
                         "z_index": label.get("z_index"),
                         "external_id": label.get("external_id"),
                         "tool_used": C_LABELS_TOOL_USED})
        res = requester.put(Label.endpoint_image.format(project_id=project_id, image_id=image_id), json_data=data)
        updated_labels = []
        for label in res["items"]:
            updated_labels.append(Label(requester, label, {"project_id": project_id, "image_id": image_id}))
        return updated_labels

    @staticmethod
    def _batch_delete(requester, project_id, image_id, label_ids):
        data = []
        for label_id in label_ids:
            data.append({"id": label_id})
        requester.delete(Label.endpoint_image.format(project_id=project_id, image_id=image_id), json_data=data)

    def edit(self, label_class, bbox=None, polygon=None, mask=None, z_index=None, external_id=None):
        """
        Update label properties

        Args:
            label_class (LabelClass, str): Label class or label class ID of the label
            bbox (list of int): Coordinates of bounding box [x_min, y_min, x_max, y_max]
            polygon (list): List of x, y pairs [[x0, y0], [x1, y1], .... [x0, y0]]
            mask (list of int): RLE Encoded binary mask, (order right -> down)
            z_index (float): Z index of the label. A label with greater value is in front of a label with a lower one.
            external_id (str, optional): External Identifier
        """
        class_id = label_class
        if isinstance(label_class, LabelClass):
            class_id = label_class.id
        updated_labels = Label._batch_update(self._requester, self.project_id, self.image_id,
                                             [{"label_id": self.id,
                                               "class_id": class_id,
                                               "bbox": bbox,
                                               "polygon": polygon,
                                               "mask": mask,
                                               "z_index": z_index,
                                               "external_id": external_id,
                                               "tool_used": C_LABELS_TOOL_USED}])
        updated_label = updated_labels[0]
        self._class_id = updated_label.class_id
        self._bbox = updated_label.bbox
        self._polygon = updated_label.polygon
        self._mask = updated_label.mask
        self._z_index = updated_label.z_index
        self._external_id = updated_label.external_id

    def delete(self):
        """
        Delete label
        """
        Label._batch_delete(self._requester, self.project_id, self.image_id, [self.id])

    def get_attributes(self):
        """
        Get attributes values, list of :py:class:`~hasty.LabelAttribute` objects.
        """
        return PaginatedList(LabelAttribute, self._requester,
                             LabelAttribute.endpoint.format(project_id=self.project_id, label_id=self.id))

    def set_attribute(self, attribute, value):
        """
        Set label attribute

        Args:
            attribute (`~hasty.Attribute`, str) - `~hasty.Attribute` object or attribute id
            value (str, float, int, bool, list of str) - Attribute value
        """
        attribute_id = attribute
        if isinstance(attribute, Attribute):
            attribute_id = attribute.id
        LabelAttribute._set_label_attribute(self._requester, self.project_id, self.id, attribute_id, value)
