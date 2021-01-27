# Python library for the Hasty API.
[![PyPI version](https://badge.fury.io/py/hasty.svg)](https://badge.fury.io/py/hasty)

## Installation
```
 git pull hasty
```

## Usage

```
from hasty import Client

API_KEY = "your_key"
h = Client(api_key=API_KEY)

projects = h.get_projects()
print(projects)
>> ['Project(id="9a5ac730-9b08-477d-8f20-e7245baf0e29", name="African Wildlife")']

buffalo_ds = project.create_dataset("buffalo")
print(buffalo_ds)
>> Dataset(id="66ee13d5-aaf7-4fac-862c-45f44eff802a", name="buffalo")


img = project.upload_from_file(buffalo_ds,
                               "./buffalo/001.jpg")
print(img)
>> Image(id="ebf88007-134b-4bce-9799-995504b2b0ee", dataset_name="buffalo", name="001.jpg")
```
