from youtube_transcript_api import YouTubeTranscriptApi


def get_subtitles(video_id):
    text = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    return " ". join([dialogue['text'] for dialogue in text])

# print(get_subtitles('9bZkp7q19f0')) disables subtiltes
print(get_subtitles("elvwguckWjQ"))