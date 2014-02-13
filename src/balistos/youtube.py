# -*- coding: utf-8 -*-
"""Youtube API interaction methods"""

from balistos import DEVELOPER_KEY
import gdata.youtube
import gdata.youtube.service
from random import randrange


def get_related_video(video_id):
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

    related_feed = yt_service.GetYouTubeRelatedVideoFeed(video_id=video_id)

    videos = related_feed.entry
    # videos_len = len(videos)
    # end = videos_len > 10 and 10 or videos_len
    video = videos[randrange(len(videos)-1)]
    title = video.title.text
    image_url = video.media.thumbnail[0].url
    duration = video.media.duration.seconds
    youtube_video_id = video.id.text.split('/')[-1]

    return {
        'youtube_video_id': youtube_video_id,
        'title': title,
        'image_url': image_url,
        'duration': duration,
    }
