import os
from typing import List, Optional, Union
import urllib.error
import urllib.request

from .hasty_object import HastyObject
from .activity import ActivityType, Activity
from .dataset import Dataset
from .helper import PaginatedList
from .constants import VideoStatus, VALID_VIDEO_STATUSES
from .exception import ValidationException


class Video(HastyObject):
    endpoint = '/v1/projects/{project_id}/videos'
    endpoint_video = '/v1/projects/{project_id}/videos/{video_id}'

    @property
    def id(self):
        """
        :type: string
        """
        return self._id

    @property
    def name(self):
        """
        :type: string
        """
        return self._name

    @property
    def project_id(self):
        """
        :type: string
        """
        return self._project_id

    @property
    def dataset_id(self):
        """
        :type: string
        """
        return self._dataset_id

    @property
    def status(self):
        """
        :type: string
        """
        return self._status

    @property
    def width(self):
        """
        :type: int
        """
        return self._width

    @property
    def height(self):
        """
        :type: int
        """
        return self._height

    @property
    def public_url(self):
        """
        :type: string
        """
        return self._public_url

    @property
    def format(self):
        """
        :type: string
        """
        return self._format

    @property
    def duration_ms(self):
        """
        :type: int
        """
        return self._duration_ms

    @property
    def duration_frames(self):
        """
        :type: int
        """
        return self._duration_frames

    @property
    def health_status(self):
        """
        :type: string
        """
        return self._health_status

    def _init_properties(self):
        self._id = None
        self._name = None
        self._project_id = None
        self._dataset_id = None
        self._status = None
        self._public_url = None
        self._width = None
        self._height = None
        self._format = None
        self._duration_ms = None
        self._duration_frames = None
        self._health_status = None

    def _set_prop_values(self, data):
        if "id" in data:
            self._id = data["id"]
        if "name" in data:
            self._name = data["name"]
        if "project_id" in data:
            self._project_id = data["project_id"]
        if "dataset_id" in data:
            self._dataset_id = data["dataset_id"]
        if "status" in data:
            self._status = data["status"]
        if "public_url" in data:
            self._public_url = data["public_url"]
        if "width" in data:
            self._width = data["width"]
        if "height" in data:
            self._height = data["height"]
        if "format" in data:
            self._format = data["format"]
        if "duration_ms" in data:
            self._duration_ms = data["duration_ms"]
        if "duration_frames" in data:
            self._duration_frames = data["duration_frames"]
        if "health_status" in data:
            self._health_status = data["health_status"]

    @classmethod
    def _get_by_id(cls, requester, project_id, video_id):
        data = requester.get(cls.endpoint_video.format(project_id=project_id, video_id=video_id))
        return Video(requester, data, {"project_id": project_id})

    @staticmethod
    def _upload_from_file(requester, project_id, dataset_id, filepath: str = None):
        filename = os.path.basename(filepath)
        url_data = HastyObject._generate_sign_url(requester, project_id)
        with open(filepath, 'rb') as f:
            requester.put(url_data['url'], data=f.read(), content_type="")
        res = requester.post(Video.endpoint.format(project_id=project_id),
                             json_data={"dataset_id": dataset_id,
                                        "filename": filename,
                                        "upload_id": url_data["id"]})
        return Video(requester, res, {"project_id": project_id,
                                      "dataset_id": dataset_id})

    @staticmethod
    def _upload_from_url(requester, project_id, dataset_id, filename, url):
        res = requester.post(Video.endpoint.format(project_id=project_id),
                             json_data={"dataset_id": dataset_id,
                                        "filename": filename,
                                        "url": url})
        return Video(requester, res, {"project_id": project_id,
                                      "dataset_id": dataset_id})

    def create_activity(self, start_time_ms: int, end_time_ms: int,
                        activity_types: Union[List[str], List[ActivityType]], replace_overlap=False):
        """
        Create activity

        Args:
            video_id (str): Video ID
            start_time_ms (int): Start time in milliseconds
            end_time_ms (int): End time in milliseconds
            activity_types: List of `~hasty.ActivityType` or `str` (IDs)
            replace_overlap: Replace overlapping activities
        """
        return Activity._create(requester=self._requester, project_id=self._project_id,
                                video_id=self._id, activities=activity_types,
                                start_time_ms=start_time_ms, end_time_ms=end_time_ms,
                                replace_overlap=replace_overlap)

    def get_activities(self, activity_type_id: Optional[str] = None,
                       start_time_ms: Optional[int] = None, end_time_ms: Optional[int] = None):
        """
        Returns activities (list of `~hasty.Activity` objects) for the video
        """
        params = {}
        if start_time_ms:
            params["start_time_ms"] = start_time_ms
        if end_time_ms:
            params["end_time_ms"] = end_time_ms
        if activity_type_id:
            params["activity_type_id"] = activity_type_id
        return PaginatedList(Activity, self._requester,
                             Activity.endpoint.format(project_id=self._project_id, video_id=self._id),
                             query_params=params,
                             obj_params={"project_id": self._project_id, "video_id": self._id})

    def check_health(self) -> str:
        """
        Checks health status of the video
        """
        if self._health_status == "PROCESSING":
            v = self._get_by_id(self._requester, self._project_id, self._id)
            self._health_status = v._health_status
        return self._health_status

    def set_status(self, status: str):
        """
        Set video status

        Args:
            status: New status one of ["NEW", "DONE", "SKIPPED", "IN PROGRESS", "TO REVIEW"]
        """
        if status not in VALID_VIDEO_STATUSES:
            raise ValidationException(f"Got {status}, expected on of {VALID_VIDEO_STATUSES}")
        self._requester.put(Video.endpoint_video.format(project_id=self.project_id,
                                                        video_id=self.id) + "/status",
                            json_data={"status": status})
        self._status = status

    def download(self, filepath: str):
        """
        Downloads video to file

        Args:
            filepath (str): Local path
        """
        if self.check_health() != "OK":
            raise ValidationException.video_not_ready()
        try:
            urllib.request.urlretrieve(self._public_url, filepath)
        except urllib.error.HTTPError as e:
            if e.code == 404:
                raise ValidationException.video_not_ready()
            raise e

    def rename(self, new_name: str):
        """
        Rename video

        Args:
            new_name (str): New video name
        """
        response = self._requester.patch(Video.endpoint_video.format(project_id=self.project_id,
                                                                     video_id=self.id),
                                         json_data={"filename": new_name})
        self._name = response.get("name")

    def move(self, dataset: Union[Dataset, str]):
        """
        Move video to another dataset
        """
        dataset_id = dataset
        if isinstance(dataset, Dataset):
            dataset_id = dataset.id
        response = self._requester.patch(Video.endpoint_video.format(project_id=self.project_id,
                                                                     video_id=self.id),
                                         json_data={"dataset_id": dataset_id})
        self._dataset_id = response.get("dataset_id")
        self._dataset_name = response.get("dataset_name")

    def delete(self):
        """
        Removes video
        """
        self._requester.delete(Video.endpoint_video.format(project_id=self.project_id,
                                                           video_id=self.id))
