from __future__ import absolute_import, division, print_function
import os

from .. import api_requestor


endpoint = '/v1/projects/{project_id}/images'


class Image:
    @staticmethod
    def list(API_class, project_id, offset=0, limit=100):
        json_data = {
            'offset': offset,
            'limit': limit
        }
        return api_requestor.get(API_class, endpoint.format(project_id=project_id), json_data)

    @staticmethod
    def create(API_class, project_id, dataset_id, image_url):
        json_data = {
            'url': image_url,
            'dataset_id': dataset_id
        }
        return api_requestor.post(API_class, endpoint.format(project_id=project_id),
                                  json_data=json_data)

    ''' # need to see if still working
    @staticmethod
    def upload(API_class, project_id, dataset_id, file_path):
        files_request = {
            "dataset_id": (None, dataset_id),
            "image": (os.path.basename(file_path), open(file_path, 'rb'))
        }
        return api_requestor.post(API_class, endpoint.format(project_id=project_id),
                                  files=files_request)
    '''