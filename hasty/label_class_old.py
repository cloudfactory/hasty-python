from __future__ import absolute_import, division, print_function

from . import api_requestor


class LabelClass:
    """Class that contains some basic requests and features for label classes."""
    endpoint = '/v1/projects/{project_id}/label_classes'
    endpoint_class = '/v1/projects/{project_id}/label_classes/{label_class_id}'

    @staticmethod
    def list(API_class, project_id, offset=0, limit=100):
        """ fetches a list of label classes from a project given the offset and limit params

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
            label class objects

        """
        json_data = {
            'offset': offset,
            'limit': limit
        }
        return api_requestor.get(API_class,
                                 LabelClass.endpoint.format(
                                     project_id=project_id),
                                 json_data=json_data)

    @staticmethod
    def fetch_all(API_class, project_id):
        """ fetches every label classes from a project

        Parameters
        ----------
        API_class : class
            hasty.API class
        project_id : str
            id of the project

        Returns
        -------
        list [dict]
            label class objects
        """
        tot = []
        n = LabelClass.get_total_items(API_class, project_id)
        for offset in range(0, n, 100):
            tot += LabelClass.list(API_class, project_id,
                                   offset=offset)['items']
        return tot

    @staticmethod
    def create(API_class, project_id, class_name, class_type, color='#49D3404D'):
        """ creates a new label class

        Parameters
        ----------
        API_class : class
            hasty.API class
        project_id : str
            id of the project
        class_name : str
            name of the label class
        class_type : str
            type of the label class
        color : str
            color of the label class (Default value = '#49D3404D')

        Returns
        -------
        dict
            label class object

        """
        json_data = {
            'name': class_name,
            'type': class_type,
            'color': color
        }
        return api_requestor.post(API_class,
                                  LabelClass.endpoint.format(
                                      project_id=project_id),
                                  json_data=json_data)

    @staticmethod
    def copy(API_class, project_id, item_to_copy):
        """ copies a label class object to the project

        Parameters
        ----------
        API_class : class
            hasty.API class
        project_id : str
            id of the project
        item_to_copy : dict
            label class object to copy

        Returns
        -------
        dict
            label class object

        """
        json_data = {
            'name': item_to_copy['name'],
            'color': item_to_copy['color'],
            'type': item_to_copy['type'],
            'norder': item_to_copy['norder'],
            'icon_url': item_to_copy['icon_url'],
            'parent_id': item_to_copy['parent_id'],
            'removable': item_to_copy['removable']
        }
        return api_requestor.post(API_class,
                                  LabelClass.endpoint.format(
                                      project_id=project_id),
                                  json_data=json_data)

    @staticmethod
    def edit(API_class, project_id, label_class_id, name, type, color=None, icon_url=None, norder=None):
        """ edits an existing label class

        Parameters
        ----------
        API_class : class
            hasty.API class
        project_id : str
            id of the project
        label_class_id : str
            id of the label class to edit
        name : str
            name of the label class
        type : str
            type of the label class
        color : str
            color of the label class (Default value = None)
        icon_url : url
            icon url of the label class (Default value = None)
        norder : int
            order number of the label class (Default value = None)

        Returns
        -------
        dict
            label class object

        """
        json_data = {
            'name': name,
            'type': type,
            'color': color,
            'icon_url': icon_url,
            'norder': norder
        }
        return api_requestor.edit(API_class,
                                  LabelClass.endpoint_class.format(project_id=project_id,
                                                                   label_class_id=label_class_id),
                                  json_data=json_data)

    @staticmethod
    def delete_class(API_class, project_id, label_class_id):
        """ deletes the given label class from the project

        Parameters
        ----------
        API_class : class
            hasty.API class
        project_id : str
            id of the project
        label_class_id :str
            id of the label class

        Returns
        -------
        json
            empty

        """
        return api_requestor.delete(API_class,
                                    LabelClass.endpoint_class.format(project_id=project_id,
                                                                     label_class_id=label_class_id))

    @staticmethod
    def delete_all(API_class, project_id):
        """ deletes every label classes in the project

        Parameters
        ----------
        API_class : class
            hasty.API class
        project_id : str
            id of the project

        Returns
        -------
        list[json]
            empty

        """
        label_classes = LabelClass.fetch_all(API_class, project_id)
        label_class_ids = [label_class['id'] for label_class in label_classes]
        return [LabelClass.delete_class(API_class, project_id, label_class_id) for label_class_id in label_class_ids]

    @staticmethod
    def get_total_items(API_class, project_id):
        """ gets the number of label classes in the given project

        Parameters
        ----------
        API_class : class
            hasty.API class
        project_id : str
            id of the project

        Returns
        -------
        int
            number of items
        """
        return LabelClass.list(API_class, project_id, limit=0)['meta']['total']
