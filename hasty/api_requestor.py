import requests


def get(API_class, endpoint, json_data=None):
    """ get request

    Parameters
    ----------
    API_class : class
        hasty.API class
    endpoint : str
        url endpoint
    json_data : dict
        dict of arguments to be passed as query string parameter (Default value = None)

    Returns
    -------
    json
        request result

    """
    return requests.request("GET",
                            API_class.api_base + endpoint,
                            headers=API_class.headers,
                            params=json_data).json()


def post(API_class, endpoint, json_data=None):
    """ post request

    Parameters
    ----------
    API_class : class
        hasty.API class
    endpoint : str
        url endpoint
    json_data :
        dict of arguments to be passed as body parameter (Default value = None)

    Returns
    -------
    json
        request result

    """
    return requests.request("POST",
                            API_class.api_base + endpoint,
                            headers=API_class.headers,
                            json=json_data).json()


def edit(API_class, endpoint, json_data=None):
    """ put request

    Parameters
    ----------
    API_class : class
        hasty.API class
    endpoint : str
        url endpoint
    json_data :
        dict of arguments to be passed as body parameter (Default value = None)

    Returns
    -------
    json
        request result

    """
    return requests.request("PUT",
                            API_class.api_base + endpoint,
                            headers=API_class.headers,
                            json=json_data).json()


def delete(API_class, endpoint, json_data=None):
    """ delete request

    Parameters
    ----------
    API_class : class
        hasty.API class
    endpoint : str
        url endpoint
    json_data :
        dict of arguments to be passed as body parameter (Default value = None)

    Returns
    -------
    json
        request result (empty)


    """
    return requests.request("DELETE",
                            API_class.api_base + endpoint,
                            headers=API_class.headers,
                            json=json_data)
