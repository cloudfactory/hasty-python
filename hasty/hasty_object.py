from collections import OrderedDict
from operator import itemgetter


class HastyObject:
    endpoint_uploads = '/v1/projects/{project_id}/uploads'

    def __init__(self, requester, data, obj_params=None):
        self._requester = requester
        self._init_properties()
        self._set_prop_values(data)
        if obj_params:
            self._set_prop_values(obj_params)

    def get__repr__(self, params):
        """
        Converts the object to a nicely printable string.
        """

        def format_params(_params):
            items = list(_params.items())
            if not isinstance(_params, OrderedDict):
                items = sorted(items, key=itemgetter(0), reverse=True)
            for k, v in items:
                if isinstance(v, bytes):
                    v = v.decode("utf-8")
                if isinstance(v, str):
                    v = f'"{v}"'
                yield f"{k}={v}"

        return "{class_name}({params})".format(
            class_name=self.__class__.__name__,
            params=", ".join(list(format_params(params))),
        )

    def _init_properties(self):
        raise NotImplementedError()

    def _set_prop_values(self, data):
        raise NotImplementedError()

    @classmethod
    def _generate_sign_url(cls, requester, project_id):
        data = requester.get(cls.endpoint_uploads.format(project_id=project_id), query_params={"count": 1})
        return data["items"][0]
