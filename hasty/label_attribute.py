from __future__ import absolute_import, division, print_function

from . import api_requestor


class LabelAttribute:
    """Class that contains some basic requests and features for label attributes."""
    endpoint = '/v1/projects/{project_id}/labels/{label_id}/attributes'
    set_endpoint = '/v1/projects/{project_id}/labels/{label_id}/attributes/{attribute_id}'

    @staticmethod
    def fetch_all_label(API_class, project_id, label_id):
        """ fetches every label attributes from the given label

        Parameters
        ----------
        API_class : class
            hasty.API class
        project_id : str
            id of the project
        label_id : str
            id of the label

        Returns
        -------
        dict
            label attributes objects

        """
        return api_requestor.get(API_class,
                                 LabelAttribute.endpoint.format(project_id=project_id,
                                                                label_id=label_id))

    @staticmethod
    def fetch_all(API_class, project_id, label_ids):
        """ fetches every label attrtibutes of the given label list

        Parameters
        ----------
        API_class : class
            hasty.API class
        project_id : str
            id of the project
        label_ids : iterable
            iterable of label ids

        Returns
        -------
        list [dict]
            label attributes list
        """
        lab_attributes = {}
        for label_id in label_ids:
            lab_attributes[label_id] = LabelAttribute.fetch_all_label(
                API_class, project_id, label_id)['items']
        return lab_attributes

    @staticmethod
    def set(API_class, project_id, label_id, attribute_id, value):
        """ sets a label attribute's value

        Parameters
        ----------
        API_class : class
            hasty.API class
        project_id : str
            id of the project
        label_id : str
            id of the label
        attribute_id : str
            id of the attribute
        value :
            value to set label attribute to

        Returns
        -------
        dict
            label attribute object

        """
        json_data = {
            'value': value
        }
        return api_requestor.post(API_class,
                                  LabelAttribute.set_endpoint.format(project_id=project_id,
                                                                     label_id=label_id,
                                                                     attribute_id=attribute_id),
                                  json_data=json_data)

    @staticmethod
    def copy(API_class, project_id, label_id, item_to_copy, attribute_class_mapping):
        """ copies a label attribute object to the given label

        Parameters
        ----------
        API_class : class
            hasty.API class
        project_id : str
            id of the project
        item_to_copy : dict
            label attribute object to copy
        label_id : str
            id of the label
        attribute_class_mapping : dict
            attribute class ids mapping from src to dst

        Returns
        -------
        dict
            attribute object

        """
        json_data = {
            'value': item_to_copy['value']
        }
        attribute_id = attribute_class_mapping[item_to_copy['id']]
        return api_requestor.post(API_class,
                                  LabelAttribute.set_endpoint.format(project_id=project_id,
                                                                     label_id=label_id,
                                                                     attribute_id=attribute_id),
                                  json_data=json_data)
