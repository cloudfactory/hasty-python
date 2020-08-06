import uuid


class API:
    """Class that will be passed to every functions that you call."""

    def __init__(self, api_key, api_base='https://api.hasty.ai'):
        """
        Parameters:
            api_key (string): your hasty API key
            api_base (string): base link of the API
        """
        if isinstance(api_key, str):
            self.api_key = api_key
        else:
            raise ValueError(
                f'API key should be a string, not: {type(api_key)}')

        # if isinstance(last_state_ui, str):
        #     self.last_state_ui = last_state_ui
        # else:
        #     raise ValueError(
        #         f'last state should be a string, not: {type(last_state_ui)}')

        if isinstance(api_key, str):
            self.api_base = api_base
        else:
            raise ValueError(
                f'API base link should be a string, not: {type(api_base)}')

        self.headers = {
            'accept': 'application/json',
            'X-Api-Key': self.api_key,
            'X-Session-Id': str(uuid.uuid4())
        }
