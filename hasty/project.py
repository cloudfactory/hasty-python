from collections import OrderedDict

from .dataset import Dataset
from .hasty_object import HastyObject
from .helper import PaginatedList
from .image import Image


class Project(HastyObject):
    endpoint = '/v1/projects'
    endpoint_project = '/v1/projects/{project_id}'

    def __repr__(self):
        return self.get__repr__(OrderedDict({"id": self._id, "name": self._name}))

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

    def _init_properties(self):
        self._id = None
        self._name = None

    def _set_prop_values(self, data):
        if "id" in data:
            self._id = data["id"]
        if "name" in data:
            self._name = data["name"]

    def get_datasets(self):
        return PaginatedList(Dataset, self._requester,
                             Dataset.endpoint.format(project_id=self._id),
                             {"projec_id": self._id})

    def get_images(self):
        return PaginatedList(Image, self._requester,
                             Image.endpoint.format(project_id=self._id))

    def upload_from_file(self, dataset, filepath):
        dataset_id = dataset
        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        return Image.upload_from_file(self._requester, self._id, dataset_id, filepath)

    def create_dataset(self, name):
        return Dataset.create(self._requester, self._id, name)
