from __future__ import absolute_import, division, print_function

from . import api_requestor


class Label:
    """Class that contains some basic requests and features for labels."""
    endpoint_image = '/v1/projects/{project_id}/images/{image_id}/labels'
    endpoint_project = '/v1/projects/{project_id}/labels'

    @staticmethod
    def list_project(API_class, project_id, offset=0, limit=100):
        """ fetches a list of label given the offset and limit params from the project endpoint

        Parameters
        ----------
        API_class : class
            hasty.API class
        project_id : str
            id of the project
        offset : int
            query offset param (Default value = 0)
        limit : int
            query limit param (Default value = 100)

        Returns
        -------
        dict
            label objects from project endpoint

        """
        json_data = {
            'offset': offset,
            'limit': limit
        }
        return api_requestor.get(API_class,
                                 Label.endpoint_project.format(
                                     project_id=project_id),
                                 json_data=json_data)

    @staticmethod
    def list_image(API_class, project_id, image_id, offset=0, limit=100):
        """ fetches a list of label given the offset and limit params from the image endpoint

        Parameters
        ----------
        API_class : class
            hasty.API class
        project_id : str
            id of the project
        image_id : str
            image id
        offset : int
            query offset param (Default value = 0)
        limit : int
            query limit param (Default value = 100)

        Returns
        -------
        dict
            label objects from project image

        """
        json_data = {
            'offset': offset,
            'limit': limit
        }
        return api_requestor.get(API_class,
                                 Label.endpoint_image.format(project_id=project_id,
                                                             image_id=image_id),
                                 json_data=json_data)

    @staticmethod
    def fetch_all_image(API_class, project_id, image_id):
        """ fetches every labels of the given image using the image endpoint

        Parameters
        ----------
        API_class : class
            hasty.API class
        project_id : str
            id of the project
        image_id : str
            id of the image

        Returns
        -------
        list [dict]
            label objects from image endpoint
        """
        tot = []
        n = Label.get_total_items_image(API_class, project_id, image_id)
        for offset in range(0, n+1, 100):
            tot += Label.list_image(API_class, project_id,
                                    image_id, offset=offset)['items']
        return tot

    @staticmethod
    def fetch_all_project(API_class, project_id, image_id):
        """ fetches every labels in the project using the project endpoint

        Parameters
        ----------
        API_class : class
            hasty.API class
        project_id : str
            id of the project
        image_id : str
            id of the image

        Returns
        -------
        list [dict]
            label objects from project endpoint

        """
        tot = []
        n = Label.get_total_items_project(API_class, project_id)
        for offset in range(0, n+1, 100):
            tot += Label.list_project(API_class,
                                      project_id, offset=offset)['items']
        return tot

    @staticmethod
    def fetch_all_images(API_class, project_id, image_ids):
        """ fetches every labels from the image_ids iterable using the image endpoint

        Parameters
        ----------
        API_class : class
            hasty.API class
        project_id : str
            id of the project
        image_ids : iterable
            iterable of image ids

        Returns
        -------
        list [dict]
            label objects from image endpoint

        """
        tot = []
        for image_id in image_ids:
            tot += Label.fetch_all_image(API_class, project_id, image_id)
        return tot

    @staticmethod
    def create(API_class, project_id, image_id, class_id, bbox, mask, polygon, z_index=0):
        """ create a new label for the given image

        Parameters
        ----------
        API_class : class
            hasty.API class
        project_id : str
            id of the project
        image_id : str
            image id
        class_id : str
            label class id
        bbox : list [int]
            bounding box coordinates
        mask : list [int]
            mask encoded label
        polygon : list [int]
            polygon label coordinates
        z_index : int
            z position index (Default value = 0)

        Returns
        -------
        dict
            label object

        """
        json_data = [{
            'class_id': class_id,
            'bbox': bbox,
            'mask': mask,
            'polygon': polygon,
            'z_index': z_index
        }]
        return api_requestor.post(API_class,
                                  Label.endpoint_image.format(project_id=project_id,
                                                              image_id=image_id),
                                  json_data=json_data)

    @staticmethod
    def copy(API_class, project_id, items_to_copy, image_mapping, label_class_mapping):
        """ copies a label object to the given image

        Parameters
        ----------
        API_class : class
            hasty.API class
        project_id : str
            id of the project
        items_to_copy : dict
            label objects to copy
        image_mapping : dict
            image ids mapping from src to dst
        label_class_mapping :
            label class ids mapping from src to dst

        Returns
        -------
        dict
            label objects

        """
        json_data = [{
            'class_id': label_class_mapping[i['class_id']],
            'bbox': i['bbox'],
            'mask': i['mask'],
            'polygon': i['polygon'],
            'z_index': i['z_index'],
            'tool_used': i['tool_used']
        } for i in items_to_copy]
        image_id = image_mapping[items_to_copy[0]['image_id']]
        return api_requestor.post(API_class,
                                  Label.endpoint_image.format(project_id=project_id,
                                                              image_id=image_id),
                                  json_data=json_data)

    @staticmethod
    def edit(API_class, project_id, image_id, label_id, class_id, bbox, mask, polygon, z_index=0):
        """ edits an existing label

        Parameters
        ----------
        API_class : class
            hasty.API class
        project_id : str
            id of the project
        image_id : str
            id of the image
        label_id : str
            id of the label
        class_id : str
            id of the label class
        bbox : list [int]
            bounding box coordinates
        mask : list [int]
            mask encoded label
        polygon : list [int]
            polygon label coordinates
        z_index : int
            z position index (Default value = 0)

        Returns
        -------

        """
        json_data = [{
            'id': label_id,
            'class_id': class_id,
            'bbox': bbox,
            'mask': mask,
            'polygon': polygon,
            'z_index': z_index
        }]
        return api_requestor.edit(API_class,
                                  Label.endpoint_image.format(project_id=project_id,
                                                              image_id=image_id),
                                  json_data=json_data)

    @staticmethod
    def delete(API_class, project_id, image_id, label_ids):
        """ deletes every labels in label_ids iterable from the given image

        Parameters
        ----------
        API_class : class
            hasty.API class
        project_id : str
            id of the project
        image_id : str
            image id
        label_ids : iterable
            iterable of label ids

        Returns
        -------
        json
            empty

        """
        if isinstance(label_ids, int):  # if a single ID value is gived, transform it into a list
            label_ids = [label_ids]
        json_data = {
            'labels': [{'label_id': label_id} for label_id in label_ids]
        }
        return api_requestor.delete(API_class,
                                    Label.endpoint_image.format(project_id=project_id,
                                                                image_id=image_id),
                                    json_data=json_data)

    @staticmethod
    def get_total_items_project(API_class, project_id):
        """ gets the number of labels in the given project

        Parameters
        ----------
        API_class : class
            hasty.API class
        project_id : str
            id of the project

        Returns
        -------
        int
            number of items in the project

        """
        return Label.list_project(API_class, project_id, limit=0)['meta']['total']

    @staticmethod
    def get_total_items_image(API_class, project_id, image_id):
        """ gets the number of labels in the given image

        Parameters
        ----------
        API_class : class
            hasty.API class
        project_id : str
            id of the project

        Returns
        -------
        int
            number of items in the image

        """
        return Label.list_image(API_class, project_id, image_id, limit=0)['meta']['total']
