Quick Start
===========

Authentication
^^^^^^^^^^^^^^
In order to communicate with your Hasty server via the API, you must provide valid API Key. The Key can be generated on Edit Workspace page (Hasty -> Edit Workspace -> API Accounts)

You will need to create a service account, define it's role and finally generate API Key:

.. image:: img/edit_workspace.png


Create a Hasty API Client instance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This example shows how to create establish your initial connection to Hasty:

::

    from hasty import Client

    API_KEY = "bNZ09SA2hFSZGHa6jfMK2Ywo7GoActTXNCvJR1wEkVDtKvl9EMTLRvknwmwUz7Hjl1jPwxYBkyGF8BcWV3y9rg"

    h = Client(api_key=API_KEY)


Managing projects
^^^^^^^^^^^^^^^^^

Below you can find an example of how the projects can be created, retrieved, updated or removed. Please note, that every project should belong to some workspace.

::

    # Get workspaces that the user account can have access to
    workspaces = h.get_workspaces()
    print(workspaces)
    >> ['Workspace(id="57d9a50e-73a2-47c5-a130-a652fa98d244", name="Hasty Python Library Workspace")']

    # Create new project
    default_workspace = workspaces[0]
    new_project = h.create_project(workspace = default_workspace,
                               name = "My Awesome Project",
                               description = "Awesome description")
    print(new_project)
    >> Project(id="75472e11-d6f2-403c-80f6-f0fc83c97041", name="My Awesome Project")

    # Get Projects
    print(h.get_projects())
    >> ['Project(id="75472e11-d6f2-403c-80f6-f0fc83c97041", name="My Awesome Project")']

    # Get project by id
    h.get_project(new_project.id)
    >> Project(id="75472e11-d6f2-403c-80f6-f0fc83c97041", name="My Awesome Project")

    # Edit project
    new_project.edit(name="Super Awesome Project", description="Amazing description")

    # Delete project
    new_project.delete()


Managing images
^^^^^^^^^^^^^^^

Images in hasty stored in datasets. Similar to folders on your computer, every image should have a unique image name inside the dataset.
You can upload image from local file or using url.

::

    # Create dataset
    train_dataset = new_project.create_dataset("train")
    print(train_dataset)
    >> Dataset(id="7a55886d-e695-4693-9a3d-7addd75c5e74", name="train")

    # Upload image from file
    image = new_project.upload_from_file(dataset=train_dataset,
                                         filepath='../Datasets/African Wildlife/rhino/001.jpg')
    print(image)
    >> Image(id="b58860f1-8da0-4c94-bff7-b7476c3c8f50", dataset_name="train", name="001.jpg")

    # Upload from URL
    image = new_project.upload_from_url(dataset=train_dataset,
                                        filename='4.jpg',
                                        url='https://www.gstatic.com/webp/gallery/4.jpg')
    print(image)
    >> Image(id="2dae09ce-ca8a-416f-90e2-a4024515ae95", dataset_name=None, name="4.jpg")

    # Retrieve the list of projects images
    images = new_project.get_images()
    print(images)
    >> ['Image(id="b58860f1-8da0-4c94-bff7-b7476c3c8f50", dataset_name="train", name="001.jpg")',
        'Image(id="2dae09ce-ca8a-416f-90e2-a4024515ae95", dataset_name="train", name="4.jpg")']


Managing label classes
^^^^^^^^^^^^^^^^^^^^^^

Every label in hasty should belongs to some label class.

::

    # Create label classes
    rhino_class = new_project.create_label_class(name="rhino", color="#6a3d9a", class_type="object")
    sky_class = new_project.create_label_class(name="sky", color="#6a3d9a", class_type="background")

    # Edit label class
    sky_class.edit(name="sky", color="#f0e928", class_type="background")

    # Get label classes
    label_classes = new_project.get_label_classes()
    print(label_classes)
    >> ['LabelClass(id="1201c994-c0dc-4efa-9892-f9d030320c5d", name="rhino", color="#6a3d9a", type="object", norder=10.0)',
        'LabelClass(id="2c8097bc-6dbf-4753-9485-683aff6171f9", name="sky", color="#f0e928", type="background", norder=11.0)']

    # Delete label class
    sky_class.delete()



Managing labels
^^^^^^^^^^^^^^^


::

    # Create label
    image.create_label(label_class=rhino_class, bbox=[20, 30, 300, 400])
    lbl.edit(label_class=rhino_class, bbox=[120, 130, 300, 400])
    lbl.delete()
