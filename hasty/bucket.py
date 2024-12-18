from collections import OrderedDict
from dataclasses import dataclass
from typing import Union, Protocol

from .constants import BucketProviders
from .hasty_object import HastyObject

@dataclass
class Credentials(Protocol):
    def get_credentials(self):
        raise NotImplementedError

    def cloud_provider(self):
        raise NotImplementedError

@dataclass
class DummyCreds(Credentials):
    secret: str

    def get_credentials(self):
        return {"secret": self.secret, "cloud_provider": BucketProviders.DUMMY}

    def cloud_provider(self):
        return BucketProviders.DUMMY

@dataclass
class GCSCreds(Credentials):
    bucket: str
    key_json: str

    def get_credentials(self):
        return {"bucket_gcs": self.bucket, "key_json": self.key_json, "cloud_provider": BucketProviders.GCS}

    def cloud_provider(self):
        return BucketProviders.GCS

@dataclass
class S3Creds(Credentials):
    bucket: str
    role: str

    def get_credentials(self):
        return {"bucket_s3": self.bucket, "role": self.role, "cloud_provider": BucketProviders.S3}

    def cloud_provider(self):
        return BucketProviders.S3

@dataclass
class AZCreds(Credentials):
    account_name: str
    secret_access_key: str
    container: str

    def get_credentials(self):
        return {"account_name": self.account_name, "secret_access_key": self.secret_access_key,
                "container": self.container, "cloud_provider": BucketProviders.AZ}

    def cloud_provider(self):
        return BucketProviders.AZ

class Bucket(HastyObject):
    """Class that contains some basic requests and features for bucket management"""
    endpoint = '/v1/buckets/{workspace_id}/credentials'

    def __repr__(self):
        return self.get__repr__(OrderedDict({"id": self._id, "name": self._name, "cloud_provider": self._cloud_provider}))

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
    def cloud_provider(self):
        """
        :type: string
        """
        return self._cloud_provider

    def _init_properties(self):
        self._id = None
        self._name = None
        self._cloud_provider = None

    def _set_prop_values(self, data):
        if "credential_id" in data:
            self._id = data["credential_id"]
        if "description" in data:
            self._name = data["description"]
        if "cloud_provider" in data:
            self._cloud_provider = data["cloud_provider"]

    @staticmethod
    def _create_bucket(requester, workspace_id, name, credentials: Union[DummyCreds, GCSCreds, S3Creds, AZCreds]):
        json = {"description": name, "cloud_provider": credentials.cloud_provider(), **credentials.get_credentials()}
        data = requester.post(Bucket.endpoint.format(workspace_id=workspace_id), json_data=json)
        return Bucket(requester, data)
