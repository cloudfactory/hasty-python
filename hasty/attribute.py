from __future__ import absolute_import, division, print_function

from . import api_requestor


class Attribute:
    """Class that contains some basic requests and features for attributes"""
    endpoint = '/v1/projects/{project_id}/attributes'
    endpoint_attribute = '/v1/projects/{project_id}/attributes/{attribute_id}'

    @staticmethod
    def fetch_all(API_class, project_id):
        """Retreives every attribute in a project

        Parameters
        ----------
        API_class : class
            hasty.API class
        project_id : str
            project id

        Returns
        -------
        list [dict]
            attribute objects
        """
        return api_requestor.get(API_class,
                                 Attribute.endpoint.format(
                                     project_id=project_id))['items']

    @staticmethod
    def create(API_class, project_id, attribute_name, attribute_type,
               description=None, default=None, min=None, max=None, values=[]):
        """Create an attribute

        Parameters
        ----------
        API_class : class
            hasty.API class
        project_id : str
            project id
        attribute_name : str
            attribute name
        attribute_type : str
            attribute type
        description : str
            description (Default value = None)
        default :
            default attribute value (Default value = None)
        min :
            min value (Default value = None)
        max :
            max value (Default value = None)
        values :
            list of values (Default value = [])

        Returns
        -------
        dict
            attribute object

        """
        json_data = {
            'name': attribute_name,
            'type': attribute_type,
            'description': description,
            'default': default,
            'min': min,
            'max': max,
            'values': values
        }
        return api_requestor.post(API_class,
                                  Attribute.endpoint.format(
                                      project_id=project_id),
                                  json_data=json_data)

    @staticmethod
    def copy(API_class, project_id, item_to_copy):
        """Create an attribute from an existing one

        Parameters
        ----------
        API_class : class
            hasty.API class
        project_id : str
            project id
        item_to_copy : dict
            attribute object to copy

        Returns
        -------
        dict
            attribute object

        """
        json_data = {
            'name': item_to_copy['name'],
            'type': item_to_copy['type'],
            'description': item_to_copy['description'],
            'default': item_to_copy['default'],
            'norder': item_to_copy['norder'],
            'min': item_to_copy['min'],
            'max': item_to_copy['max']
        }
        return api_requestor.post(API_class,
                                  Attribute.endpoint.format(
                                      project_id=project_id),
                                  json_data=json_data)

    @staticmethod
    def edit_attribute(API_class, project_id, attribute_id, name, type, description=None, min=None, max=None):
        """Edits an existing attribute

        Parameters
        ----------
        API_class : class
            hasty.API class
        project_id : str
            project id
        attribute_id : str
            attribute id
        name : str
            new attribute name
        type : str
            new attribute type
        description :
            new description (Default value = None)
        min :
            new min value (Default value = None)
        max :
            new max value (Default value = None)

        Returns
        -------
        dict
            attribute object

        """
        json_data = {
            'name': name,
            'description': description,
            'type': type,
            'min': min,
            'max': max,
        }
        return api_requestor.edit(API_class,
                                  Attribute.endpoint_attribute.format(project_id=project_id,
                                                                      attribute_id=attribute_id),
                                  json_data=json_data)

    @staticmethod
    def delete_attribute(API_class, project_id, attribute_id):
        """

        Parameters
        ----------
        API_class : class
            hasty.API class
        project_id : str
            project id
        attribute_id : str
            attribute id

        Returns
        -------
        json
            empty

        """
        return api_requestor.delete(API_class,
                                    Attribute.endpoint_attribute.format(project_id=project_id,
                                                                        attribute_id=attribute_id))
