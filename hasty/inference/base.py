from hasty.hasty_object import HastyObject


class Inference(HastyObject):
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

    def predict(self, image_url: str = None, image_path: str = None, **kwargs):
        pass
