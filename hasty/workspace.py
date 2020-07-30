from __future__ import absolute_import, division, print_function

from . import api_requestor


class Workspace:
    endpoint = '/v1/workspaces'

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
    def fetch_all(API_class):
        tot = []
        n = Workspace.get_total_items(API_class)
        for offset in range(0, n+1, 100):
            tot += Workspace.list(API_class, offset=offset)['items']
        return tot

    @staticmethod
    def get_total_items(API_class):
        return Workspace.list(API_class, limit=0)['meta']['total']
