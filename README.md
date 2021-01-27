# hasty-python
Python library for the Hasty API.

## deployement to PyPi (pip)
* python setup.py sdist
* pip install twine
* twine upload dist/*
* [enter username and password]

## installation (github)
* git pull https://github.com/hasty-ai/hasty-python.git
* cd hasty-python
* pip install -e . 

## installation (pip)
* pip install hasty_python

## Usage

```
from hasty import Client

API_KEY = "your_key"
h = Client(api_key=API_KEY,
           base_url='https://api.kp.none.kp.dev.hasty.ai')

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