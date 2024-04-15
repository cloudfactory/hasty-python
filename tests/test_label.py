import unittest

from tests.utils import get_client

img_url = "https://images.ctfassets.net/hiiv1w4761fl/6NhZFymLPiX8abIUuEYV7i/c7a63c3a56e7e4f40cfd459c01a10853" \
          "/Untitled_presentation__6_.jpg?w=945&h=494&q=50&fit=fill"


class TestLabel(unittest.TestCase):
    def setUp(self):
        self.h = get_client()
        ws = self.h.get_workspaces()
        ws0 = ws[0]
        self.project = self.h.create_project(ws0, "Test Project 1")
        ds = self.project.create_dataset("ds")
        self.image = self.project.upload_from_url(ds, "tmp1.jpg", img_url, True)
        self.label_class = self.project.create_label_class("Label class")
        self.label_class2 = self.project.create_label_class("Label class 2")

    def validate_label_object(self, label, class_id, bbox, polygon, mask, z_index):
        self.assertEqual(class_id, label.class_id)
        self.assertEqual(bbox, label.bbox)
        self.assertEqual(polygon, label.polygon)
        self.assertEqual(mask, label.mask)
        self.assertEqual(z_index, label.z_index)

    def test_label(self):
        labels = self.image.get_labels()
        self.assertEqual(0, len(labels))
        # Create label
        bbox = [10, 10, 50, 50]
        poly = [[10, 20], [20, 44], [10, 15]]
        z_index = 3
        label = self.image.create_label(self.label_class, bbox, poly, z_index=z_index)
        self.validate_label_object(label, self.label_class.id, bbox, poly, None, z_index)
        labels = self.image.get_labels()
        self.assertEqual(1, len(labels))
        self.validate_label_object(labels[0], self.label_class.id, bbox, poly, None, z_index)
        # Edit label
        bbox2 = [b + 5 for b in bbox]
        poly2 = None
        mask2 = [1, 10, 20, 3]
        z_index2 = 4
        label.edit(self.label_class2, bbox2, poly2, mask2, z_index2)
        self.validate_label_object(label, self.label_class2.id, bbox2, poly2, mask2, z_index2)
        labels = self.image.get_labels()
        self.assertEqual(1, len(labels))
        self.validate_label_object(labels[0], self.label_class2.id, bbox2, poly2, mask2, z_index2)
        # Bulk edit labels
        labels = self.image.edit_labels([{"label_id": label.id, "class_id": self.label_class.id, "bbox": bbox,
                                          "polygon": poly, "mask": None, "z_index": z_index} for label in labels])
        self.validate_label_object(labels[0], self.label_class.id, bbox, poly, None, z_index)
        # Delete label
        label.delete()
        labels = self.image.get_labels()
        self.assertEqual(0, len(labels))

    def test_external_id_for_label(self):
        # Create label
        bbox = [10, 10, 50, 50]
        poly = [[10, 20], [20, 44], [10, 15]]
        z_index = 3
        label = self.image.create_label(self.label_class, bbox, poly, z_index=z_index, external_id="ext_id_1")
        self.assertEqual("ext_id_1", label.external_id)
        labels = self.image.get_labels()
        self.assertEqual(1, len(labels))
        self.assertEqual("ext_id_1", labels[0].external_id)
        # Edit label

        label.edit(self.label_class2, bbox, poly, external_id="ext_id_2")
        self.assertEqual("ext_id_2", label.external_id)
        labels = self.image.get_labels()
        self.assertEqual(1, len(labels))
        self.assertEqual("ext_id_2", labels[0].external_id)

    def tearDown(self) -> None:
        projects = self.h.get_projects()
        for p in projects:
            p.delete()


if __name__ == '__main__':
    unittest.main()
