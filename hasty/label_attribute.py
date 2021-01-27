from collections import OrderedDict
from .hasty_object import HastyObject


class LabelAttribute(HastyObject):
    endpoint = '/v1/projects/{project_id}/labels/{label_id}/attributes'
    set_endpoint = '/v1/projects/{project_id}/labels/{label_id}/attributes/{attribute_id}'

    def __repr__(self):
        return self.get__repr__(OrderedDict({"id": self._id, "label_id": self._label_id,
                                             "attribute_id": self._attribute_id,
                                             "value": self._value}))

    @property
    def id(self):
        """
        :type: string
        """
        return self._id

    @property
    def label_id(self):
        """
        :type: string
        """
        return self._label_id

    @property
    def project_id(self):
        """
        :type: string
        """
        return self._project_id

    @property
    def attribute_id(self):
        """
        :type: string
        """
        return self._attribute_id

    @property
    def value(self):
        """
        :type: str, int, float, bool, List
        """
        return self._value

    def _init_properties(self):
        self._id = None
        self._label_id = None
        self._project_id = None
        self._attribute_id = None
        self._value = None

    def _set_prop_values(self, data):
        if "id" in data:
            self._id = data["id"]
        if "label_id" in data:
            self._name = data["label_id"]
        if "project_id" in data:
            self._project_id = data["project_id"]
        if "attribute_id" in data:
            self._attribute_id = data["attribute_id"]
        if "value" in data:
            self._value = data["value"]

    @staticmethod
    def _set_label_attribute(requester, project_id, label_id, attribute_id, value):
        res = requester.post(LabelAttribute.set_endpoint.format(project_id=project_id, label_id=label_id,
                                                                attribute_id=attribute_id),
                             json_data={"value": value})
        return LabelAttribute(requester, res, {"project_id": project_id, "label_id": label_id,
                                               "attribute_id": attribute_id})
