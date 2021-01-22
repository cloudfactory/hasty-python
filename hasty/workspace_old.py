from __future__ import absolute_import, division, print_function

from . import api_requestor


class Workspace:
    """Class that contains some basic requests and features for workspaces."""
    endpoint = '/v1/workspaces'
    endpoint_workspace = '/v1/workspaces/{workspace_id}'

    @staticmethod
    def list(API_class, offset=0, limit=100):
        """ fetches a list of workspaces given the offset and limit params

        Parameters
        ----------
        API_class : class
            hasty.API class
        offset : int
            query offset param (Default value = 0)
        limit : int
            query limit param (Default value = 100)

        Returns
        -------
        dict
            workspace objects

        """
        json_data = {
            'offset': offset,
            'limit': limit
        }
        return api_requestor.get(API_class,
                                 Workspace.endpoint,
                                 json_data=json_data)

    @staticmethod
    def fetch_workspace(API_class, workspace_id):
        """ fetches workspace's metadata

        Parameters
        ----------
        API_class : class
            hasty.API class
        workspace_id : str
            id of the workspace

        Returns
        -------
        dict
            workspace metadata

        """
        return api_requestor.get(API_class,
                                 Workspace.endpoint_workspace.format(workspace_id=workspace_id))

    @staticmethod
    def fetch_all(API_class):
        """ fetches every workspaces

        Parameters
        ----------
        API_class : class
            hasty.API class

        Returns
        -------
        list [dict]
            workspace objects

        """
        tot = []
        n = Workspace.get_total_items(API_class)
        for offset in range(0, n+1, 100):
            tot += Workspace.list(API_class, offset=offset)['items']
        return tot

    @staticmethod
    def edit_workspace(API_class, workspace_id, name, description=None,
                       background_color=None, logo_url=None, is_public=False, unique_name=None):
        """ edits an existing workspace

        Parameters
        ----------
        API_class : class
            hasty.API class
        workspace_id : str
            id of the workspace
        name : str
            name of the workspace
        description : str
            description of the workspace (Default value = None)
        background_color : str
            background color of the workspace (Default value = None)
        logo_url : str
            url of logo image (Default value = None)
        is_public : bool
            boolean wether the workspace should be public (Default value = False)
        unique_name : str
            unique name of the workspace (Default value = None)

        Returns
        -------
        dict
            new workspace object

        """
        json_data = {
            'name': name,
            'description': description,
            'background_color': background_color,
            'logo_url': logo_url,
            'is_public': is_public,
            'unique_name': unique_name
        }
        return api_requestor.edit(API_class,
                                  Workspace.endpoint_workspace.format(
                                      workspace_id=workspace_id),
                                  json_data=json_data)

    @staticmethod
    def get_total_items(API_class):
        """ gets the number of workspaces

        Parameters
        ----------
        API_class : class
            hasty.API class

        Returns
        -------
        int
            number of workspaces

        """
        return Workspace.list(API_class, limit=0)['meta']['total']
