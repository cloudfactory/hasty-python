from .base import Inference


class SemanticSegmentor(Inference):
    model_check_endpoint = "/v1/projects/{project_id}/semantic_segmentor"
    predict_endpoint = "/v1/projects/{project_id}/semantic_segmentation"

    def discover_model(self):
        """
        Performs model discovery and loads model to GPU
        """
        self._discover_model(self.model_check_endpoint)

    def predict(self, image_url: str = None, image_path: str = None, min_size: float = 0.0):
        """
        Returns predictions for provided image.

        Args:
            image_url (str): Image URL
            image_path (str): Path to local image file
            min_size (float): Ignore prediction with an area less then min_size

        Returns:
            List of dict:
            - bbox (list of int): Coordinates of bounding box [x_min, y_min, x_max, y_max]
            - mask (list of int): RLE Encoded binary mask, (order right -> down)
            - class_id (str): Label class ID
        """
        json_data = {"min_size": min_size,
                     "model_id": self._model_id}
        response = self._predict(image_url, image_path, SemanticSegmentor.predict_endpoint,
                                 SemanticSegmentor.model_check_endpoint, json_data)
        return response
