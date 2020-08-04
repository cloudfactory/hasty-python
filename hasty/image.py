from __future__ import absolute_import, division, print_function
from . import api_requestor


class Image:
    endpoint = '/v1/projects/{project_id}/images'
    endpoint_uploads = '/v1/projects/{project_id}/image_uploads'
    endpoint_image = '/v1/projects/{project_id}/images/{image_id}'

    @staticmethod
    def list(API_class, project_id, offset=0, limit=100):
        json_data = {
            'offset': offset,
            'limit': limit
        }
        return api_requestor.get(API_class,
                                 Image.endpoint.format(project_id=project_id),
                                 json_data=json_data)

    @staticmethod
    def fetch_all(API_class, project_id):
        tot = []
        n = Image.get_total_items(API_class, project_id)
        for offset in range(0, n+1, 100):
            tot += Image.list(API_class, project_id, offset=offset)['items']
        return tot

    @staticmethod
    def create(API_class, project_id, dataset_id, image_url):
        json_data = {
            'url': image_url,
            'dataset_id': dataset_id
        }
        return api_requestor.post(API_class,
                                  Image.endpoint.format(project_id=project_id),
                                  json_data=json_data)

    @staticmethod
    def copy(API_class, project_id, item_to_copy, dataset_mapping):
        json_data = {
            'copy_original': True,
            'dataset_id': dataset_mapping[item_to_copy['dataset_id']],
            'filename': item_to_copy['name'],
            'url': item_to_copy['public_url'],
        }
        return api_requestor.post(API_class,
                                  Image.endpoint.format(project_id=project_id),
                                  json_data=json_data)

    @staticmethod
    def edit(API_class, project_id, image_id, filename, url, copy_original=True):
        json_data = {
            'filename': filename,
            'url': url,
            'copy_original': copy_original
        }
        return api_requestor.edit(API_class,
                                  Image.endpoint_image.format(project_id=project_id,
                                                              image_id=image_id),
                                  json_data=json_data)

    @staticmethod
    def get_total_items(API_class, project_id):
        return Image.list(API_class, project_id, limit=0)['meta']['total']
