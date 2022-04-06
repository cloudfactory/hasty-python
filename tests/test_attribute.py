import unittest

from tests.utils import get_client, img_url


class TestAttribute(unittest.TestCase):
    def setUp(self):
        self.h = get_client()
        ws = self.h.get_workspaces()
        ws0 = ws[0]
        self.project = self.h.create_project(ws0, "Test Project 1")
        ds = self.project.create_dataset("ds")
        self.image = self.project.upload_from_url(ds, "tmp1.jpg", img_url, True)

    def validate_attribute(self, attr, name, attribute_type, description, norder, values):
        self.assertEqual(36, len(attr.id), 'Length of the id must be 36')
        self.assertEqual(name, attr.name)
        self.assertEqual(attribute_type, attr.attribute_type)
        self.assertEqual(description, attr.description)
        self.assertEqual(norder, attr.norder)
        for v in attr.values:
            self.assertIn(v['value'], values, f"{v['value']} not found in {values}")

    def test_attributes(self):
        attributes = self.project.get_attributes()
        self.assertEqual(0, len(attributes), 'Should be no attributes for a new project')
        # Create attribute
        attr = self.project.create_attribute("attr1", "SELECTION", "Some desc", 2, ["v1", "v2", "v3"])
        self.validate_attribute(attr, "attr1", "SELECTION", "Some desc", 2, ["v1", "v2", "v3"])
        # Update attribute
        attr.edit("attr2", "SELECTION", "Desc2", 3, ["v1", "v2"])
        self.validate_attribute(attr, "attr2", "SELECTION", "Desc2", 3, ["v1", "v2"])
        # Check get attributes
        attributes = self.project.get_attributes()
        self.assertEqual(1, len(attributes))
        self.validate_attribute(attributes[0], "attr2", "SELECTION", "Desc2", 3, ["v1", "v2"])
        # Delete attribute
        attr.delete()
        attributes = self.project.get_attributes()
        self.assertEqual(0, len(attributes), 'Should not be any attributes')

    def test_attribute_class(self):
        attr1 = self.project.create_attribute("attr1", "SELECTION", "Some desc", 2, ["v1", "v2", "v3"])
        attr2 = self.project.create_attribute("attr2", "SELECTION", "Some desc", 2, ["v1", "v2", "v3"])
        lc1 = self.project.create_label_class("class1", "#ff00aa99", "object", 2)
        lc2 = self.project.create_label_class("class2", "#ff00aa99", "object", 2)
        attr_cls = self.project.get_attribute_classes()
        self.assertEqual(0, len(attr_cls))
        self.project.set_attribute_classes([{"attribute_id": attr1.id, "class_id": lc1.id},
                                            {"attribute_id": attr1.id, "class_id": lc2.id}])
        attr_cls = self.project.get_attribute_classes()
        self.assertEqual(2, len(attr_cls))
        self.project.set_attribute_classes([{"attribute_id": attr2.id, "class_id": lc1.id},
                                            {"attribute_id": attr2.id, "class_id": lc2.id}])
        attr_cls = self.project.get_attribute_classes()
        self.assertEqual(4, len(attr_cls))
        self.project.delete_attribute_classes([{"attribute_id": attr2.id, "class_id": lc1.id},
                                               {"attribute_id": attr2.id, "class_id": lc2.id},
                                               {"attribute_id": attr1.id, "class_id": lc1.id},
                                               {"attribute_id": attr1.id, "class_id": lc2.id}])
        attr_cls = self.project.get_attribute_classes()
        self.assertEqual(0, len(attr_cls))

    def test_label_attributes(self):
        attr1 = self.project.create_attribute("attr1", "SELECTION", "Some desc", 2, ["v1", "v2", "v3"])
        attr2 = self.project.create_attribute("attr2", "SELECTION", "Some desc", 2, ["v1", "v2", "v3"])
        lc1 = self.project.create_label_class("class1", "#ff00aa99", "object", 2)
        self.project.set_attribute_classes([{"attribute_id": attr1.id, "class_id": lc1.id},
                                            {"attribute_id": attr2.id, "class_id": lc1.id}])

        label = self.image.create_label(lc1, [10, 10, 20, 20])
        lbl_attr = label.get_attributes()
        self.assertEqual(0, len(lbl_attr))
        label.set_attribute(attr1, attr1.values[0]["id"])
        lbl_attr = label.get_attributes()
        self.assertEqual(1, len(lbl_attr))
        self.assertEqual(lbl_attr[0].value, attr1.values[0]["id"])

    def tearDown(self) -> None:
        projects = self.h.get_projects()
        for p in projects:
            p.delete()


if __name__ == '__main__':
    unittest.main()
