import unittest

from tests.utils import get_client


class TestLabelClass(unittest.TestCase):
    def setUp(self):
        self.h = get_client()
        ws = self.h.get_workspaces()
        ws0 = ws[0]
        self.project = self.h.create_project(ws0, "Test Project 1")

    def test_label_class(self):
        label_classes = self.project.get_label_classes()
        self.assertEqual(0, len(label_classes), 'Should be no label classes for a new project')
        # Create label class
        lc = self.project.create_label_class("class1", "#ff00aa99", "object", 2)
        self.assertEqual(36, len(lc.id), 'Length of the id must be 36')
        self.assertEqual("class1", lc.name)
        self.assertEqual("#ff00aa99", lc.color)
        self.assertEqual("object", lc.class_type)
        self.assertEqual(2, lc.norder)
        # Update dataset
        lc.edit("class2", "#ff88aa99", "background", 3)
        self.assertEqual("class2", lc.name)
        self.assertEqual("#ff88aa99", lc.color)
        self.assertEqual("background", lc.class_type)
        self.assertEqual(3, lc.norder)
        # Check get label class by id
        lc_copy = self.project.get_label_class(lc.id)
        self.assertEqual(lc_copy.id, lc.id)
        self.assertEqual(lc_copy.name, lc.name)
        self.assertEqual(lc_copy.color, lc.color)
        self.assertEqual(lc_copy.class_type, lc.class_type)
        self.assertEqual(lc_copy.norder, lc.norder)
        # Delete label class
        label_classes = self.project.get_label_classes()
        self.assertEqual(1, len(label_classes), 'Should be one label class')
        lc.delete()
        label_classes = self.project.get_label_classes()
        self.assertEqual(0, len(label_classes), 'Should not be any label classes')

    def test_external_id(self):
        # Create label class
        lc = self.project.create_label_class("class1", "#ff00aa99", "object", 2, external_id="ext_id_1")
        self.assertEqual("ext_id_1", lc.external_id)
        # Check DB
        lc_copy = self.project.get_label_class(lc.id)
        self.assertEqual("ext_id_1", lc_copy.external_id)
        # Update
        lc.edit("class2", "#ff88aa99", "background", 3, external_id="ext_id_2")
        self.assertEqual("ext_id_2", lc.external_id)
        # Check DB
        lc_copy = self.project.get_label_class(lc.id)
        self.assertEqual("ext_id_2", lc_copy.external_id)

    def tearDown(self) -> None:
        projects = self.h.get_projects()
        for p in projects:
            p.delete()


if __name__ == '__main__':
    unittest.main()
