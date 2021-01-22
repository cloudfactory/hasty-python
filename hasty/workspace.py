from collections import OrderedDict

from .hasty_object import HastyObject


class Workspace(HastyObject):
    """Class that contains some basic requests and features for workspaces."""
    endpoint = '/v1/workspaces'
    endpoint_workspace = '/v1/workspaces/{workspace_id}'

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
