from collections import OrderedDict
from typing import List, Optional

from .exception import ValidationException
from .hasty_object import HastyObject


class Attribute(HastyObject):
    endpoint = '/v1/projects/{project_id}/attributes'
    endpoint_attribute = '/v1/projects/{project_id}/attributes/{attribute_id}'
    endpoint_attributes_classes = '/v1/projects/{project_id}/attributes_classes'

    def __repr__(self):
        return self.get__repr__(OrderedDict({"id": self._id, "name": self._name, "attribute_type": self._attribute_type,
                                             "description": self._description, "norder": self._norder,
                                             "values": self._values}))

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
    def attribute_type(self):
        """
        :type: string
        """
        return self._attribute_type

    @property
    def description(self):
        """
        :type: string
        """
        return self._description

    @property
    def norder(self):
        """
        :type: float
        """
        return self._norder

    @property
    def values(self):
        """
        :type: Dict
        """
        return self._values

    def _init_properties(self):
        self._id = None
        self._name = None
        self._project_id = None
        self._attribute_type = None
        self._description = None
        self._norder = None
        self._values = None

    def _set_prop_values(self, data):
        if "id" in data:
            self._id = data["id"]
        if "name" in data:
            self._name = data["name"]
        if "project_id" in data:
            self._project_id = data["project_id"]
        if "type" in data:
            self._attribute_type = data["type"]
        if "description" in data:
            self._description = data["description"]
        if "norder" in data:
            self._norder = data["norder"]
        if "values" in data:
            self._values = data["values"]

    @staticmethod
    def validate_type(attribute_type):
        if attribute_type not in ['SELECTION', 'MULTIPLE-SELECTION', 'TEXT', 'INT', 'FLOAT', 'BOOL']:
            raise ValidationException('Attribute type should be one of the following '
                                      '[SELECTION, MULTIPLE-SELECTION, TEXT, INT, FLOAT, BOOL]')

    @staticmethod
    def create(requester, project_id: str, name: str, attribute_type: str, description: Optional[str] = None,
               norder: Optional[float] = None, values: List[str] = None):
        Attribute.validate_type(attribute_type)
        json_data = {"name": name,
                     "type": attribute_type,
                     "description": description,
                     "values": [{"value": v} for v in values],
                     "norder": norder}

        res = requester.post(Attribute.endpoint.format(project_id=project_id), json_data=json_data)
        return Attribute(requester, res, {"project_id": project_id})

    def edit(self, name: str, attribute_type: str, description: Optional[str] = None,
             norder: Optional[float] = None, values: List[str] = None):
        """
        Edit attribute properties

        Arguments:
            Args:
            name (str): Attribute name
            attribute_type (str): Attribute type ['SELECTION', 'MULTIPLE-SELECTION', 'TEXT', 'INT', 'FLOAT', 'BOOL']
            description (str, optional): Attrbute description
            norder (float, optional): Order in the Hasty tool
            values (list of str): List of values for SELECTION and MULTIPLE-SELECTION attribute type
        """
        json_data = {"name": name,
                     "type": attribute_type,
                     "description": description,
                     "norder": norder,
                     "values": [{"value": v} for v in values]}

        res = self._requester.put(Attribute.endpoint_attribute.format(project_id=self.project_id, attribute_id=self.id),
                                  json_data=json_data)
        self._name = res["name"]
        self._attribute_type = res["type"]
        self._description = res["description"]
        self._norder = res["norder"]
        self._values = res["values"]

    def delete(self):
        """
        Deletes attribute
        """
        self._requester.delete(Attribute.endpoint_attribute.format(project_id=self.project_id, attribute_id=self.id))

    @staticmethod
    def get_attributes_classes(requester, project_id):
        res = requester.get(Attribute.endpoint_attributes_classes.format(project_id=project_id))
        return res

    @staticmethod
    def set_attributes_classes(requester, project_id, attributes_classes):
        json_data = []
        for attr_cls in attributes_classes:
            json_data.append({"attribute_id": attr_cls["attribute_id"],
                              "class_id": attr_cls["class_id"],
                              "attribute_order": attr_cls.get("attribute_order", 0),
                              "class_order": attr_cls.get("class_order", 0)})
        res = requester.post(Attribute.endpoint_attributes_classes.format(project_id=project_id),
                             json_data=json_data)
        return res

    @staticmethod
    def delete_attributes_classes(requester, project_id, attributes_classes):
        requester.delete(Attribute.endpoint_attributes_classes.format(project_id=project_id),
                         json_data=attributes_classes)
