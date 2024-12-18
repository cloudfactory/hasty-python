import unittest

from tests.utils import get_client

from hasty.bucket import S3Creds


class TestBucketManagement(unittest.TestCase):
    def setUp(self):
        self.h = get_client()
        self.workspace = self.h.get_workspaces()[0]
        self.project = self.h.create_project(self.workspace, "Test Project 1")

    def tearDown(self):
        self.project.delete()

    def test_bucket_creation(self):
        ws = self.h.get_workspaces()[0]
        creds = S3Creds()
        creds.bucket = "hasty-public-bucket-mounter"
        creds.role = "arn:aws:iam::045521589961:role/hasty-public-bucket-mounter"
        res = ws.create_bucket("test_bucket", creds)
        self.assertIsNotNone(res.id)
        self.assertEqual("test_bucket", res.name)
        self.assertEqual("s3", res.cloud_provider)

    def test_import_image(self):
        creds = S3Creds()
        creds.bucket = "hasty-public-bucket-mounter"
        creds.role = "arn:aws:iam::045521589961:role/hasty-public-bucket-mounter"
        bucket = self.workspace.create_bucket("test_bucket", creds)
        bucket_id = bucket.id

        # Test import image
        dataset = self.project.create_dataset("ds2")
        img = self.project.upload_from_bucket(dataset, "1645001880-075718046bb2fbf9b8c35d6e88571cd7f91ca1a1.png", "dummy/1645001880-075718046bb2fbf9b8c35d6e88571cd7f91ca1a1.png", bucket_id)
        self.assertEqual("1645001880-075718046bb2fbf9b8c35d6e88571cd7f91ca1a1.png", img.name)
        self.assertEqual("ds2", img.dataset_name)
        self.assertIsNotNone(img.id)
        self.assertEqual(1280, img.width)
        self.assertEqual(720, img.height)


if __name__ == '__main__':
    unittest.main()
