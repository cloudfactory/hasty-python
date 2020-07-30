import hasty

# quick example to retreive the project list
# and read the first 100 images from the first project in list

my_API = hasty.API(api_key="enter here your Key",
                   api_base="https://api.staging.dev.hasty.ai")

# retreive the first 50 images from the project
project_list = hasty.Project.fetch_all(my_API)
print(project_list)

project_id = project_list["items"][0]["id"]

# retreive the first 50 images from the project
images_list = hasty.Image.list(my_API, project_id, offset=0, limit=50)
print(images_list)
