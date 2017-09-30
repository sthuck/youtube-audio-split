from typing import Text, List
from string import Template

from utils import SongInfo


def build_ffmpeg_filter(index: int, song: SongInfo):
    output_name = Template('[out$index]').substitute({'index': str(index)})
    end = song.end_time
    start = song.start_time

    end_param = ['end=', str(end), ':'] if end is not None else []
    return ''.join(['[0:a]atrim=']
                   + end_param
                   + ['start=', str(start), output_name])


def build_ffmpeg_output(index: int, song: SongInfo):
    return Template('-map [out$index] -acodec libmp3lame -aq 1 -vn  "$name.mp3"') \
        .substitute({'index': str(index), 'name': song.name})


def build_ffmpeg_command(input_file: Text, song_list: List[SongInfo]):
    filters = ';'.join([build_ffmpeg_filter(index, song) for index, song in enumerate(song_list)])
    outputs = ' '.join([build_ffmpeg_output(index, song) for index, song in enumerate(song_list)])

    return ''.join(['ffmpeg -i "', input_file, '" ', '-filter_complex \'', filters, '\' ', outputs])
