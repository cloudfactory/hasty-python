from __future__ import absolute_import, division, print_function

from .. import api_requestor



class LabelClassAttribute:
    endpoint = '/v1/projects/{project_id}/attributes'

    @staticmethod
    def list(API_class, project_id, offset=0, limit=100):
        json_data = {
            'offset': offset,
            'limit': limit
        }
        return api_requestor.get(API_class, LabelClassAttribute.endpoint.format(project_id=project_id), json_data=json_data)

    @staticmethod
    def fetch_all(API_class, project_id):
        tot = []
        n = LabelClassAttribute.get_total_items(API_class, project_id)
        for offset in range(0, n+1, 100):
            tot += LabelClassAttribute.list(API_class, project_id, offset=offset)['items']
        return tot

    @staticmethod
    def create(API_class, project_id, attribute_name, attribute_type, description=None, default=None, min=None, max=None):
        return api_requestor.post(API_class, LabelClassAttribute.endpoint.format(project_id=project_id),
            json_data= {
                'name': attribute_name,
                'type': attribute_type,
                'description': description,
                'default': default,
                'min': min,
                'max': max
                })

    @staticmethod
    def copy(API_class, project_id, item_to_copy):
        json_data= {
            'name': item_to_copy['name'],
            'type': item_to_copy['type'],
            'description': item_to_copy['description'],
            'default': item_to_copy['default'],
            'norder': item_to_copy['norder'],
            'min': item_to_copy['min'],
            'max': item_to_copy['max']
        }
        return api_requestor.post(API_class, LabelClassAttribute.endpoint.format(project_id=project_id), json_data=json_data)

    @staticmethod
    def get_total_items(API_class, project_id):
        return LabelClassAttribute.list(API_class, project_id, limit=0)['meta']['total']
