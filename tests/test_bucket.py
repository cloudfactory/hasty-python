import unittest

from utils import get_client

from hasty.bucket import S3Creds


class TestBucketManagement(unittest.TestCase):
    def setUp(self):
        self.h = get_client()

    def test_bucket_creation(self):
        ws = self.h.get_workspaces()[0]
        creds = S3Creds()
        creds.bucket = "hasty-public-bucket-mounter"
        creds.role = "arn:aws:iam::045521589961:role/hasty-public-bucket-mounter"
        res = ws.create_bucket("test_bucket", creds)
        self.assertIsNotNone(res.id)
        self.assertEqual("test_bucket", res.name)
        self.assertEqual("s3", res.cloud_provider)


if __name__ == '__main__':
    unittest.main()
