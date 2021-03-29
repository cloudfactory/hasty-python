import os

from ..image import Image
from .base import Inference


class SemanticSegmentor(Inference):
    model_check_endpoint = "/v1/projects/{project_id}/semantic_segmentor"
    predict_endpoint = "/v1/projects/{project_id}/semantic_segmentation"

    def discover_model(self):
        self._discover_model(self.model_check_endpoint)

    def predict(self, image_url: str = None, image_path: str = None, min_size: float = 0.0):
        if image_path is not None:
            url_data = Image._generate_sign_url(self._requester, self._project_id)
            with open(image_path, 'rb') as f:
                self._requester.put(url_data['url'], data=f.read(), content_type="image/*")
            image_url = url_data['url']
        response = self._requester.post(SemanticSegmentor.predict_endpoint.format(project_id=self._project_id),
                                        json_data={"image_url": image_url,
                                                   "min_size": min_size,
                                                   "model_id": self._model_id})
        return response
