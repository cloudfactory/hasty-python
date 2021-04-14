from .base import Inference


class InstanceSegmentor(Inference):
    model_check_endpoint = "/v1/projects/{project_id}/instance_segmentor"
    predict_endpoint = "/v1/projects/{project_id}/instance_segmentation"

    def discover_model(self):
        """
        Performs model discovery and loads model to GPU
        """
        self._discover_model(self.model_check_endpoint)

    def predict(self, image_url: str = None, image_path: str = None, confidence_threshold: float = 0.5,
                max_detections_per_image: int = 100):
        """
        Returns predictions for provided image.

        Args:
            image_url (str): Image URL
            image_path (str): Path to local image file
            confidence_threshold (float): Confidence threshold [0, 1) (default 0.5)
            max_detections_per_image (int): Maximum detections per image (default 100)

        Returns:
            List of dict:
            - bbox (list of int): Coordinates of bounding box [x_min, y_min, x_max, y_max]
            - mask (list of int): RLE Encoded binary mask, (order right -> down)
            - score (float): Confidence score
            - class_id (str): Label class ID
        """
        json_data = {"confidence_threshold": confidence_threshold,
                     "max_detections_per_image": max_detections_per_image,
                     "model_id": self._model_id}
        response = self._predict(image_url, image_path, InstanceSegmentor.predict_endpoint,
                                 InstanceSegmentor.model_check_endpoint, json_data)
        return response
