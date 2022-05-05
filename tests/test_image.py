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
        # Download image
        images[1].download(images[1].name)
        self.assertTrue(os.path.exists(images[1].name), "Image doesnt exists after download")
        # Delete dataset
        ds.delete()

    def test_image_filters_and_status(self):
        ds2 = self.project.create_dataset("ds2")
        self.project.upload_from_url(ds2, "tmp1.jpg", img_url, True)
        img2 = self.project.upload_from_url(ds2, "tmp2.jpg", img_url, True)
        ds3 = self.project.create_dataset("ds3")
        img3 = self.project.upload_from_url(ds3, "tmp3.jpg", img_url, True)
        img2.set_status("TO REVIEW")
        img3.set_status("DONE")
        # Check total number of images
        images = self.project.get_images()
        self.assertEqual(3, len(images))
        # Filter by status DONE
        images = self.project.get_images(image_status="DONE")
        self.assertEqual(1, len(images))
        # Filter by status DONE, TO REVIEW
        images = self.project.get_images(image_status=["DONE", "TO REVIEW"])
        self.assertEqual(2, len(images))
        # Filter by status and dataset
        images = self.project.get_images(dataset=ds3, image_status=["DONE", "TO REVIEW"])
        self.assertEqual(1, len(images))
        # Filter by datasets
        images = self.project.get_images(dataset=[ds2, ds3])
        self.assertEqual(3, len(images))
        # Delete dataset
        ds2.delete()
        ds3.delete()

    def test_image_rename_move_delete(self):
        ds2 = self.project.create_dataset("ds2")
        ds3 = self.project.create_dataset("ds3")
        self.project.upload_from_url(ds2, "tmp1.jpg", img_url, True)
        # Check image name
        images = self.project.get_images()
        image = images[0]
        self.assertEqual("tmp1.jpg", image.name)
        # Check rename feature
        image.rename("tmp2.jpg")
        self.assertEqual("tmp2.jpg", image.name)
        # Check move feature
        image.move(ds3)
        self.assertEqual(ds3.name, image.dataset_name)
        # Check delete
        image.delete()
        images = self.project.get_images()
        self.assertEqual(0, len(images))

    def test_external_ids(self):
        ds2 = self.project.create_dataset("dsE")
        img = self.project.upload_from_url(ds2, "tmp1.jpg", img_url, True, "EXTERNAL_ID")
        self.assertEqual("EXTERNAL_ID", img.external_id)
        images = self.project.get_images()
        image = images[0]
        self.assertEqual("EXTERNAL_ID", image.external_id)
        image.delete()

    def tearDown(self) -> None:
        projects = self.h.get_projects()
        for i in ["image.jpg", "tmp1.jpg"]:
            if os.path.exists(i):
                os.remove(i)
        for p in projects:
            p.delete()


if __name__ == '__main__':
    unittest.main()
