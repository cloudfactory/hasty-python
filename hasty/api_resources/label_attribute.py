from __future__ import absolute_import, division, print_function

from .. import api_requestor

label_attribute_endpoint = '/v1/projects/{project_id}/labels/{label_id}/attributes'
set_label_attribute_endpoint = '/v1/projects/{project_id}/labels/{label_id}/attributes/{attribute_id}'

class LabelAttribute:

    @staticmethod
    def list(API_class, project_id, label_id, offset=0, limit=100):
        json_data = {
            'offset': offset,
            'limit': limit
        }
        return api_requestor.get(API_class, label_attribute_endpoint.format(project_id=project_id, label_id=label_id), json_data=json_data)

    @staticmethod
    def fetch_all(API_class, project_id, label_id):
        tot = []
        n = LabelAttribute.get_total_items(API_class, project_id, label_id)
        for offset in range(0, n+1, 100):
            tot += LabelAttribute.list(API_class, project_id, label_id, offset=offset)
        return tot

    @staticmethod
    def set(API_class, project_id, label_id, attribute_id, value):
        json_data = {
            'value': value
        }
        return api_requestor.post(API_class, set_label_attribute_endpoint.format(project_id=project_id, label_id=label_id, attribute_id=attribute_id), json_data=json_data)

    @staticmethod
    def get_total_items(API_class, project_id, label_id):
        return LabelAttribute.list(API_class, project_id, label_id, limit=0)['meta']['total']
