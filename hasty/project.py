from collections import OrderedDict

from .dataset import Dataset
from .hasty_object import HastyObject
from .helper import PaginatedList
from .image import Image
from .label_class import LabelClass


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

    @property
    def description(self):
        """
        :type: string
        """
        return self._description

    @property
    def workspace_id(self):
        """
        :type: string
        """
        return self._workspace_id

    def _init_properties(self):
        self._id = None
        self._name = None
        self._workspace_id = None
        self._description = None

    def _set_prop_values(self, data):
        if "id" in data:
            self._id = data["id"]
        if "name" in data:
            self._name = data["name"]
        if "workspace_id" in data:
            self._workspace_id = data["workspace_id"]
        if "description" in data:
            self._description = data["description"]

    @staticmethod
    def create(requester, workspace_id, name, description):
        res = requester.post(Project.endpoint,
                             json_data={"workspace_id": workspace_id,
                                        "name": name,
                                        "description": description})
        return Project(requester, res, {"workspace_id": workspace_id})

    def edit(self, name, description):
        """
        Edits projects properties
        Arguments:
            name (str): Name of the project
            description (str, optional): Project description
        """
        res = self._requester.put(Project.endpoint_project.format(project_id=self.id),
                                  json_data={"name": name,
                                             "description": description})
        self._name = res["name"]
        self._description = res["description"]

    def delete(self):
        """
        Removes project
        """
        self._requester.delete(Project.endpoint_project.format(project_id=self.id))

    def get_datasets(self):
        """
        Returns projects datasets :py:class:`~hasty.Dataset` objects.
        """
        return PaginatedList(Dataset, self._requester,
                             Dataset.endpoint.format(project_id=self._id),
                             {"project_id": self._id})

    def get_dataset(self, dataset_id: str):
        """
        Get dataset by id

        Arguments:
            dataset_id (str): Dataset id
        """
        res = self._requester.get(Dataset.endpoint_dataset.format(project_id=self.id, dataset_id=dataset_id))
        return Dataset(self._requester, res, {"project_id": self.id})

    def create_dataset(self, name: str, norder: float = 0):
        """
        Creates a new dataset

        Arguments:
            name (str): Name of the dataset
            norder (float, optional): Order in the list
        """
        return Dataset.create(self._requester, self._id, name, norder)

    def get_images(self):
        return PaginatedList(Image, self._requester,
                             Image.endpoint.format(project_id=self._id))

    def get_image(self, image_id):
        return Image.get_by_id(self._requester, self._id, image_id)

    def upload_from_file(self, dataset, filepath):
        dataset_id = dataset
        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        return Image.upload_from_file(self._requester, self._id, dataset_id, filepath)

    def get_label_classes(self):
        """
        Get label classes, list of :py:class:`~hasty.LabelClass` objects.
        """
        return PaginatedList(LabelClass, self._requester,
                             LabelClass.endpoint.format(project_id=self._id))

    def create_label_class(self, name: str, color: str = None, class_type: str = "object", norder: float = None):
        """
        Create label class, returns :py:class:`~hasty.LabelClass` object.format

        Args:
            name (str): Label class name
            color (str): Color in HEX format #0f0f0faa
            class_type (str): Class type (object or background)
            norder (float): Order in the Hasty tool
        """
        return LabelClass.create(self._requester, self._id, name, color, class_type, norder)
