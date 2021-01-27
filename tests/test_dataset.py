import unittest

from tests.utils import get_client


class TestDataset(unittest.TestCase):
    def setUp(self):
        self.h = get_client()
        ws = self.h.get_workspaces()
        ws0 = ws[0]
        self.project = self.h.create_project(ws0, "Test Project 1")

    def test_dataset(self):
        datasets = self.project.get_datasets()
        self.assertEqual(0, len(datasets), 'Should be no datasets for a new project')
        # Create dataset
        ds = self.project.create_dataset("DS1", 1)
        self.assertEqual(36, len(ds.id), 'Length of the id must be 36')
        self.assertEqual("DS1", ds.name)
        # Update dataset
        ds.edit("DS2", 2)
        self.assertEqual("DS2", ds.name)
        self.assertEqual(2, ds.norder)
        # Check get dataset by id
        ds_copy = self.project.get_dataset(ds.id)
        self.assertEqual(ds_copy.id, ds.id)
        self.assertEqual(ds_copy.name, ds.name)
        self.assertEqual(ds_copy.norder, ds.norder)
        # Delete dataset
        datasets = self.project.get_datasets()
        self.assertEqual(1, len(datasets), 'Should be one dataset')
        ds.delete()
        datasets = self.project.get_datasets()
        self.assertEqual(0, len(datasets), 'Should not be any datasets')

    def tearDown(self) -> None:
        projects = self.h.get_projects()
        for p in projects:
            p.delete()


if __name__ == '__main__':
    unittest.main()
