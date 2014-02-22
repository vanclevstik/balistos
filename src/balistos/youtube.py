# -*- coding: utf-8 -*-
"""Youtube API interaction methods"""

from balistos import DEVELOPER_KEY
import gdata.youtube
import gdata.youtube.service
from random import randrange


def get_related_video(playlist, video_id):
    """
    Gets related video and its information

    :param    video_id: id of current video
    :type     video_id: str

    :returns: all the info about related video
    :rtype:   dict of strings
    """
    yt_service = gdata.youtube.service.YouTubeService()
    yt_service.ssl = True

    yt_service.developer_key = DEVELOPER_KEY
    max_seconds = playlist.duration_limit
    videos = None
    while not videos:
        related_feed = yt_service.GetYouTubeRelatedVideoFeed(video_id=video_id)
        videos = select_video(related_feed.entry, max_seconds=max_seconds)
        if not videos:
            video_id = related_feed.entry[0].id.text.split('/')[-1]

    return videos


def select_video(videos, max_seconds=600):
    """
    Select videos from related videos list according to our options

    :param    videos: list of videos
    :type     videos: list of Youtube VideoEntry

    :returns: metadata of selected video
    :rtype:   dict
    """
    videos = [video for video in videos if int(video.media.duration.seconds) < max_seconds]  # noqa
    if not videos:
        return None
    video = videos[randrange(len(videos)-1)]
    title = unicode(video.title.text)
    image_url = video.media.thumbnail[0].url
    duration = video.media.duration.seconds
    youtube_video_id = video.id.text.split('/')[-1]

    return {
        'youtube_video_id': youtube_video_id,
        'title': title,
        'image_url': image_url,
        'duration': duration,
    }
