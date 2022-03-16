from collections import OrderedDict

from .hasty_object import HastyObject


class TagClass(HastyObject):
    endpoint = '/v1/projects/{project_id}/tag_classes'
    endpoint_class = '/v1/projects/{project_id}/tag_classes/{tag_class_id}'

    def __repr__(self):
        return self.get__repr__(OrderedDict({"id": self._id, "name": self._name, "norder": self._norder}))

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
    def _create(requester, project_id, name, norder=None):
        res = requester.post(TagClass.endpoint.format(project_id=project_id),
                             json_data={"name": name,
                                        "norder": norder})
        return TagClass(requester, res, {"project_id": project_id})

    def edit(self, name, norder=None):
        """
        Edit tag class properties

        Arguments:
            name (str): Taп class name
            norder (float, optional): Order in the Hasty tool
        """
        self._requester.put(TagClass.endpoint_class.format(project_id=self.project_id, tag_class_id=self.id),
                            json_data={"name": name,
                                       "norder": norder})
        self._name = name
        self._norder = norder

    def delete(self):
        """
        Deletes tag class
        """
        self._requester.delete(TagClass.endpoint_class.format(project_id=self.project_id, tag_class_id=self.id))
