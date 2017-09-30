import unittest
from utils import _match_str_template, song_desc_to_song_info, _str_time_to_seconds, set_song_end_by_next_song


class TestUtils(unittest.TestCase):
    def test_match_str_template_simple(self):
        # Simple case
        result = _match_str_template('Nick Cave - 04:20', r'%artist% - %time%')
        self.assertEqual(result, {'artist': 'Nick Cave', 'time': '04:20'})

    def test_match_str_template_multiple(self):
        # Multiple separators
        result = _match_str_template('Some words - goes here - 04:20', r'%song% - %time%')
        self.assertEqual(result, {'song': 'Some words - goes here', 'time': '04:20'})

    def test_str_time_to_seconds(self):
        res = _str_time_to_seconds('00:05:4')
        self.assertEqual(res, 304, 'Simple case')

        res = _str_time_to_seconds('10:10')
        self.assertEqual(res, 610, 'No hours')

        with self.assertRaises(ValueError):
            _str_time_to_seconds('00:10:10:05')

        with self.assertRaises(ValueError):
            _str_time_to_seconds('00:A:15')

    def test_song_desc_to_song_info(self):
        text = '''I Love You, Honeybear - 1:04:50
In Twenty Years or So - 1:12:31
Holy Shit - 1:18:24'''
        song_list = song_desc_to_song_info(text, r'%name% - %time%')
        res = [vars(song_info) for song_info in song_list]
        self.assertEqual(res,
                         [{'name': 'I Love You, Honeybear', 'start_time': 3890, 'end_time': None},
                          {'name': 'In Twenty Years or So', 'start_time': 4351, 'end_time': None},
                          {'name': 'Holy Shit', 'start_time': 4704, 'end_time': None}])

    def test_set_song_end_by_next_song(self):
        text = '''I Love You, Honeybear - 1:04:50
In Twenty Years or So - 1:12:31
Holy Shit - 1:18:24'''
        song_list = song_desc_to_song_info(text, r'%name% - %time%')
        set_song_end_by_next_song(song_list)

        res = [vars(song_info) for song_info in song_list]
        self.assertEqual(res,
                         [{'name': 'I Love You, Honeybear', 'start_time': 3890, 'end_time': 4351},
                          {'name': 'In Twenty Years or So', 'start_time': 4351, 'end_time': 4704},
                          {'name': 'Holy Shit', 'start_time': 4704, 'end_time': None}])


if __name__ == '__main__':
    unittest.main()
