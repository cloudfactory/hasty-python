from __future__ import absolute_import, division, print_function

from . import api_requestor


class LabelAttribute:
    endpoint = '/v1/projects/{project_id}/labels/{label_id}/attributes'
    set_endpoint = '/v1/projects/{project_id}/labels/{label_id}/attributes/{attribute_id}'

    @staticmethod
    def list(API_class, project_id, label_id, offset=0, limit=100):
        json_data = {
            'offset': offset,
            'limit': limit
        }
        return api_requestor.get(API_class, LabelAttribute.endpoint.format(project_id=project_id, label_id=label_id), json_data=json_data)

    @staticmethod
    def fetch_all(API_class, project_id, label_ids):
        lab_attributes = {}
        for label_id in label_ids:
            attributes = []
            n_attribute = LabelAttribute.get_total_items(API_class, project_id, label_id)
            for offset in range(0, n_attribute+1, 100):
                attributes += LabelAttribute.list(API_class, project_id, label_id, offset=offset)['items']
            lab_attributes[label_id] = attributes
        return lab_attributes

    @staticmethod
    def set(API_class, project_id, label_id, attribute_id, value):
        json_data = {
            'value': value
        }
        return api_requestor.post(API_class, LabelAttribute.set_endpoint.format(project_id=project_id, label_id=label_id, attribute_id=attribute_id), json_data=json_data)

    @staticmethod
    def copy(API_class, project_id, label_id, attribute_class_mapping, item_to_copy):
        json_data = {
            'value': item_to_copy['value']
        }
        attribute_id = attribute_class_mapping[item_to_copy['id']]
        return api_requestor.post(API_class, LabelAttribute.set_endpoint.format(project_id=project_id, label_id=label_id, attribute_id=attribute_id), json_data=json_data)

    @staticmethod
    def get_total_items(API_class, project_id, label_id):
        return LabelAttribute.list(API_class, project_id, label_id, limit=0)['meta']['total']
