from collections import OrderedDict

from .hasty_object import HastyObject
from .helper import PaginatedList


class Dataset(HastyObject):
    endpoint = '/v1/projects/{project_id}/datasets'
    endpoint_dataset = '/v1/projects/{project_id}/datasets/{dataset_id}'

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
    def project_id(self):
        """
        :type: string
        """
        return self._project_id

    def _init_properties(self):
        self._id = None
        self._name = None
        self._project_id = None

    def _set_prop_values(self, data):
        if "id" in data:
            self._id = data["id"]
        if "name" in data:
            self._name = data["name"]
        if "project_id" in data:
            self._project_id = data["project_id"]

    @staticmethod
    def create(requester, project_id, name):
        res = requester.post(Dataset.endpoint.format(project_id=project_id),
                             json_data={"name": name})
        return Dataset(requester, res, {"project_id": project_id})
