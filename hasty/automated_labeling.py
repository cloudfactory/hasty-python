from collections import OrderedDict
from typing import Optional

from .hasty_object import HastyObject
from .requester import Requester


class AutomatedLabelingJob(HastyObject):
    endpoint = '/v1/projects/{project_id}/automated_labeling'

    def __repr__(self):
        return self.get__repr__(OrderedDict({"id": self._id,
                                             "status": self._status,
                                             "progress": self._progress}))

    @property
    def id(self):
        """
        :type: string
        """
        return self._id

    @property
    def status(self):
        """
        :type: string
        """
        return self._status

    @property
    def project_id(self):
        """
        :type: string
        """
        return self._project_id

    @property
    def progress(self):
        """
        :type: float
        """
        return self._progress

    @property
    def started_on(self):
        """
        :type: string
        """
        return self._started_on

    @property
    def completed_on(self):
        """
        :type: string
        """
        return self._completed_on

    def _init_properties(self):
        self._job_id = None
        self._status = None
        self._project_id = None
        self._started_on = None
        self._completed_on = None
        self._last_check = None
        self._progress = None

    def _set_prop_values(self, data):
        if "job_id" in data:
            self._id = data["job_id"]
        if "status" in data:
            self._status = data["status"]
        if "start_date" in data:
            self._started_on = data["start_date"]
        if "end_date" in data:
            self._completed_on = data["end_date"]
        if "project_id" in data:
            self._project_id = data["project_id"]
        if "progress" in data:
            self._progress = data["progress"]

    @staticmethod
    def _create(requester: Requester, project_id: str, experiment_id: str, confidence_threshold: float = 0.8,
                max_detections_per_image: int = 100, num_images: int = 0, masker_threshold: float = 0.5,
                dataset_id: Optional[str] = None):
        res = requester.post(AutomatedLabelingJob.endpoint.format(project_id=project_id),
                             json_data={"experiment_id": experiment_id,
                                        "confidence_threshold": confidence_threshold,
                                        "max_detections_per_image": max_detections_per_image,
                                        "num_images": num_images,
                                        "masker_threshold": masker_threshold,
                                        "dataset_id": dataset_id})
        return AutomatedLabelingJob(requester, res, {"project_id": project_id})