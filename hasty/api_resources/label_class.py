from __future__ import absolute_import, division, print_function

from .. import api_requestor


endpoint = '/v1/projects/{project_id}/label_classes'


class LabelClass:
    
    @staticmethod
    def list(project_id):
        return api_requestor.get(endpoint.format(project_id=project_id))

    @staticmethod
    def create(project_id, class_name, color='#49D3404D', class_type='object'):
        return api_requestor.post(endpoint.format(project_id=project_id),
                                  json_data={'class_name': class_name,
                                             'class_type': class_type,
                                             'color': color})

    @staticmethod
    def delete(project_id, label_class_id):
        delete_endpoint = f'{endpoint.format(project_id=project_id)}/{label_class_id}'
        return api_requestor.delete(delete_endpoint)


attributes_endpoint = '/v1/projects/{project_id}/label_classes/{class_id}/attributes'


class LabelClassAttribute:

    @staticmethod
    def list(project_id, class_id):
        return api_requestor.get(attributes_endpoint.format(project_id=project_id,
                                                            class_id=class_id))

    @staticmethod
    def create(project_id, class_id, attribute_name, attribute_type, description=None):
        return api_requestor.post(attributes_endpoint.format(project_id=project_id,
                                                             class_id=class_id),
                                  json_data={'attribute_name': attribute_name,
                                             'attribute_type': attribute_type,
                                             'description': description})


lov_endpoint = '/v1/projects/{project_id}/attributes/{attribute_id}/lov'


class LabelAttributeLOV:

    @staticmethod
    def list(project_id, attribute_id):
        return api_requestor.get(lov_endpoint.format(project_id=project_id,
                                                     attribute_id=attribute_id))

    @staticmethod
    def create(project_id, attribute_id, value):
        return api_requestor.post(lov_endpoint.format(project_id=project_id,
                                                      attribute_id=attribute_id),
                                  json_data={'value': value})
