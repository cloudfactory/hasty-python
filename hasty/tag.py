from collections import OrderedDict

from .exception import LimitExceededException, ValidationException
from .hasty_object import HastyObject
from .tag_class import TagClass


C_TAGS_LIMIT = 100


class Tag(HastyObject):
    endpoint = '/v1/projects/{project_id}/images/{image_id}/tags'

    def __repr__(self):
        return self.get__repr__(OrderedDict({"id": self._id, "tag_class_id": self._tag_class_id,
                                             "tag_class_name": self._tag_class_name, "image_id": self._image_id}))

    @property
    def id(self):
        """
        :type: string
        """
        return self._id

    @property
    def tag_class_id(self):
        """
        :type: string
        """
        return self._tag_class_id

    @property
    def project_id(self):
        """
        :type: string
        """
        return self._project_id

    @property
    def image_id(self):
        """
        :type: string
        """
        return self._image_id

    @property
    def tag_class_name(self):
        """
        :type: string
        """
        return self._tag_class_name

    def _init_properties(self):
        self._id = None
        self._tag_class_id = None
        self._tag_class_name = None
        self._project_id = None
        self._image_id = None

    def _set_prop_values(self, data):
        if "id" in data:
            self._id = data["id"]
        if "tag_class_name" in data:
            self._tag_class_name = data["tag_class_name"]
        if "tag_class_id" in data:
            self._tag_class_id = data["tag_class_id"]
        if "project_id" in data:
            self._project_id = data["project_id"]
        if "image_id" in data:
            self._image_id = data["image_id"]

    @staticmethod
    def _batch_create(requester, project_id, image_id, tags):
        if len(tags) == 0:
            return []
        data = []
        if len(tags) > C_TAGS_LIMIT:
            raise LimitExceededException.max_tags_per_batch(len(tags))
        for tag in tags:
            if isinstance(tag, TagClass):
                data.append({"tag_class_id": tag.id})
            elif "tag_class_id" not in tag:
                raise ValidationException("tag_class_id property should be defined")
            else:
                data.append({"tag_class_id": tag["tag_class_id"]})
        res = requester.post(Tag.endpoint.format(project_id=project_id, image_id=image_id), json_data=data)
        new_tags = []
        for tag in res:
            new_tags.append(Tag(requester, tag, {"project_id": project_id, "image_id": image_id}))
        return new_tags

    @staticmethod
    def _batch_delete(requester, project_id, image_id, tags):
        data = []
        for tag in tags:
            if isinstance(tag, TagClass):
                data.append({"tag_class_id": tag.id})
            elif isinstance(tag, Tag):
                data.append({"tag_id": tag.id})
            elif "tag_class_id" not in tag and "tag_id" not in tag:
                raise ValidationException("tag_class_id or tag_id property should be defined")
            else:
                data.append({"tag_id": tag.get("tag_id"),
                             "tag_class_id": tag.get("tag_class_id")})
        requester.delete(Tag.endpoint.format(project_id=project_id, image_id=image_id), json_data=data)
