# Python library for the Hasty API.
[![PyPI version](https://badge.fury.io/py/hasty.svg)](https://badge.fury.io/py/hasty)
[![Documentation Status](https://readthedocs.org/projects/hasty/badge/?version=latest)](https://hasty.readthedocs.io/en/latest/?badge=latest)
![CI](https://github.com/hasty-ai/hasty-python/workflows/CI/badge.svg)


## Installation
```
 pip install hasty
```

## Usage Example

Establish initial connection with Hasty:
``` python
from hasty import Client

API_KEY = "your_key"
h = Client(api_key=API_KEY)
```

Get projects
``` python

projects = h.get_projects()
print(projects)
>> ['Project(id="9a5ac730-9b08-477d-8f20-e7245baf0e29", name="African Wildlife")']
```

Create dataset
``` python
buffalo_ds = project.create_dataset("buffalo")
print(buffalo_ds)
>> Dataset(id="66ee13d5-aaf7-4fac-862c-45f44eff802a", name="buffalo")
```

Upload image
``` python
img = project.upload_from_file(buffalo_ds,
                               "./buffalo/001.jpg")
print(img)
>> Image(id="ebf88007-134b-4bce-9799-995504b2b0ee", dataset_name="buffalo", name="001.jpg")
```

For more information check our [documentation](https://hasty.readthedocs.io/en/latest/)
