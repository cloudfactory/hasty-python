from typing import List

from .base import Inference


class Attributer(Inference):
    model_check_endpoint = "/v1/projects/{project_id}/attributer"
    predict_endpoint = "/v1/projects/{project_id}/attribute_prediction"

    def discover_model(self):
        """
        Performs model discovery and loads model to GPU
        """
        self._discover_model(self.model_check_endpoint)

    def predict(self, image_url: str = None, image_path: str = None, bboxes: List[List[str]] = None):
        """
        Returns predictions for provided image.

        Args:
            image_url (str): Image URL
            image_path (str): Path to local image file
            bboxes (list of list of int): List of bounding boxes [x_min, y_min, x_max, y_max]

        Returns:
            List of List of dict:
            - bbox (list of int): Coordinates of bounding box [x_min, y_min, x_max, y_max]
            - attribute_id (str): Attribute  id
            - lov_ids (list of str): List of attribute values
        """
        json_data = {"bboxes": bboxes,
                     "model_id": self._model_id}
        response = self._predict(image_url, image_path, Attributer.predict_endpoint,
                                 Attributer.model_check_endpoint, json_data)
        return response
