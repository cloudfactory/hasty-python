import os

from ..image import Image
from .base import Inference


class Detector(Inference):
    model_check_endpoint = "/v1/projects/{project_id}/object_detector"
    predict_endpoint = "/v1/projects/{project_id}/object_detection"

    def discover_model(self):
        self._discover_model(self.model_check_endpoint)

    def predict(self, image_url: str = None, image_path: str = None, confidence_threshold: float = 0.5,
                max_detections_per_image: int = 100):
        if image_path is not None:
            url_data = Image._generate_sign_url(self._requester, self._project_id)
            with open(image_path, 'rb') as f:
                self._requester.put(url_data['url'], data=f.read(), content_type="image/*")
            image_url = url_data['url']
        response = self._requester.post(Detector.predict_endpoint.format(project_id=self._project_id),
                                        json_data={"image_url": image_url,
                                                   "confidence_threshold": confidence_threshold,
                                                   "max_detections_per_image": max_detections_per_image,
                                                   "model_id": self._model_id})
        return response
