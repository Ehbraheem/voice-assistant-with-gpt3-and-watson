import os
import requests
from openai import OpenAI
from dotenv import load_dotenv
from functools import reduce

load_dotenv()

openai_client = OpenAI()

STT_BASE_URL = os.getenv('STT_BASE_URL') or "https://sn-watson-stt.labs.skills.network"
TTS_BASE_URL = os.getenv('TTS_BASE_URL') or "https://sn-watson-tts.labs.skills.network"

SYSTEM_PROMPT = 'Act like a personal assistant. You can respond to questions, translate sentences, summarize news, and give recommendations.'


def speech_to_text(audio_binary):
    api_url = f'{STT_BASE_URL}/speech-to-text/api/v1/recognize'

    params = { 'model': 'en-US_Multimedia' }

    response = requests.post(api_url, params=params, data=audio_binary).json()

    text = 'null'
    if not bool(response.get('results')):
        return text

    flattened_result = reduce(lambda accum, curr: accum + curr.get('alternatives', []), response.get('results'), [])

    winning_prediction = max(flattened_result, key=lambda r: r.get('confidence'))

    text = winning_prediction.get('transcript', text).strip()

    return text


def text_to_speech(text, voice=""):
    api_url = f'{TTS_BASE_URL}/text-to-speech/api/v1/synthesize?output=output_text.wav'

    if voice and voice != 'default':
        api_url = f'{api_url}&voice={voice}'

    headers = {
        'Accept': 'audio/wav',
        'Content-Type': 'application/json'
    }

    data = {
        'text': text
    }

    response = requests.post(api_url, headers=headers, json=data)
    print('Text to Speech response: ', response)

    return response.content


def openai_process_message(user_message):
    openai_response = openai_client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages=[
            { 'role': 'system', 'content': SYSTEM_PROMPT },
            { 'role': 'user', 'content': user_message }
        ],
        max_tokens=4000
    )

    print('OpenAI response: ', openai_response)

    response_text = openai_response.choices[0].message.content

    return response_text
