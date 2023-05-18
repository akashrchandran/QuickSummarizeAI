import os
from youtube_transcript_api import YouTubeTranscriptApi
import openai
import json
import dotenv

dotenv.load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

DEV_PROMPT = os.getenv("DEV_PROMPT")

def get_subtitles(video_id):
    text = YouTubeTranscriptApi.get_transcript(video_id, languages=['en'])
    return " ". join([dialogue['text'] for dialogue in text])

def get_summary(captions):
    captions = truncate_text_to_word_limit(captions)
    completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {
            "role": "system", 
            "content": DEV_PROMPT
        },
        {
            "role": "user",
            "content": captions
        }
    ]
    )

    return completion.choices[0].message.content

def html_gen(response):
    summary = json.loads(response)
    htmlString = ''
    for key, value in summary.items():
        htmlString += f'<h3>{key}</h3>'
        if isinstance(value, list):
            htmlString += '<ul>'
            for item in value:
                if isinstance(item, dict):
                    htmlString += '<li><strong>' + item['Keyword'] + ': </strong>' + item['Explanation'] + '</li>'
                else:
                    htmlString += f'<li>{item}</li>'
            htmlString += '</ul>'
        else:
            htmlString += f'<p>{value}</p>'

    return htmlString

def truncate_text_to_word_limit(text, word_limit=3500):
    words = text.split()
    truncated_words = words[:word_limit]
    return ' '.join(truncated_words)