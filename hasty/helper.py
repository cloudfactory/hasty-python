class PaginatedList:

    def __init__(self, content_class, requester, endpoint, obj_params=None, query_params=None):
        self.content_class = content_class
        self.requester = requester
        self.offset = 0
        self.limit = 100
        self.query_params = query_params if query_params else dict()
        self.query_params['offset'] = self.offset
        self.query_params['limit'] = self.limit
        self.endpoint = endpoint
        self.obj_params = obj_params
        data = self.requester.get(endpoint, self.query_params)
        self.total_count = data['meta']['total']
        self.items = data['items']
        self.offset = len(self.items)
        self.instances = [content_class(self.requester, cc, obj_params) for cc in self.items]
        self.has_more = self.total_count > self.limit

    def __repr__(self):
        # TODO Add current size and total number if needed
        return str([str(i) for i in self.instances])

    def __getitem__(self, idx):
        # Check idx and fetch next batch if needed
        while len(self.items) <= idx < self.total_count:
            self.query_params['offset'] = self.offset
            new_data = self.requester.get(self.endpoint, self.query_params)
            self.items.extend(new_data["items"])
            self.instances.extend([self.content_class(self.requester, cc, self.obj_params) for cc in new_data["items"]])
            self.total_count = new_data['meta']['total']
            self.offset = len(self.items)
        return self.instances[idx]

    def __len__(self):
        return self.total_count
