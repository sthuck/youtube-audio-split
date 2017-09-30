from ffmpeg import build_ffmpeg_command
from utils import song_desc_to_song_info, set_song_end_by_next_song

filename = r'/Users/aviadh/Father John Misty ~  2017-06-30 ~ Roskilde Festival ~ full show-0trfwUJQbG4.webm'
setlist = '''Pure Comedy - 0:22
Total Entertainment Forever - 7:06
Things It Would Have Been Helpful to Know Before the Revolution - 10:11
Ballad of the Dying Man - 14:52
When You're Smiling and Astride Me - 20:15
Nancy From Now On - 25:22
Chateau Lobby #4 (in C for Two Virgins) - 29:37
Strange Encounter - 32:50
When the God of Love Returns There'll Be Hell to Pay - 37:02
A Bigger Paper Bag - 43:27
True Affection - 48:31
Bored in the USA - 52:46
Hollywood Forever Cemetery Sings - 57:49
Real Love Baby - 1:01:25
I Love You, Honeybear -  1:04:50
In Twenty Years or So - 1:12:31
Holy Shit - 1:18:24'''
template = '%name% - %time%'
artist = 'Father John Misty'
album = 'Live at Roskilde 2017'


def main():
    song_list = song_desc_to_song_info(setlist, template)
    set_song_end_by_next_song(song_list)
    command = build_ffmpeg_command(filename, song_list)

    print(command)


if __name__ == '__main__':
    main()
