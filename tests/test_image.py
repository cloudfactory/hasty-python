import os
import unittest
import urllib.request

from tests.utils import get_client, img_url

class TestImage(unittest.TestCase):
    def setUp(self):
        self.h = get_client()
        ws = self.h.get_workspaces()
        ws0 = ws[0]
        self.project = self.h.create_project(ws0, "Test Project 1")
        urllib.request.urlretrieve(img_url, "image.jpg")

    def test_image(self):
        ds = self.project.create_dataset("ds")
        # Test upload from file
        self.project.upload_from_file(ds, "image.jpg")
        images = self.project.get_images()
        self.assertEqual(1, len(images))
        self.assertEqual("image.jpg", images[0].name)
        # Upload from url
        self.project.upload_from_url(ds, "tmp1.jpg", img_url, True)
        images = self.project.get_images()
        self.assertEqual(2, len(images))
        self.assertIn(images[0].name, ("image.jpg", "tmp1.jpg"))
        self.assertIn(images[1].name, ("image.jpg", "tmp1.jpg"))

    def tearDown(self) -> None:
        projects = self.h.get_projects()
        if os.path.exists("image.jpg"):
            os.remove("image.jpg")
        for p in projects:
            p.delete()


if __name__ == '__main__':
    unittest.main()
