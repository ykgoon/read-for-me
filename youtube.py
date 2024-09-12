import re
from youtube_transcript_api import YouTubeTranscriptApi

class YouTube(object):
    def is_link(self, url):
        # Detect if `url` is a YouTube link
        youtube_regex = re.compile(
            r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?([\w-]{11})"
        )
        match = youtube_regex.match(url)
        return bool(match)

    def get_transcriptions(self, url:str):
        vid = self._get_video_id(url)
        try:
            transcriptions = YouTubeTranscriptApi.get_transcript(vid)
            return '\n'.join([trs['text'] for trs in transcriptions])
        except:
            return False

    def _get_video_id(self, url):
        """
        Given a YouTube url, extract and return the video ID
        """
        if not self.is_link(url): return
        match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11}).*", url)
        if match:
            return match.group(1)
