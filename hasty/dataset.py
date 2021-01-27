from collections import OrderedDict

from .hasty_object import HastyObject
from .requester import Requester


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

    @property
    def norder(self):
        """
        :type: float
        """
        return self._norder

    def _init_properties(self):
        self._id = None
        self._name = None
        self._project_id = None
        self._norder = None

    def _set_prop_values(self, data):
        if "id" in data:
            self._id = data["id"]
        if "name" in data:
            self._name = data["name"]
        if "project_id" in data:
            self._project_id = data["project_id"]
        if "norder" in data:
            self._norder = data["norder"]

    @staticmethod
    def _create(requester: Requester, project_id: str, name: str, norder: float = 0):
        res = requester.post(Dataset.endpoint.format(project_id=project_id),
                             json_data={"name": name,
                                        "norder": norder})
        return Dataset(requester, res, {"project_id": project_id})

    def edit(self, name: str, norder: float):
        """
        Edit dataset properties

        Arguments:
            name (str): Name of the dataset
            norder (float): Order in the list
        """
        res = self._requester.put(self.endpoint_dataset.format(project_id=self.project_id, dataset_id=self.id),
                                  json_data={"name": name,
                                             "norder": norder})
        self._name = res["name"]
        self._norder = res["norder"]

    def delete(self):
        """
        Removes dataset
        """
        self._requester.delete(Dataset.endpoint_dataset.format(project_id=self.project_id,
                                                               dataset_id=self.id))
