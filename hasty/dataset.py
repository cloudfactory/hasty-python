from __future__ import absolute_import, division, print_function

from . import api_requestor


class Dataset:
    endpoint = '/v1/projects/{project_id}/datasets'
    endpoint_dataset = '/v1/projects/{project_id}/datasets/{dataset_id}'

    @staticmethod
    def list(API_class, project_id, offset=0, limit=100):
        json_data = {
            'offset': offset,
            'limit': limit
        }
        return api_requestor.get(API_class,
                                 Dataset.endpoint.format(project_id=project_id),
                                 json_data=json_data)

    @staticmethod
    def fetch_all(API_class, project_id):
        tot = []
        n = Dataset.get_total_items(API_class, project_id)
        for offset in range(0, n+1, 100):
            tot += Dataset.list(API_class, project_id, offset=offset)['items']
        return tot

    @staticmethod
    def create(API_class, project_id, dataset_id, name, norder):
        json_data = {
            'id': dataset_id,
            'name': name,
            'norder': norder
        }
        return api_requestor.post(API_class,
                                  Dataset.endpoint.format(project_id=project_id),
                                  json_data=json_data)

    @staticmethod
    def copy(API_class, project_id, item_to_copy):
        json_data = {
            'id': item_to_copy['id'],
            'name': item_to_copy['name'],
            'norder': item_to_copy['norder']
        }
        return api_requestor.post(API_class,
                                  Dataset.endpoint.format(project_id=project_id),
                                  json_data=json_data)

    @staticmethod
    def edit_dataset(API_class, project_id, dataset_id, name, norder=None):
        json_data = {
            'name': name,
            'norder': norder
        }
        return api_requestor.edit(API_class,
                                  Dataset.endpoint_dataset.format(project_id=project_id,
                                                                  dataset_id=dataset_id),
                                  json_data=json_data)

    @staticmethod
    def delete_dataset(API_class, project_id, dataset_id):
        return api_requestor.delete(API_class,
                                    Dataset.endpoint_dataset.format(project_id=project_id,
                                                                    dataset_id=dataset_id))

    @staticmethod
    def delete_all(API_class, project_id):
        datasets = Dataset.fetch_all(API_class, project_id)
        dataset_ids = [dataset['id'] for dataset in datasets]
        return [Dataset.delete_dataset(API_class,
                                       project_id,
                                       dataset_id)
                for dataset_id in dataset_ids]

    @staticmethod
    def get_total_items(API_class, project_id):
        return Dataset.list(API_class, project_id, limit=0)['meta']['total']
