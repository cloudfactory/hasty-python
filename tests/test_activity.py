import os
import unittest
import urllib.request

from hasty.constants import ProjectType
from tests.utils import get_client, vid_url


class TestActivity(unittest.TestCase):
    def setUp(self):
        self.h = get_client()
        ws = self.h.get_workspaces()
        ws0 = ws[0]
        self.project = self.h.create_project(ws0, "Test Project", content_type=ProjectType.Video)
        urllib.request.urlretrieve(vid_url, "tmp5.mp4")
        ds = self.project.create_dataset("ds")
        self.video = self.project.upload_from_file(ds, "tmp5.mp4")

    def test_activity_types(self):
        act_types = self.project.get_activity_types()
        self.assertEqual(0, len(act_types), 'Should be no activity types for a new project')
        # Create activity type
        lc = self.project.create_activity_type("act1", "#ff00aa99")
        self.assertEqual(36, len(lc.id), 'Length of the id must be 36')
        self.assertEqual("act1", lc.name)
        self.assertEqual("#ff00aa99", lc.color)
        # Update activity type
        lc.edit("act2", "#ff88aa99")
        self.assertEqual("act2", lc.name)
        self.assertEqual("#ff88aa99", lc.color)
        # Delete activity type
        act_types = self.project.get_activity_types()
        self.assertEqual(1, len(act_types), 'Should be one activity type')
        lc.delete()
        act_types = self.project.get_activity_types()
        self.assertEqual(0, len(act_types), 'Should not be any activity type')

    def test_activities(self):
        activities = self.video.get_activities()
        self.assertEqual(0, len(activities), 'Should be no activities for a new video')
        # Create activity
        act_type = self.project.create_activity_type("act5", "#ff00aa99")
        act = self.video.create_activity(500, 1000, [act_type])
        self.assertEqual([act_type.id], act.activities)
        self.assertEqual(500, act.start_time_ms)
        self.assertEqual(1000, act.end_time_ms)
        activities = self.video.get_activities()
        self.assertEqual(1, len(activities), 'Should be one activity')
        # Edit activity
        act_type2 = self.project.create_activity_type("act4", "#ff00aa99")
        act.edit(2000, 10000, [act_type, act_type2])
        self.assertEqual(set([act_type.id, act_type2.id]), set(act.activities))
        self.assertEqual(2000, act.start_time_ms)
        self.assertEqual(10000, act.end_time_ms)
        activities = self.video.get_activities()
        self.assertEqual(1, len(activities), 'Should be one activity')
        # Delete activity
        act.delete()
        activities = self.video.get_activities()
        self.assertEqual(0, len(activities), 'Should be no activities')

    def tearDown(self) -> None:
        for i in ["tmp5.mp4"]:
            if os.path.exists(i):
                os.remove(i)
        projects = self.h.get_projects()
        for p in projects:
            p.delete()


if __name__ == '__main__':
    unittest.main()
