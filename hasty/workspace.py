from __future__ import absolute_import, division, print_function

from . import api_requestor


class Workspace:
    endpoint = '/v1/workspaces'
    endpoint_workspace = '/v1/workspaces/{workspace_id}'

    @staticmethod
    def list(API_class, offset=0, limit=100):
        json_data = {
            'offset': offset,
            'limit': limit
        }
        return api_requestor.get(API_class,
                                 Workspace.endpoint,
                                 json_data=json_data)

    @staticmethod
    def fetch_workspace(API_class, workspace_id):
        return api_requestor.get(API_class,
                                 Workspace.endpoint_workspace.format(workspace_id=workspace_id))

    @staticmethod
    def fetch_all(API_class):
        tot = []
        n = Workspace.get_total_items(API_class)
        for offset in range(0, n+1, 100):
            tot += Workspace.list(API_class, offset=offset)['items']
        return tot

    @staticmethod
    def edit_workspace(API_class, workspace_id, name, description=None,
                       background_color=None, logo_url=None, is_public=False, unique_name=None):
        json_data = {
            'name': name,
            'description': description,
            'background_color': background_color,
            'logo_url': logo_url,
            'is_public': is_public,
            'unique_name': unique_name
        }
        return api_requestor.edit(API_class,
                                  Workspace.endpoint_workspace.format(workspace_id=workspace_id),
                                  json_data=json_data)


    @staticmethod
    def get_total_items(API_class):
        return Workspace.list(API_class, limit=0)['meta']['total']
