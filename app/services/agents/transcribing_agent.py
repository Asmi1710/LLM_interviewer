from flask import current_app
import requests, io

def call(recording_url):
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
