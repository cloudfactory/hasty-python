from collections import OrderedDict

from hasty.hasty_object import HastyObject

from ..image import Image
from ..exception import InferenceException


class Inference(HastyObject):

    def __repr__(self):
        return self.get__repr__(OrderedDict({"model_id": self._model_id,
                                             "status": self._status}))

    @property
    def model_id(self):
        """
        :type integer
        """
        return self._model_id

    @property
    def status(self):
        """
        :type string
        """
        return self._status

    @property
    def project_id(self):
        """
        :type string
        """
        return self._project_id

    def _init_properties(self):
        self._model_id = None
        self._last_check = None
        self._status = None
        self._project_id = None

    def _set_prop_values(self, data):
        if "model_id" in data:
            self._model_id = data["model_id"]
        if "status" in data:
            self._status = data["status"]
        if "project_id" in data:
            self._project_id = data["project_id"]

    def _discover_model(self, endpoint):
        res = self._requester.get(endpoint.format(project_id=self._project_id))
        self._set_prop_values(res)

    def _predict(self, image_url: str, image_path: str, endpoint: str,
                 discover_endpoint: str, json_data):
        if self._status != 'LOADED':
            self._discover_model(discover_endpoint)
        if self._status != 'LOADED':
            raise InferenceException.model_not_loaded()
        if image_path is not None:
            url_data = HastyObject._generate_sign_url(self._requester, self._project_id)
            with open(image_path, 'rb') as f:
                self._requester.put(url_data['url'], data=f.read(), content_type="image/*")
            upload_id = url_data['id']
            json_data['upload_id'] = upload_id
        else:
            json_data['image_url'] = image_url
        response = self._requester.post(endpoint.format(project_id=self._project_id),
                                        json_data=json_data)
        return response
