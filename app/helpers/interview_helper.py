import json
from flask import current_app

def get_redis():
    return current_app.extensions['redis']

def save_interview_session(call_sid, data: dict):
    current_app.logger.info(f"save_interview_session: {call_sid}, \n data: {data}")
    r = get_redis()
    r.set(f"interview:{call_sid}", json.dumps(data), ex=3600)  # 1 hr expiry

def load_interview_session(call_sid):
    r = get_redis()
    raw = r.get(f"interview:{call_sid}")
    return json.loads(raw) if raw else None

def delete_interview_session(call_sid):
    r = get_redis()
    r.delete(f"interview:{call_sid}")

# use AI to create a next question/response based on editable prompt, previous answer and current next question
def generate_questions(question):
    return question


def transcribe_recording(recording_url):
    from flask import current_app
    import requests, tempfile, io

    client = current_app.extensions['openai_client']
    account_sid = current_app.config['TWILIO_ACCOUNT_SID']
    auth_token = current_app.config['TWILIO_AUTH_TOKEN']
    try:
        # Download Twilio recording with basic auth
        audio = requests.get(recording_url, auth=(account_sid, auth_token))
        if audio.status_code != 200:
            current_app.logger.error(f"Failed to download audio: {audio.status_code}")
            return ""
        
        audio_bytes = io.BytesIO(audio.content)
        audio_bytes.name = "recording.mp3"
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_bytes
        )
        current_app.logger.info(f"transcript: {transcript}")
        return transcript.text
    except Exception as e:
        print("STT error:", e)
        return ""
