from __future__ import absolute_import, division, print_function

from . import api_requestor


class Project:
    endpoint = '/v1/projects'
    endpoint_project = '/v1/projects/{project_id}'

    @staticmethod
    def list(API_class, offset=0, limit=100):
        json_data = {
            'offset': offset,
            'limit': limit
        }
        return api_requestor.get(API_class,
                                 Project.endpoint,
                                 json_data=json_data)

    @staticmethod
    def fetch_all(API_class):
        tot = []
        n = Project.get_total_items(API_class)
        for offset in range(0, n+1, 100):
            tot += Project.list(API_class, offset=offset)['items']
        return tot

    @staticmethod
    def fetch_project(API_class, project_id):
        return api_requestor.get(API_class,
                                 Project.endpoint_project.format(project_id=project_id))

    @staticmethod
    def create(API_class, project_name, description):
        json_data = {
            'name': project_name,
            'description': description
        }
        return api_requestor.post(API_class,
                                  Project.endpoint,
                                  json_data=json_data)
    @staticmethod
    def edit_project(API_class, project_id, name=None, description=None):
        json_data = {
            'name': name,
            'description': description
        }
        return api_requestor.edit(API_class,
                                  Project.endpoint_project.format(project_id=project_id),
                                  json_data=json_data)

    @staticmethod
    def delete_project(API_class, project_id):
        return api_requestor.delete(API_class,
                                    Project.endpoint_project.format(project_id=project_id))

    @staticmethod
    def get_total_items(API_class):
        print(Project.list(API_class, limit=0))
        return Project.list(API_class, limit=0)['meta']['total']
