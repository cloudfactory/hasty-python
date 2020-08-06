from __future__ import absolute_import, division, print_function

from . import api_requestor


class Attribute:
    '''
    This is a class that contains some basic requests and features for attributes
    '''
    endpoint = '/v1/projects/{project_id}/attributes'
    endpoint_attribute = '/v1/projects/{project_id}/attributes/{attribute_id}'

    @staticmethod
    def fetch_all(API_class, project_id):
        '''
        Function to retreive every attribute in a project

        Parameters:
            API_class (hasty.api.API): API object
            project_id (string): id of the project you want to fetch

        Returns:
            a list of attributes
        '''
        return api_requestor.get(API_class,
                                 Attribute.endpoint.format(
                                     project_id=project_id))

    @staticmethod
    def create(API_class, project_id, attribute_name, attribute_type,
               description=None, default=None, min=None, max=None):
        '''
        Function to create an attribute
        '''
        json_data = {
            'name': attribute_name,
            'type': attribute_type,
            'description': description,
            'default': default,
            'min': min,
            'max': max
        }
        return api_requestor.post(API_class,
                                  Attribute.endpoint.format(
                                      project_id=project_id),
                                  json_data=json_data)

    @staticmethod
    def copy(API_class, project_id, item_to_copy):
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
        return api_requestor.delete(API_class,
                                    Attribute.endpoint_attribute.format(project_id=project_id,
                                                                        attribute_id=attribute_id))
