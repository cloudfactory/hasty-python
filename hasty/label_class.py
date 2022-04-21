from collections import OrderedDict

from .hasty_object import HastyObject


class LabelClass(HastyObject):
    endpoint = '/v1/projects/{project_id}/label_classes'
    endpoint_class = '/v1/projects/{project_id}/label_classes/{label_class_id}'

    def __repr__(self):
        return self.get__repr__(OrderedDict({"id": self._id, "name": self._name, "color": self._color,
                                             "type": self._class_type, "norder": self._norder}))

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
    def color(self):
        """
        :type: string
        """
        return self._color

    @property
    def class_type(self):
        """
        :type: string
        """
        return self._class_type

    @property
    def norder(self):
        """
        :type: float
        """
        return self._norder

    @property
    def external_id(self):
        """
        :type: string
        """
        return self._external_id

    def _init_properties(self):
        self._id = None
        self._name = None
        self._project_id = None
        self._color = None
        self._class_type = None
        self._norder = None
        self._external_id = None

    def _set_prop_values(self, data):
        if "id" in data:
            self._id = data["id"]
        if "name" in data:
            self._name = data["name"]
        if "project_id" in data:
            self._project_id = data["project_id"]
        if "color" in data:
            self._color = data["color"]
        if "type" in data:
            self._class_type = data["type"]
        if "norder" in data:
            self._norder = data["norder"]
        if "external_id" in data:
            self._external_id = data["external_id"]

    @staticmethod
    def _create(requester, project_id, name, color=None, class_type="object", norder=None, external_id=None):
        res = requester.post(LabelClass.endpoint.format(project_id=project_id),
                             json_data={"name": name,
                                        "color": color,
                                        "type": class_type,
                                        "norder": norder,
                                        "external_id": external_id})
        return LabelClass(requester, res, {"project_id": project_id})

    def edit(self, name, color=None, class_type="object", norder=None, external_id=None):
        """
        Edit label class properties

        Arguments:
            name (str): Label class name
            color (str, optional): Color in HEX format #0f0f0faa
            class_type (str, optional): Class type [object or background] (default object)
            norder (float, optional): Order in the Hasty tool
            external_id (str, optional): External identifier
        """
        self._requester.put(LabelClass.endpoint_class.format(project_id=self.project_id, label_class_id=self.id),
                            json_data={"name": name,
                                       "color": color,
                                       "type": class_type,
                                       "norder": norder,
                                       "external_id": external_id})
        self._name = name
        self._color = color
        self._class_type = class_type
        self._norder = norder
        self._external_id = external_id

    def delete(self):
        """
        Deletes label class
        """
        self._requester.delete(LabelClass.endpoint_class.format(project_id=self.project_id, label_class_id=self.id))
