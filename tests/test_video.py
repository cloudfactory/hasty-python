import os
import time
import unittest
import urllib.request

from hasty.exception import ValidationException
from hasty.constants import ProjectType
from hasty.project import VideoProject
from tests.utils import get_client, vid_url


class TestVideo(unittest.TestCase):
    def setUp(self):
        self.h = get_client()
        ws = self.h.get_workspaces()
        ws0 = ws[0]
        self.project = self.h.create_project(ws0, "Test Project 1", content_type=ProjectType.Video)
        urllib.request.urlretrieve(vid_url, "video.mp4")

    def test_video_project(self):
        # Fetch video project by id
        video_project = self.h.get_project(self.project.id)
        self.assertIsInstance(video_project, VideoProject)

    def test_video(self):
        ds = self.project.create_dataset("ds")
        # Test upload from file
        self.project.upload_from_file(ds, "video.mp4")
        videos = self.project.get_videos()
        self.assertEqual(1, len(videos))
        self.assertEqual("video.mp4", videos[0].name)
        # Upload from url
        self.project.upload_from_url(ds, "tmp1.mp4", vid_url)
        videos = self.project.get_videos()
        self.assertEqual(2, len(videos))
        self.assertIn(videos[0].name, ("video.mp4", "tmp1.mp4"))
        self.assertIn(videos[1].name, ("video.mp4", "tmp1.mp4"))
        # Download video
        for _ in range(60):  # timeout in 5-mins
            try:
                videos[0].download(videos[0].name)
                break
            except ValidationException:
                time.sleep(5)
                continue
        self.assertTrue(os.path.exists(videos[0].name), "video doesnt exists after download")
        # Delete dataset
        ds.delete()

    def test_video_filters_and_status(self):
        ds2 = self.project.create_dataset("ds2")
        self.project.upload_from_url(ds2, "tmp1.mp4", vid_url)
        vid2 = self.project.upload_from_url(ds2, "tmp2.mp4", vid_url)
        ds3 = self.project.create_dataset("ds3")
        vid3 = self.project.upload_from_url(ds3, "tmp3.mp4", vid_url)
        vid2.set_status("TO REVIEW")
        vid3.set_status("DONE")
        # Check total number of videos
        videos = self.project.get_videos()
        self.assertEqual(3, len(videos))
        # Filter by status DONE
        videos = self.project.get_videos(video_status="DONE")
        self.assertEqual(1, len(videos))
        # Filter by status DONE, TO REVIEW
        videos = self.project.get_videos(video_status=["DONE", "TO REVIEW"])
        self.assertEqual(2, len(videos))
        # Filter by status and dataset
        videos = self.project.get_videos(dataset=ds3, video_status=["DONE", "TO REVIEW"])
        self.assertEqual(1, len(videos))
        # Filter by datasets
        videos = self.project.get_videos(dataset=[ds2, ds3])
        self.assertEqual(3, len(videos))
        # Delete dataset
        ds2.delete()
        ds3.delete()

    def test_video_rename_move_delete(self):
        ds2 = self.project.create_dataset("ds2")
        ds3 = self.project.create_dataset("ds3")
        self.project.upload_from_url(ds2, "tmp1.mp4", vid_url)
        # Check video name
        videos = self.project.get_videos()
        video = videos[0]
        self.assertEqual("tmp1.mp4", video.name)
        # Check rename feature
        video.rename("tmp2.mp4")
        self.assertEqual("tmp2.mp4", video.name)
        # Check move feature
        video.move(ds3)
        self.assertEqual(ds3.id, video.dataset_id)
        # Check delete
        video.delete()
        videos = self.project.get_videos()
        self.assertEqual(0, len(videos))

    def tearDown(self) -> None:
        projects = self.h.get_projects()
        for i in ["video.mp4", "tmp1.mp4"]:
            if os.path.exists(i):
                os.remove(i)
        for p in projects:
            p.delete()


if __name__ == '__main__':
    unittest.main()
