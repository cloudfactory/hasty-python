class PaginatedList:

    def __init__(self, content_class, requester, endpoint, obj_params=None):
        self.content_class = content_class
        self.requester = requester
        self.offset = 0
        self.limit = 100
        query_params = {
            'offset': self.offset,
            'limit': self.limit
        }
        self.data = self.requester.get(endpoint, query_params)
        self.total_count = self.data['meta']['total']
        self.items = self.data['items']
        self.instances = [content_class(self.requester, cc, obj_params) for cc in self.items]
        self.has_more = self.total_count > self.limit

    def __repr__(self):
        # TODO Add current size and total number if needed
        return str([str(i) for i in self.instances])

    def __getitem__(self, idx):
        # TODO Check idx and fetch next batch if needed
        return self.instances[idx]

    def __len__(self):
        return self.total_count
