# -*- coding: utf-8 -*-
"""Methods for handling playlists, clips..."""

from balistos.youtube import get_related_video
from datetime import datetime
from balistos.models.playlist import PlaylistUser
from balistos.models.clip import PlaylistClip
from balistos.models.clip import PlaylistClipUser
from balistos.models.clip import Clip
from balistos.models.user import User
from pyramid_basemodel import Session


def get_playlist_videos(playlist, username=None):
    """
    Method that returns all the clips that are part of playlist

    :param    playlist: playlist of which we want to get videos
    :type     playlist: balistos.models.playlist.Playlist

    :returns: dict for each clip that is part of playlist
    :rtype:   list of dicts
    """
    result = []
    pclips = []
    user = User.get_by_username(username)
    if user:
        playlist_user = PlaylistUser.get_by_playlist_and_user(playlist, user)
        playlist_user.last_active = datetime.now()
        Session.flush()
    try:
        if check_if_finished(PlaylistClip.get_active_playlist_clip(playlist)):
            play_next_clip(playlist)
    except Exception:
        pass
    pclips.append(PlaylistClip.get_active_playlist_clip(playlist))
    next_pclip = PlaylistClip.get_queue_playlist_clip(playlist)
    if next_pclip:
        pclips.append(next_pclip)
    else:
        set_next_in_queue(playlist)
    wait_clips = PlaylistClip.get_by_playlist_waiting(playlist)
    if wait_clips:
        pclips = pclips + wait_clips
    for pclip in pclips:
        clip = pclip.clip
        if pclip.state == 2:
            start_time = (datetime.now() - pclip.started).total_seconds()
        else:
            start_time = 0
        liked = -2
        owner = PlaylistClipUser.get_playlist_clip_owner(pclip)
        owner = owner.username if owner else 'related'
        if user:
            pclipuser = PlaylistClipUser.get_by_playlist_clip_and_user(
                pclip,
                user
            )
            liked = pclipuser.liked
        result.append(
            {
                'id': clip.youtube_video_id,
                'title': clip.title,
                'likes': pclip.likes,
                'image': clip.image_url,
                'start_time': start_time,
                'liked': liked,
                'owner': owner
            },
        )
    return result


def get_playlist_settings(playlist, username=None):
    """
    Get settings for current playlist for this user

    :param    playlist: current playlist
    :type     playlist: balistos.models.playlist.Playlist
    :param    username: username of current user or None
    :type     username: str

    :returns: settings of playlist
    :rtype:   dict
    """
    return {
        'duration_limit': playlist.duration_limit
    }


def play_next_clip(playlist):
    """
    Play next clip (clip in queue) in playlist

    :param    playlist: current playlist
    :type     playlist: balistos.models.playlist.Playlist
    """

    next_pclip = PlaylistClip.get_queue_playlist_clip(playlist)
    if next_pclip:
        next_pclip.state = 2
        next_pclip.started = datetime.now()
        set_next_in_queue(playlist, next_pclip.clip.youtube_video_id)
        Session.flush()


def check_if_finished(pclip):
    """
    Check if currently active clip finished playing and remove it from playing,
    state if it is.

    :param    pclip: active playlist clip
    :type     pclip: balistos.models.playlist.PlaylistClip

    :returns: True if clip is finished and we removed it, False otherwise
    :rtype:   boolean
    """
    duration = pclip.clip.duration
    started = pclip.started
    if (datetime.now()-started).total_seconds() > duration:
        Session.delete(pclip)
        #Session.flush()
        return True
    return False


def set_next_in_queue(playlist, youtube_video_id):
    """
    Set next video in queue based on likes, time added

    :param    playlist: playlist for which next clip we are setting
    :type     playlist: balistos.models.playlist.Playlist
    """
    pclips = PlaylistClip.get_by_playlist_waiting(playlist)
    if pclips:
        pclips[0].state = 1
    else:
        video = get_related_video(playlist, youtube_video_id)
        add_playlist_clip(
            playlist,
            video['title'],
            video['image_url'],
            video['youtube_video_id'],
            video['duration'],
            state=1,
        )
    Session.flush()


def add_playlist_clip(
    playlist,
    title,
    image_url,
    youtube_video_id,
    duration,
    username=None,
    state=0,
):
    """
    Add clip to playlist

    :param    playlist:         playlist of which we want to get videos
    :type     playlist:         balistos.models.playlist.Playlist
    :param    title:            title of video
    :type     title:            str
    :param    image_url:        url of image used for thumbnail
    :type     image_url:        str
    :param    youtube_video_id: id of video on youtube
    :type     youtube_video_id: str
    :param    duration:         duration of video
    :type     duration:         int
    :param    username:         username of user that added this clip
    :type     username:         str
    :param    state:            state of video to be added
    :type     state:            int

    """

    clip = Clip.get(youtube_video_id)
    if not clip:
        clip = Clip(
            title=title,
            image_url=image_url,
            youtube_video_id=youtube_video_id,
            likes=0,
            duration=duration,
        )
        Session.add(clip)
        Session.flush()
    pclip = PlaylistClip.get_by_playlist_and_clip(playlist, clip)
    if not pclip:
        pclip = PlaylistClip(
            added=datetime.now(),
            likes=0,
            state=state,
            clip=clip,
            playlist=playlist,
            username=username,
        )
        Session.add(pclip)
        Session.flush()
    else:
        pclip.likes += 1


def remove_playlist_clip(playlist, youtube_video_id):
    """
    Remove clip from playlist

    :param    playlist: playlist we want to delete clip from
    :type     playlist: balistos.models.Playlist
    :param    clip:     youtube video id we want to delete from playlist
    :type     clip:     [clip type]

    :returns  True if removed, False otherwise
    :rtype    boolean
    """

    pclip = PlaylistClip.get_by_playlist_and_clip(
        playlist,
        Clip.get(youtube_video_id)
    )
    if not pclip:
        return False

    state = pclip.state
    Session.delete(pclip)

    if state == 2:
        play_next_clip(playlist)
    elif state == 1:
        set_next_in_queue(playlist, youtube_video_id)
    Session.flush()
    return True


def get_active_users(playlist):
    """
    Get active users for current playlist

    :param    playlist: current playlist
    :type     playlist: balistos.models.playlist.Playlist

    :returns: active users list
    :rtype:   list
    """
    users = []
    for playlist_user in PlaylistUser.get_active_users_for_playlist(playlist):
        user = {}
        user['username'] = playlist_user.user.username
        users.append(user)
    return users
