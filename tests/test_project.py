import unittest

from tests.utils import get_client


class TestProject(unittest.TestCase):
    def setUp(self):
        self.h = get_client()
        projects = self.h.get_projects()
        for p in projects:
            p.delete()

    def test_project(self):
        ws = self.h.get_workspaces()
        self.assertEqual(1, len(ws), 'User should have an access to a single workspace')
        ws0 = ws[0]
        self.assertEqual(36, len(ws0.id), 'Length of the id must be 36')
        self.assertTrue(isinstance(ws0.id, str), 'Workspace id must be string')
        projects = self.h.get_projects()
        self.assertEqual(0, len(projects), "There shouldn't be any projects")
        # Create project using ws entity
        new_project1 = self.h.create_project(ws0, "Test Project 1")
        self.assertEqual(36, len(new_project1.id), 'Length of the id must be 36')
        self.assertEqual("Test Project 1", new_project1.name, 'Check project name')
        # Create project using ws id
        new_project2 = self.h.create_project(ws0.id, "Test Project 2", "Some Description")
        self.assertEqual("Test Project 2", new_project2.name, 'Check project name')
        self.assertEqual("Some Description", new_project2.description, 'Check project description')
        # Edit project
        new_project2.edit("Test Project 2 Edited", "Some Description Edited")
        self.assertEqual("Test Project 2 Edited", new_project2.name, 'Check project name')
        self.assertEqual("Some Description Edited", new_project2.description, 'Check project description')
        # Delete project
        new_project2.delete()
        projects = self.h.get_projects()
        self.assertEqual(1, len(projects), "There should be 1 project")
        # Get project by id
        copy_project = self.h.get_project(new_project1.id)
        self.assertEqual(copy_project.id, new_project1.id, "Projects IDs must be the same")
        self.assertEqual(copy_project.name, new_project1.name, "Projects names must be the same")

    def tearDown(self) -> None:
        projects = self.h.get_projects()
        for p in projects:
            p.delete()


if __name__ == '__main__':
    unittest.main()
