import os
import subprocess


def extract_audio(video_path):

    audio_path = (
        os.path.splitext(video_path)[0]
        + ".mp3"
    )

    subprocess.run(
        [
            "ffmpeg",
            "-i",
            video_path,
            "-vn",
            "-acodec",
            "libmp3lame",
            audio_path,
            "-y"
        ],
        check=True
    )

    return audio_path