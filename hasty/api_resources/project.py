from __future__ import absolute_import, division, print_function

from .. import api_requestor


endpoint = '/v1/projects'


class Project:
    
    @staticmethod
    def list(API_class, offset=0, limit=100):
        json_data = {
            'offset': offset,
            'limit': limit
        }
        return api_requestor.get(API_class, endpoint, json_data=json_data)

    @staticmethod
    def fetch_all(API_class):
        tot = []
        n = Project.get_total_items(API_class)
        for offset in range(0, n, 100):
            tot += Project.list(API_class, offset=offset)['items']
        return tot

    @staticmethod
    def create(API_class, project_name, description):
        return api_requestor.post(API_class, endpoint,
            json_data= {
                'project_name': project_name,
                'description': description
                })
    
    @staticmethod
    def get_total_items(API_class, project_id):
        return Project.list(API_class, limit=0)['meta']['total']
