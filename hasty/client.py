from typing import Union
import uuid

from .helper import PaginatedList
from .project import Project
from .workspace import Workspace
from .requester import Requester


class Client:
    """Client for Hasty API"""

    def __init__(self, api_key, base_url='https://api.hasty.ai'):
        """
        Initialize the client

        Parameters
        ----------
        api_key
            Your API key

        """
        self.api_key = api_key
        self.base_url = base_url
        self.session_id = str(uuid.uuid4())
        self._requester = Requester(self.api_key, self.base_url, self.session_id)

    def get_workspaces(self):
        """
        Returns the list of workspaces that the user can have an access to
        :returns: A list of :py:class:`~hasty.Workspace` objects.
        """
        return PaginatedList(Workspace, self._requester, Workspace.endpoint)

    def get_projects(self):
        """
        Returns the list of projects
        :returns: A list of :py:class:`~hasty.Project` objects.
        """
        return PaginatedList(Project, self._requester, Project.endpoint)

    def get_project(self, project_id):
        """
        Returns project :py:class:`~hasty.Project` by id

        Arguments:
            project_id (str): Project id
        """
        res = self._requester.get(Project.endpoint_project.format(project_id=project_id))
        return Project(self._requester, res)

    def create_project(self, workspace: Union[str, Workspace], name: str, description: str = None) -> Project:
        """
        Creates new project :py:class:`~hasty.Project`

        Arguments:
            workspace (:py:class:`~hasty.Workspace`, str): Workspace object or id which the project should belongs to
            name (str): Name of the project
            description (str, optional): Project description
        """
        workspace_id = workspace
        if isinstance(workspace, Workspace):
            workspace_id = workspace.id
        return Project.create(self._requester, workspace_id, name, description)
