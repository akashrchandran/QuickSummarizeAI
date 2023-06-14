import json
import os

import dotenv
import openai
import tiktoken
from youtube_transcript_api import YouTubeTranscriptApi

dotenv.load_dotenv()
tokenizer = tiktoken.encoding_for_model("gpt-3.5-turbo")

openai.api_key = os.getenv("OPENAI_API_KEY")
DEV_PROMPT = os.getenv("DEV_PROMPT")

def get_subtitles(video_id):
    text = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    return " ". join([dialogue['text'] for dialogue in text])

def get_summary(captions):
    captions = truncate_text_to_word_limit(captions)
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo-0613",
    messages=[
        {
            "role": "system", 
            "content": DEV_PROMPT
        },
        {
            "role": "user",
            "content": captions
        }
    ],
    temperature=0.5,
    )
    return completion.choices[0].message.content

def truncate_text_to_word_limit(text, word_limit=3700):
    tokens = tokenizer.encode(text)
    tokens = tokens[:word_limit]
    return tokenizer.decode(tokens)
