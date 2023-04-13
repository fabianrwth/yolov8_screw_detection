"""
Download Youtube Videos and cut them as you like (start and end time)

Usage - sources:
    $ python youtube_download.py --name <video.mp4>--url <youtube_url> --start <int> --end <int> --dest <path>
                --name: name of output video
                --url: youtube url (required)
                --start: start time (optional)
                --end: end time (optional)
                --dest: destination directory (optional)

"""


from pytube import YouTube
import os
import moviepy
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import argparse


def download(name, url, start, end, dest):
    print("Name: {}, URL: {}, Start: {}, End: {}, Destination: {}".format(name, url, start, end, dest))

    yt = YouTube(url)
    video_length = yt.length
    video = yt.streams.filter(res="720p", file_extension="mp4").first()
    file_name = name

    DIR_PATH = dest
    FILE_PATH = os.path.join(DIR_PATH, file_name)

    video.download(DIR_PATH, file_name)

    # cutting the downloaded video
    if start or end:
        start_time = start if start is not None else 0
        end_time = end if end is not None else video_length
        ffmpeg_extract_subclip(FILE_PATH, start_time, end_time, targetname=FILE_PATH.replace(".mp4", "_edit.mp4"))

    # remove the original video
    os.remove(FILE_PATH)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", type=str, help="name of output video")
    parser.add_argument("--url", type=str, help="url of youtube video")
    parser.add_argument("--start", type=int)
    parser.add_argument("--end", type=int)
    parser.add_argument("--dest", type=str, default="../data/input/videos", help="destination directory")
    args = parser.parse_args()

    if not (args.url and args.name):
        parser.error("No name and url requested, add --name and --url")

    return args


if __name__ == "__main__":
    args = parse_args()
    download(**vars(args))
