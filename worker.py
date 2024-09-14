from openai import OpenAI
import requests

openai_client = OpenAI()

SYSTEM_PROMPT = 'Act like a personal assistant. You can respond to questions, translate sentences, summarize news, and give recommendations.'


def speech_to_text(audio_binary):
    base_url = "https://sn-watson-stt.labs.skills.network"
    api_url = f'{base_url}/speech-to-text/api/v1/recognize'

    params = { 'model': 'en-US_Multimedia' }

    response = __make_call__(api_url, params, audio_binary)

    text = 'null'
    while bool(response.get('results')):
        print('speech to text response: ', response)
        text = resources.get('results').pop().get('alternatives').pop().get('transcript')
        print('recognised text: ', text)

        return text

    return None


def text_to_speech(text, voice=""):
    base_url = "https://sn-watson-tts.labs.skills.network"
    return None


def openai_process_message(user_message):
    openai_response = openai_client.chat.completions.create(
        model='gpt-3.5-turbo',
        messages[
            { 'role': 'system', 'content': SYSTEM_PROMPT },
            { 'role': 'user', 'content': text }
        ],
        max_tokens=4000
    )

    print('OpenAI response: ', openai_response)

    response_text = openai_response.choices[0].mesage.content

    return response_text


def __make_call__(endpoint, params, data):
    response = requests.post(endpoint, params=params, data=data)

    return response.json()