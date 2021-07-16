from typing import List

from .base import Inference
from ..exception import ValidationException
from ..label_utils import check_bbox_format


class Attributer(Inference):
    model_check_endpoint = "/v1/projects/{project_id}/attributer"
    predict_endpoint = "/v1/projects/{project_id}/attribute_prediction"

    def discover_model(self):
        """
        Performs model discovery and loads model to GPU
        """
        self._discover_model(self.model_check_endpoint)

    def predict(self, image_url: str = None, image_path: str = None, bboxes: List[List[str]] = None,
                confidence_threshold: float = 0.5):
        """
        Returns predictions for provided image.

        Args:
            image_url (str): Image URL
            image_path (str): Path to local image file
            bboxes (list of list of int): List of bounding boxes [x_min, y_min, x_max, y_max]
            confidence_threshold (float): Confidence threshold [0, 1) (default 0.5)

        Returns:
            List of List of dict:
            - bbox (list of int): Coordinates of bounding box [x_min, y_min, x_max, y_max]
            - attribute_id (str): Attribute  id
            - lov_ids (list of str): List of attribute values
        """
        # Validate bboxes
        if not isinstance(bboxes, list):
            raise ValidationException("bboxes parameter must be a list of bboxes")
        for bbox in bboxes:
            if not isinstance(bbox, list):
                raise ValidationException(f"Bounding box must be a list of inegers, got {type(bbox)}")
            # Check bbox
            if bbox is not None:
                if not check_bbox_format(bbox):
                    raise ValidationException(f"Invalid bbox format - {bbox}")

        json_data = {"bboxes": bboxes,
                     "model_id": self._model_id,
                     "confidence_threshold": confidence_threshold}
        response = self._predict(image_url, image_path, Attributer.predict_endpoint,
                                 Attributer.model_check_endpoint, json_data)
        return response
