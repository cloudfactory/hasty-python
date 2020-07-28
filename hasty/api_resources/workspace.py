from __future__ import absolute_import, division, print_function

from .. import api_requestor


class Workspace:
    endpoint = '/v1/workspaces'

    @staticmethod
    def list(API_class, offset=0, limit=100):
        json_data = {
            'offset': offset,
            'limit': limit
        }
        return api_requestor.get(API_class, Workspace.endpoint, json_data=json_data)
    
    @staticmethod
    def fetch_all(API_class):
        tot = []
        n = Workspace.get_total_items(API_class)
        for offset in range(0, n+1, 100):
            tot += Workspace.list(API_class, offset=offset)['items']
        return tot

    @staticmethod
    def create(API_class, name, is_public=False, logo_url=None, description=None, color="#c69540"): # might not work for the moment
        json_data = {
            'name': name,
            'is_public': is_public,
            'logo_url': logo_url,
            'description': description,
            'background_color': color
        }
        return api_requestor.post(API_class, Workspace.endpoint, json_data=json_data)

    @staticmethod
    def delete(API_class, workspace_id):
        del_endpoint = f'{Workspace.endpoint}/{workspace_id}'
        return api_requestor.delete(API_class, del_endpoint)

    @staticmethod
    def get_total_items(API_class):
        return Workspace.list(API_class, limit=0)['meta']['total']