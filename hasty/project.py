from __future__ import absolute_import, division, print_function

from . import api_requestor


class Project:
    """ """
    endpoint = '/v1/projects'
    endpoint_project = '/v1/projects/{project_id}'

    @staticmethod
    def list(API_class, offset=0, limit=100):
        """ fetches a list of projects given the offset and limit params

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
            project objects

        """
        json_data = {
            'offset': offset,
            'limit': limit
        }
        return api_requestor.get(API_class,
                                 Project.endpoint,
                                 json_data=json_data)

    @staticmethod
    def fetch_all(API_class):
        """ fetches every projects in the workspace

        Parameters
        ----------
        API_class : class
            hasty.API class

        Returns
        -------
        list [dict]
            project objects
        """
        tot = []
        n = Project.get_total_items(API_class)
        for offset in range(0, n+1, 100):
            tot += Project.list(API_class, offset=offset)['items']
        return tot

    @staticmethod
    def fetch_project(API_class, project_id):
        """ fetches project's metadata

        Parameters
        ----------
        API_class : class
            hasty.API class
        project_id : str
            project id

        Returns
        -------
        dict
            project metadata

        """
        return api_requestor.get(API_class,
                                 Project.endpoint_project.format(project_id=project_id))

    @staticmethod
    def create(API_class, project_name, description):
        """ creates a new project

        Parameters
        ----------
        API_class : class
            hasty.API class
        project_name : str
            project name
        description : str
            description

        Returns
        -------
        dict
            new project object

        """
        json_data = {
            'name': project_name,
            'description': description
        }
        return api_requestor.post(API_class,
                                  Project.endpoint,
                                  json_data=json_data)

    @staticmethod
    def edit_project(API_class, project_id, name=None, description=None):
        """ edits an existing project

        Parameters
        ----------
        API_class : class
            hasty.API class
        project_id : str
            project id
        name : str
            name (Default value = None)
        description : str
            description (Default value = None)

        Returns
        -------
        dict
            new project object

        """
        json_data = {
            'name': name,
            'description': description
        }
        return api_requestor.edit(API_class,
                                  Project.endpoint_project.format(project_id=project_id),
                                  json_data=json_data)

    @staticmethod
    def delete_project(API_class, project_id):
        """ deletes the given project

        Parameters
        ----------
        API_class : class
            hasty.API class
        project_id : str
            project id

        Returns
        -------
        json
            empty

        """
        return api_requestor.delete(API_class,
                                    Project.endpoint_project.format(project_id=project_id))

    @staticmethod
    def get_total_items(API_class):
        """ gets the total number of projects in the workspace

        Parameters
        ----------
        API_class : class
            hasty.API class

        Returns
        -------
        int
            number of projects

        """
        print(Project.list(API_class, limit=0))
        return Project.list(API_class, limit=0)['meta']['total']
