from collections import OrderedDict
from time import time
from typing import List
import os
import logging
import urllib.request

from .constants import WAIT_INTERVAL_SEC
from .exception import ValidationException
from .hasty_object import HastyObject
from .requester import Requester


class ExportJob(HastyObject):
    endpoint = '/v1/projects/{project_id}/exports'
    endpoint_export = '/v1/projects/{project_id}/exports/{export_id}'

    def __repr__(self):
        return self.get__repr__(OrderedDict({"id": self._id, "status": self._status}))

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

    @property
    def meta(self):
        return self._meta

    def _init_properties(self):
        self._id = None
        self._status = None
        self._project_id = None
        self._started_on = None
        self._completed_on = None
        self._meta = None
        self._last_check = None

    def _set_prop_values(self, data):
        if "id" in data:
            self._id = data["id"]
        if "status" in data:
            self._status = data["status"]
        if "started_on" in data:
            self._started_on = data["started_on"]
        if "completed_on" in data:
            self._completed_on = data["completed_on"]
        if "meta" in data:
            self._meta = data["meta"]
        if "project_id" in data:
            self._project_id = data["project_id"]

    @staticmethod
    def _create(requester: Requester, project_id: str, name: str, export_format: str,
                dataset: List[str], image_status: List[str], sign_urls: bool,
                semantic_format: str, labels_order: List[str]):
        res = requester.post(ExportJob.endpoint.format(project_id=project_id),
                             json_data={"export_name": name,
                                        "format": export_format,
                                        "dataset_id": dataset,
                                        "image_status": image_status,
                                        "sign_urls": sign_urls,
                                        "semantic_format": semantic_format,
                                        "labels_order": labels_order})
        return ExportJob(requester, res, {"project_id": project_id})

    def check_status(self):
        """
        Checks and returns the status of the export job.
        """
        if self._last_check is None or self._last_check > WAIT_INTERVAL_SEC:
            res = self._requester.get(ExportJob.endpoint_export.format(project_id=self._project_id, export_id=self._id))
            self._set_prop_values(res)
            self._last_check = time()
        return self._status

    def download(self, local_folder='.'):
        """
        Downloads export to specified folder

        Args:
             local_folder (str): Path to the local folder
        """
        self.check_status()
        if self._status == 'DONE':
            url = self._meta['url']
            filename = self._meta.get('export_name', 'export') + '.zip'
            filepath = os.path.join(local_folder, filename)
            urllib.request.urlretrieve(url, filepath)
            logging.info(f"File {filepath} saved")
        else:
            raise ValidationException.export_in_progress()
