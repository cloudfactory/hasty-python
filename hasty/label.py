from collections import OrderedDict

from .hasty_object import HastyObject
from .helper import PaginatedList


class Label(HastyObject):
    endpoint_image = '/v1/projects/{project_id}/images/{image_id}/labels'
    endpoint_project = '/v1/projects/{project_id}/labels'

    def __repr__(self):
        return self.get__repr__(OrderedDict({"id": self._id}))

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

    def _init_properties(self):
        self._id = None
        self._project_id = None
        self._image_id = None
        self._class_id = None
        self._bbox = None
        self._polygon = None
        self._mask = None
        self._z_index = None

    def _set_prop_values(self, data):
        if "id" in data:
            self._id = data["id"]

    @staticmethod
    def create(requester, project_id, image_id, class_id, bbox=None, polygon=None, mask=None, z_index=None):
        # TODO add validation
        res = requester.post(Label.endpoint_image.format(project_id=project_id, image_id=image_id),
                             json_data={"class_id": class_id,
                                        "bbox": bbox,
                                        "polygon": polygon,
                                        "mask": mask,
                                        "z_index": z_index})
        return Label(requester, res, {"project_id": project_id, "image_id": image_id})

    @staticmethod
    def batch_create(requester, project_id, image_id, labels):
        data = []
        for label in labels:
            data.append({"class_id": label["class_id"],
                         "bbox": label.get("bbox"),
                         "polygon": label.get("polygon"),
                         "mask": label.get("mask"),
                         "z_index": label.get("z_index")})
        res = requester.post(Label.endpoint_image.format(project_id=project_id, image_id=image_id), json_data=data)
        return res["items"]
