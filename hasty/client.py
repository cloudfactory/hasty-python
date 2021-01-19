import uuid

from .helper import PaginatedList
from .project import Project
from .requester import Requester


class Client:

    def __init__(self, api_key, base_url='https://api.hasty.ai'):
        self.api_key = api_key
        self.base_url = base_url
        self.session_id = str(uuid.uuid4())
        self._requester = Requester(self.api_key, self.base_url, self.session_id)

    def get_projects(self):
        return PaginatedList(Project, self._requester, Project.endpoint)
