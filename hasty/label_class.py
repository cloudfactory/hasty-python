from __future__ import absolute_import, division, print_function

from . import api_requestor


class LabelClass:
    endpoint = '/v1/projects/{project_id}/label_classes'
    endpoint_class = '/v1/projects/{project_id}/label_classes/{label_class_id}'

    @staticmethod
    def list(API_class, project_id, offset=0, limit=100):
        json_data = {
            'offset': offset,
            'limit': limit
        }
        return api_requestor.get(API_class,
                                 LabelClass.endpoint.format(project_id=project_id),
                                 json_data=json_data)

    @staticmethod
    def fetch_all(API_class, project_id):
        tot = []
        n = LabelClass.get_total_items(API_class, project_id)
        for offset in range(0, n, 100):
            tot += LabelClass.list(API_class, project_id, offset=offset)['items']
        return tot

    @staticmethod
    def create(API_class, project_id, class_name, class_type, color='#49D3404D'):
        json_data = {
                'name': class_name,
                'type': class_type,
                'color': color
        }
        return api_requestor.post(API_class,
                                  LabelClass.endpoint.format(project_id=project_id),
                                  json_data=json_data)

    @staticmethod
    def copy(API_class, project_id, item_to_copy):
        json_data = {
            'name': item_to_copy['name'],
            'color': item_to_copy['color'],
            'type': item_to_copy['type'],
            'norder': item_to_copy['norder'],
            'icon_url': item_to_copy['icon_url'],
            'parent_id': item_to_copy['parent_id'],
            'removable': item_to_copy['removable']
        }
        return api_requestor.post(API_class,
                                  LabelClass.endpoint.format(project_id=project_id),
                                  json_data=json_data)

    @staticmethod
    def edit(API_class, project_id, label_class_id, name, type, color=None, icon_url=None, norder=None):
        json_data = {
            'name': name,
            'type': type,
            'color': color,
            'icon_url': icon_url,
            'norder': norder
        }
        return api_requestor.edit(API_class,
                                  LabelClass.endpoint_class.format(project_id=project_id,
                                                                   label_class_id=label_class_id),
                                  json_data=json_data)

    @staticmethod
    def delete(API_class, project_id, label_class_id):
        return api_requestor.delete(API_class,
                                    LabelClass.endpoint_class.format(project_id=project_id,
                                                                     label_class_id=label_class_id))

    @staticmethod
    def delete_all(API_class, project_id):
        label_classes = LabelClass.fetch_all(API_class, project_id)
        label_class_ids = [label_class['id'] for label_class in label_classes]
        return [LabelClass.delete(API_class, project_id, label_class_id) for label_class_id in label_class_ids]

    @staticmethod
    def get_total_items(API_class, project_id):
        return LabelClass.list(API_class, project_id, limit=0)['meta']['total']
