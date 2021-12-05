import asyncio
import json
import re
import sys
import time

import discordsdk as dsdk
from winrt.windows.media.control import \
    GlobalSystemMediaTransportControlsSessionManager as MediaManager
from winrt.windows.storage.streams import DataReader, Buffer, InputStreamOptions

GROOVE_ID = 'Microsoft.ZuneMusic_8wekyb3d8bbwe!Microsoft.ZuneMusic'
DISCORD_CLIENT_ID = json.load(open('discord_key.json', 'r'))
LINE_LENGTH = 200


async def get_media_info():
    sessions = await MediaManager.request_async()
    # TODO: support YouTube Music playing in edge too
    groove_session = [s for s in sessions.get_sessions() if s.source_app_user_model_id == GROOVE_ID]
    if groove_session:  # if there is a Groove session running
        groove_session = groove_session[0]  # should only be one instance running so first item in list
        if groove_session.get_playback_info().playback_status == 4:  # i.e. music is playing (not paused)
            properties_obj = await groove_session.try_get_media_properties_async()
            info_dict = {
                song_attr: properties_obj.__getattribute__(song_attr)
                for song_attr in dir(properties_obj) if song_attr[0] != '_'
            }
            info_dict['genres'] = list(info_dict['genres'])
            # timeline = groove_session.get_timeline_properties()
            
            # https://github.com/Willy-JL/Soundy/blob/ae5b8bddaafd636d691ccf8921fa3b5ec9a2c825/modules/api.py#L20
            # timeline_dict = {song_attr: int(timeline.__getattribute__(song_attr).duration / 10000) for song_attr in dir(timeline) if song_attr[0] != '_' and isinstance(timeline.__getattribute__(song_attr), TimeSpan) and song_attr != 'end_time' and song_attr != 'start_time'}
            
            # [x.duration/10000000/60 for x in (timeline_properties.start_time, timeline_properties.position, timeline_properties.end_time)]
            return info_dict
        else:
            return
            
    else:
        return 'quit'


async def read_stream_into_buffer(stream_ref, buffer):
    readable_stream = await stream_ref.open_read_async()
    readable_stream.read_async(buffer, buffer.capacity, InputStreamOptions.READ_AHEAD)


def get_song_info_tuple():
    current_song_info = asyncio.run(get_media_info())
    if current_song_info:
        if current_song_info == 'quit':
            for i in range(3):
                print(f'No Groove Music instance detected. Shutting down in {3-i}...'.ljust(LINE_LENGTH), end='\r')
                time.sleep(1)
            sys.exit()
            
        if ' (On ' in current_song_info['title']:
            title, subtitle = current_song_info['title'].split(' (On ')
            subtitle = subtitle[:-1] if subtitle[-1] == ')' else subtitle
        else:
            title, subtitle = current_song_info['title'], ''   
        
        artist = current_song_info['artist']
        album = current_song_info['album_title']
        
        long_hover = f'{title} by {artist} on {subtitle if subtitle else album}'
        subtitle = subtitle[:17] + '...' if len(subtitle) > 20 else subtitle

        image_key = re.sub(r' & ', '_', album)
        # replace all of these characters with '_'
        image_key = re.sub(r'[\[:\]#+&. ]', '_', image_key).lower()
        
        # hard-coded album names
        if album == '[+ +]':
            image_key = 'plus_plus'
        elif album == '[#]':
            image_key = 'hash'
        elif image_key == '케이팝_음악':
            image_key = 'k_pop'
        elif len(image_key) > 32:  # const char* largeImageKey; /* max 32 bytes */
            image_key = image_key[:32]

        return (f'{title} by {artist}',
                f'On {subtitle if subtitle else album}'
                + str(f' - collated on {album}' if subtitle and subtitle != album else ''),
                image_key, artist, long_hover)


def discord_callback(result):
    global activity
    global start
    if result == dsdk.Result.ok:
        # make sure cmd window has no wrap and has a long (buffer) line length
        print(f'(t+{time.time()-start:>9.3f}s) '
              f'{"[Groove Music is not playing media] " if activity.state=="" else ""}'
              f'Successfully updated Groove Discord RP with: "{activity.details}"; '
              f'"{activity.state}"; (image_key)"{activity.assets.large_image}"'.ljust(LINE_LENGTH), end='\r')
    else:
        # breakpoint()
        raise Exception(result)


if __name__ == '__main__':

    # for converting thumbnail stream into file
    # # create the current_media_info dict with the earlier code first
    # thumb_stream_ref = asyncio.run(get_media_info())['thumbnail']
    #
    # # 5MB (5 million byte) buffer - thumbnail unlikely to be larger
    # thumb_read_buffer = Buffer(5000000)
    #
    # # copies data from data stream reference into buffer created above
    # asyncio.run(read_stream_into_buffer(thumb_stream_ref, thumb_read_buffer))
    #
    # # reads data (as bytes) from buffer
    # buffer_reader = DataReader.from_buffer(thumb_read_buffer)
    # byte_buffer = buffer_reader.read_bytes(thumb_read_buffer.length)
    #
    # with open('media_thumb.jpg', 'wb+') as fobj:
    #     fobj.write(bytearray(byte_buffer))
    #     print('Successfully wrote media_thumb.jpg to disk')

    app = dsdk.Discord(DISCORD_CLIENT_ID, dsdk.CreateFlags.default)  # TODO: error handle no Discord instance (stop ddl error on startup)
    activity_manager = app.get_activity_manager()
    start = time.time()

    while 1:
        time.sleep(1)  # updates presence once per second
        info_tuple = get_song_info_tuple()
        activity = dsdk.Activity()
        if info_tuple:
            # Discord doesn't throw an error if the image key doesn't exist
            activity.details, activity.state, activity.assets.large_image, current_artist, activity.assets.large_text = info_tuple
            # activity.assets.large_text = activity.details
            if 'LOONA' in current_artist:
                # activity.assets.small_image = 'orbit'
                # activity.assets.small_text = 'LOONA'
                pass
        else:
            activity.details, activity.state = 'Media currently paused.', ''
            # activity_manager.clear_activity(lambda x: print('No status'.ljust(LINE_LENGTH), end='\r'))
            
        activity_manager.update_activity(activity, discord_callback)
        app.run_callbacks()
