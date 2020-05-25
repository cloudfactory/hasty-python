from __future__ import absolute_import, division, print_function

from .. import api_requestor


endpoint = '/v1/projects'


class Project:
    
    @staticmethod
    def list():
        return api_requestor.get(endpoint)

    @staticmethod
    def create(project_name, description):
        return api_requestor.post(endpoint,
                                  json_data={'project_name': project_name,
                                             'description': description})
