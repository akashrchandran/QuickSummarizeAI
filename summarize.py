import json
import os

import dotenv
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi

dotenv.load_dotenv()

youtube_transcript_api = YouTubeTranscriptApi()

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
DEV_PROMPT = os.getenv("SYSTEM_PROMPT")

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash-lite",
    generation_config=generation_config,
)


def get_subtitles(video_id):
    text = youtube_transcript_api.fetch(video_id, languages=["en"])
    return " ".join([dialogue.text for dialogue in text])


def get_summary(captions):
    completion = model.generate_content(
        DEV_PROMPT + "\n\n" + captions
    )
    return completion.text