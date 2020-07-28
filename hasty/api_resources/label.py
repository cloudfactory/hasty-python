from __future__ import absolute_import, division, print_function

from .. import api_requestor


endpoint_project = '/v1/projects/{project_id}/labels'
endpoint_image = '/v1/projects/{project_id}/images/{image_id}/labels'


class Label:
    
    @staticmethod
    def list_project(API_class, project_id, offset=0, limit=100):
        json_data = {
            'offset': offset,
            'limit': limit
        }
        return api_requestor.get(API_class, endpoint_project.format(project_id=project_id), json_data=json_data)

    @staticmethod
    def list_image(API_class, project_id, image_id, offset=0, limit=100):
        json_data = {
            'offset': offset,
            'limit': limit
        }        
        return api_requestor.get(API_class, endpoint_image.format(project_id=project_id, image_id=image_id), json_data=json_data)

    @staticmethod
    def fetch_all(API_class, project_id, image_mapping):
        tot = []
        n = Label.get_total_items(API_class, project_id)
        for image_id in image_mapping:
            image_labs = []
            for offset in range(0, n+1, 100):
                image_labs += Label.list_image(API_class, project_id, image_id, offset=offset)['items']
            tot += image_labs
        return tot

    @staticmethod
    def create(API_class, project_id, image_id, class_id, bbox, mask, polygon, z_index=0):
        json_data = [{
            'class_id': class_id,
            'bbox': bbox,
            'mask': mask,
            'polygon': polygon,
            'z_index': z_index
            }]

        return api_requestor.post(API_class, endpoint_image.format(project_id=project_id, image_id=image_id), json_data=json_data)

    @staticmethod
    def copy(API_class, project_id, item_to_copy, image_mapping, label_class_mapping):
        json_data = [{
            'class_id': label_class_mapping[item_to_copy['class_id']],
            'bbox': item_to_copy['bbox'],
            'mask': item_to_copy['mask'],
            'polygon': item_to_copy['polygon'],
            'z_index': item_to_copy['z_index'],
            'tool_used': item_to_copy['tool_used']
        }]
        image_id = image_mapping[item_to_copy['image_id']]
        return api_requestor.post(API_class, endpoint_image.format(project_id=project_id, image_id=image_id), json_data=json_data)

    @staticmethod
    def delete_batch(API_class, project_id, image_id, label_ids):
        if isinstance(label_ids, int): # if a single ID value is gived, transform it into a list
            label_ids = [label_ids]
        return api_requestor.delete(API_class, endpoint_image.format(project_id=project_id, image_id=image_id),
                                    json_data={'labels': [{'label_id': label_id} for label_id in label_ids]})

    @staticmethod
    def get_total_items(API_class, project_id):
        return Label.list_project(API_class, project_id, limit=0)['meta']['total']

