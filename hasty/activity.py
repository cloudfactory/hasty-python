from collections import OrderedDict

from .exception import ValidationException
from .hasty_object import HastyObject


class ActivityType(HastyObject):
    endpoint = '/v1/projects/{project_id}/activity_types'
    endpoint_class = '/v1/projects/{project_id}/activity_types/{activity_type_id}'

    def __repr__(self):
        return self.get__repr__(OrderedDict({"id": self._id, "name": self._name, "color": self._color}))

    @property
    def id(self):
        """
        :type: string
        """
        return self._id

    @property
    def name(self):
        """
        :type: string
        """
        return self._name

    @property
    def project_id(self):
        """
        :type: string
        """
        return self._project_id

    @property
    def color(self):
        """
        :type: string
        """
        return self._color

    def _init_properties(self):
        self._id = None
        self._name = None
        self._project_id = None
        self._color = None

    def _set_prop_values(self, data):
        if "id" in data:
            self._id = data["id"]
        if "name" in data:
            self._name = data["name"]
        if "project_id" in data:
            self._project_id = data["project_id"]
        if "color" in data:
            self._color = data["color"]

    @classmethod
    def _create(cls, requester, project_id, name, color=None):
        res = requester.post(cls.endpoint.format(project_id=project_id),
                             json_data={"name": name,
                                        "color": color})
        return cls(requester, res, {"project_id": project_id})

    def edit(self, name, color=None):
        """
        Edit activity type properties

        Arguments:
            name (str): Label class name
            color (str, optional): Color in HEX format #0f0f0faa
        """
        self._requester.put(self.endpoint_class.format(project_id=self._project_id, activity_type_id=self._id),
                            json_data={"name": name, "color": color})
        self._name = name
        self._color = color

    def delete(self):
        """
        Delete activity type
        """
        self._requester.delete(self.endpoint_class.format(project_id=self._project_id, activity_type_id=self._id))


class Activity(HastyObject):
    endpoint = '/v1/projects/{project_id}/videos/{video_id}/segments'
    endpoint_class = '/v1/projects/{project_id}/segments/{segment_id}'

    def __repr__(self):
        return self.get__repr__(OrderedDict({"id": self._id, "activities": self._activities,
                                             "start": self._start_time_ms, "end": self._end_time_ms}))

    @property
    def id(self):
        """
        :type: string
        """
        return self._id

    @property
    def video_id(self):
        """
        :type: string
        """
        return self._video_id

    @property
    def activities(self):
        """
        :type: list
        """
        return self._activities

    @property
    def start_time_ms(self):
        """
        :type: int
        """
        return self._start_time_ms

    @property
    def end_time_ms(self):
        """
        :type: int
        """
        return self._end_time_ms

    def _init_properties(self):
        self._id = None
        self._video_id = None
        self._activities = None
        self._start_time_ms = None
        self._end_time_ms = None
        self._project_id = None

    def _set_prop_values(self, data):
        if "id" in data:
            self._id = data["id"]
        if "video_id" in data:
            self._video_id = data["video_id"]
        if "activities" in data:
            self._activities = data["activities"]
        if "start_time_ms" in data:
            self._start_time_ms = data["start_time_ms"]
        if "end_time_ms" in data:
            self._end_time_ms = data["end_time_ms"]
        if "project_id" in data:
            self._project_id = data["project_id"]

    @classmethod
    def _create(cls, requester, project_id, video_id, activities,
                start_time_ms, end_time_ms, replace_overlap=False):
        if len(activities) == 0 or not isinstance(activities, list):
            raise ValidationException.invalid_activities()
        type_ids = []
        for a in activities:
            if isinstance(a, ActivityType):
                type_ids.append(a.id)
            elif isinstance(a, str):
                type_ids.append(a)
            else:
                raise ValidationException.invalid_activities()
        query_params = None
        if replace_overlap:
            query_params = {"replace_overlap": replace_overlap}
        res = requester.post(cls.endpoint.format(project_id=project_id, video_id=video_id),
                             json_data={"activities": type_ids,
                                        "start_time_ms": start_time_ms,
                                        "end_time_ms": end_time_ms},
                             query_params=query_params)
        return cls(requester, res, {"project_id": project_id})

    def delete(self):
        """
        Delete activity
        """
        self._requester.delete(self.endpoint_class.format(project_id=self._project_id, segment_id=self._id))

    def edit(self, start_time_ms, end_time_ms, activities):
        """
        Edit activity properties

        Arguments:
            start_time_ms (int): Start time in milliseconds
            end_time_ms (int): End time in milliseconds
            activities (list): List of `~hasty.ActivityType` or `str` (IDs)
        """
        if len(activities) == 0 or not isinstance(activities, list):
            raise ValidationException.invalid_activities()
        type_ids = []
        for a in activities:
            if isinstance(a, ActivityType):
                type_ids.append(a.id)
            elif isinstance(a, str):
                type_ids.append(a)
            else:
                raise ValidationException.invalid_activities()
        res = self._requester.put(self.endpoint_class.format(project_id=self._project_id, segment_id=self._id),
                                  json_data={"activities": type_ids,
                                             "start_time_ms": start_time_ms,
                                             "end_time_ms": end_time_ms})
        self._set_prop_values(res)
        return Activity(self._requester, res, {"project_id": self._project_id})
