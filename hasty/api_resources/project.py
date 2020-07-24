from __future__ import absolute_import, division, print_function

from .. import api_requestor


endpoint = '/v1/projects'


class Project:
    
    @staticmethod
    def list(API_class):
        return api_requestor.get(API_class, endpoint)

    @staticmethod
    def create(API_class, project_name, description):
        return api_requestor.post(API_class, endpoint,
            json_data= {
                'project_name': project_name,
                'description': description
                })
