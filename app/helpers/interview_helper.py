import json

def get_redis():
    from flask import current_app
    return current_app.extensions['redis']

def save_interview_session(call_sid, data: dict):
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
    import requests
    import tempfile

    client = current_app.extensions['openai_client']
    try:
        # Download Twilio recording
        audio = requests.get(recording_url)
        with tempfile.NamedTemporaryFile(suffix=".mp3") as f:
            f.write(audio.content)
            f.seek(0)
            transcript = client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )
            current_app.logger.info(f"transcript: {transcript}")
            return transcript.text
    except Exception as e:
        print("STT error:", e)
        return ""
