from typing import List, Text, Dict, Union
import re
from string import Template


def _match_str_template(text: Text, template: Text) -> Dict[Text, Text]:
    fields = re.findall(r"%\w*%", template)
    for field in fields:
        field_name = field.replace('%', '')
        template = template.replace(field, r'(?P<' + field_name + r'>.*)')

    template = '^' + template + '$'

    pattern = re.compile(template)
    match = pattern.match(text)
    if match:
        return match.groupdict()
    return {}


class SongInfo:
    def __str__(self) -> str:
        return Template('name: $name, time: $time') \
            .substitute(name=self.name, time=self.start_time)

    def __init__(self, name: Text, start_time: int):
        self.name = name
        self.start_time = start_time
        self.end_time: int = None

    __repr__ = __str__


def _line_to_song_info(line: Text, pattern: Text):
    d = _match_str_template(line, pattern)
    return SongInfo(d['name'], _str_time_to_seconds(d['time']))


def _str_time_to_seconds(str_time: Text) -> int:
    token_list = str_time.split(':')
    if len(token_list) > 3 or len(token_list) < 2:
        raise ValueError('wrong timestamp format')
    if len(token_list) == 2:
        token_list = ['0'] + token_list

    for token in token_list:
        token = token.strip()
        if not token.isdigit():
            raise ValueError('wrong timestamp format')
    time_list = [int(token) for token in token_list]

    seconds = sum([a * b for a, b in zip([3600, 60, 1], time_list)])
    return seconds


# Public Functions go here

def song_desc_to_song_info(desc: Text, pattern: Text) -> List[SongInfo]:
    """
    Convert lines of song description to list of SongInfo
    
    :rtype: List[SongInfo]
    :param desc: string -- do
    :param pattern: Text
    :return:
    """
    lines = desc.split('\n')
    return list(map(lambda line: _line_to_song_info(line, pattern), lines))


def set_song_end_by_next_song(song_list: List[SongInfo]):
    song_end_list: Union[int, None] = [song.start_time for song in song_list]
    song_end_list = song_end_list[1:] + [None]

    for (song, song_end) in zip(song_list, song_end_list):
        song.end_time = song_end
