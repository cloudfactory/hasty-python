from __future__ import absolute_import, division, print_function

from .. import api_requestor


endpoint = '/v1/projects/{project_id}/datasets'


class Dataset:

    @staticmethod
    def list(project_id):
        return api_requestor.get(endpoint.format(project_id=project_id))

    @staticmethod
    def create(project_id, dataset_name):
        return api_requestor.post(endpoint.format(project_id=project_id),
                                  json_data={'dataset_name': dataset_name})
