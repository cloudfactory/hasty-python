from __future__ import absolute_import, division, print_function

from .. import api_requestor


endpoint = '/v1/projects/{project_id}/image/{image_id}/labels'
label_attribute_endpoint = '/v1/projects/{project_id}/labels/{label_id}/attributes'


class Label:
    
    @staticmethod
    def list(project_id, image_id):
        return api_requestor.get(endpoint.format(project_id=project_id,
                                                 image_id=image_id))

    @staticmethod
    def create(project_id, image_id, class_id, bbox, z_index=0):
        return api_requestor.post(endpoint.format(project_id=project_id, image_id=image_id),
                                  json_data=[{'class_id': class_id,
                                              'bbox': bbox,
                                              'z_index': z_index}])

    @staticmethod
    def delete(project_id, image_id, label_ids):
        if isinstance(label_ids, int):
            label_ids = [label_ids]
        return api_requestor.delete(endpoint.format(project_id=project_id, image_id=image_id),
                                    json_data={'labels': [{'label_id': label_id} for label_id in label_ids]})


class LabelAttribute:

    @staticmethod
    def set(project_id, label_id, attribute_id, value):
        set_endpoint = f'{label_attribute_endpoint}/{attribute_id}'
        return api_requestor.post(set_endpoint.format(project_id=project_id, label_id=label_id,
                                                      attribute_id=set_endpoint),
                                  json_data={'value': value})
