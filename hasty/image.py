from collections import OrderedDict
import os

from .hasty_object import HastyObject
from .helper import PaginatedList
from .label import Label


class Image(HastyObject):
    endpoint = '/v1/projects/{project_id}/images'
    endpoint_uploads = '/v1/projects/{project_id}/image_uploads'
    endpoint_image = '/v1/projects/{project_id}/images/{image_id}'

    def __repr__(self):
        return self.get__repr__(OrderedDict({"id": self._id, "dataset_name": self._dataset_name, "name": self._name}))

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

    def _init_properties(self):
        self._id = None
        self._name = None
        self._project_id = None
        self._dataset_name = None

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

    @staticmethod
    def get_by_id(requester, project_id, image_id):
        data = requester.get(Image.endpoint_image.format(project_id=project_id, image_id=image_id))
        return Image(requester, data, {"project_id": project_id})

    @staticmethod
    def _generate_sign_url(requester, project_id):
        data = requester.post(Image.endpoint_uploads.format(project_id=project_id), json_data={"count": 1})
        return data["items"][0]

    @staticmethod
    def upload_from_file(requester, project_id, dataset_id, filepath):
        filename = os.path.basename(filepath)
        url_data = Image._generate_sign_url(requester, project_id)
        requester.put(url_data['url'], data=open(filepath, 'rb').read(), content_type="image/*")
        res = requester.post(Image.endpoint.format(project_id=project_id),
                             json_data={"dataset_id": dataset_id,
                                        "filename": filename,
                                        "upload_id": url_data["id"]})
        return Image(requester, res, {"project_id": project_id,
                                      "dataset_id": dataset_id})

    def create_label(self, class_id, bbox=None, polygon=None, mask=None, z_index=None):
        label = Label.create(self._requester, self._project_id, self._id, class_id, bbox, polygon, mask, z_index)
        return label

    def create_labels(self, labels):
        return Label.batch_create(self._requester, self._project_id, self._id, labels)
