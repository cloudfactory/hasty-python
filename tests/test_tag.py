import unittest

from tests.utils import get_client

img_url = "https://images.ctfassets.net/hiiv1w4761fl/6NhZFymLPiX8abIUuEYV7i/c7a63c3a56e7e4f40cfd459c01a10853" \
          "/Untitled_presentation__6_.jpg?w=945&h=494&q=50&fit=fill"


class TestTag(unittest.TestCase):
    def setUp(self):
        self.h = get_client()
        ws = self.h.get_workspaces()
        ws0 = ws[0]
        self.project = self.h.create_project(ws0, "Test Project 1")

    def test_tag_class(self):
        tag_classes = self.project.get_tag_classes()
        self.assertEqual(0, len(tag_classes), 'Should be no tag classes for a new project')
        # Create tag class
        tc = self.project.create_tag_class("class1", 2)
        self.assertEqual(36, len(tc.id), 'Length of the id must be 36')
        self.assertEqual("class1", tc.name)
        self.assertEqual(2, tc.norder)
        # Update tag class
        tc.edit("class2", 3)
        self.assertEqual("class2", tc.name)
        self.assertEqual(3, tc.norder)
        # Check get tag class by id
        tc_copy = self.project.get_tag_class(tc.id)
        self.assertEqual(tc_copy.id, tc.id)
        self.assertEqual(tc_copy.name, tc.name)
        self.assertEqual(tc_copy.norder, tc.norder)
        # Delete tag class
        tag_classes = self.project.get_tag_classes()
        self.assertEqual(1, len(tag_classes), 'Should be one tag class')
        tc.delete()
        tag_classes = self.project.get_tag_classes()
        self.assertEqual(0, len(tag_classes), 'Should not be any tag classes')

    def test_tag(self):
        ds = self.project.create_dataset("ds")
        self.image = self.project.upload_from_url(ds, "tmp1.jpg", img_url, True)
        # Create tag class
        tc1 = self.project.create_tag_class("class1", 1)
        tc2 = self.project.create_tag_class("class2", 2)
        tags = self.image.get_tags()
        self.assertEqual(0, len(tags), 'Should be no tag classes for a new image')
        # Assign by tag class
        self.image.add_tags([tc1])
        tags = self.image.get_tags()
        self.assertEqual(1, len(tags), 'Should be one tag class assigned')
        self.assertEqual(tc1.id, tags[0].tag_class_id, 'Tag class id should match')
        self.assertEqual(tc1.name, tags[0].tag_class_name, 'Tag class id should match')
        # Assign by tag class id
        self.image.add_tags([{"tag_class_id": tc2.id}])
        tags = self.image.get_tags()
        self.assertEqual(2, len(tags), 'Should be two tag class assigned')
        # Assign same classes
        self.image.add_tags([tc1, tc2])
        original_tags = self.image.get_tags()
        self.assertEqual(2, len(original_tags), 'Still should be two tag class assigned')
        # Delete one tag
        self.image.delete_tags([original_tags[0]])
        tags = self.image.get_tags()
        self.assertEqual(1, len(tags), 'Should be one tag class assigned')
        # Delete another tag by tag_class
        self.image.delete_tags([tc1, tc2])
        tags = self.image.get_tags()
        self.assertEqual(0, len(tags), 'Should not be any tags assigned')
        # Assign same classes
        tags = self.image.add_tags([tc1, tc2])
        self.assertEqual(2, len(tags), 'Should be two tag class assigned')
        # Delete via object: tag_class_id
        self.image.delete_tags([{"tag_class_id": tc1.id}])
        tags = self.image.get_tags()
        self.assertEqual(1, len(tags), 'Should be one tag class assigned')
        # Delete via object: tag_id
        self.image.delete_tags([{"tag_id": tag.id} for tag in tags])
        tags = self.image.get_tags()
        self.assertEqual(0, len(tags), 'Should not be any tags assigned')

    def tearDown(self) -> None:
        projects = self.h.get_projects()
        for p in projects:
            p.delete()


if __name__ == '__main__':
    unittest.main()
