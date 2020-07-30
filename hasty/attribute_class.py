from __future__ import absolute_import, division, print_function

from . import api_requestor


class AttributeClass:
    endpoint = '/v1/projects/{project_id}/attributes'
    endpoint_class = '/v1/projects/{project_id}/attributes/{attribute_id}/label_classes'

    @staticmethod
    def list_attribute(API_class, project_id, offset=0, limit=100):
        json_data = {
            'offset': offset,
            'limit': limit
        }
        return api_requestor.get(API_class,
                                 AttributeClass.endpoint.format(project_id=project_id),
                                 json_data=json_data)

    @staticmethod
    def list_attribute_class(API_class, project_id, attribute_id, offset=0, limit=100):
        json_data = {
            'offset': offset,
            'limit': limit
        }
        return api_requestor.get(API_class,
                                 AttributeClass.endpoint_class.format(project_id=project_id,
                                                                      attribute_id=attribute_id),
                                 json_data=json_data)

    @staticmethod
    def fetch_all_attribute(API_class, project_id):
        tot = []
        n = AttributeClass.get_total_items_attribute(API_class, project_id)
        for offset in range(0, n+1, 100):
            tot += AttributeClass.list_attribute(API_class, project_id, offset=offset)['items']
        return tot

    @staticmethod
    def fetch_all_attribute_class(API_class, project_id, attribute_id):
        tot = []
        n = AttributeClass.get_total_items_attribute_class(API_class, project_id, attribute_id)
        for offset in range(0, n+1, 100):
            tot += AttributeClass.list_attribute_class(API_class, project_id, attribute_id, offset=offset)['items']
        return tot

    @staticmethod
    def create_attribute(API_class, project_id, attribute_name, attribute_type,
                         description=None, default=None, min=None, max=None):
        json_data = {
            'name': attribute_name,
            'type': attribute_type,
            'description': description,
            'default': default,
            'min': min,
            'max': max
        }
        return api_requestor.post(API_class,
                                  AttributeClass.endpoint.format(project_id=project_id),
                                  json_data=json_data)

    @staticmethod
    def set_attribute_class(API_class, project_id, attribute_id, class_ids_list):
        json_data = [{'class_id': i} for i in class_ids_list]
        return api_requestor.post(API_class,
                                  AttributeClass.endpoint_class.format(project_id=project_id,
                                                                       attribute_id=attribute_id),
                                  json_data=json_data)

    @staticmethod
    def copy_attribute(API_class, project_id, item_to_copy):
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
                                  AttributeClass.endpoint.format(project_id=project_id),
                                  json_data=json_data)

    @staticmethod
    def copy_attribute_class(API_class, project_id, attribute_id, items_to_copy, label_class_mapping):
        # should work when added to public API
        json_data = [{
            'class_id': label_class_mapping[i['class_id']]
        } for i in items_to_copy]
        return api_requestor.post(API_class,
                                  AttributeClass.endpoint_class.format(project_id=project_id,
                                                                       attribute_id=attribute_id),
                                  json_data=json_data)

    @staticmethod
    def get_total_items_attribute(API_class, project_id):
        return AttributeClass.list_attribute(API_class, project_id, limit=0)['meta']['total']

    @staticmethod
    def get_total_items_attribute_class(API_class, project_id, attribute_id):
        return AttributeClass.list_attribute_class(API_class, project_id, attribute_id, limit=0)['meta']['total']
