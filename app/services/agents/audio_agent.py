from elevenlabs.client import ElevenLabs
from elevenlabs import play
import os, wave, io
from flask import current_app


elevenlabs = ElevenLabs(
  api_key=os.getenv("ELEVENLABS_API_KEY"),
)

def generate_voice(input_text):
    audio_pcm_generator = elevenlabs.text_to_speech.convert(
        text=input_text,
        voice_id= current_app.config['ELEVENLAB_VOICE_ID'],
        model_id= "eleven_multilingual_v2",
        output_format="pcm_16000",
    )
    #play(audio)
    # Combine generator chunks into bytes
    audio_pcm = b"".join(audio_pcm_generator)
    
    audio_wave = convert_pcm_to_wav(audio_pcm)
    return audio_wave


def convert_pcm_to_wav(pcm_data):
    buffer = io.BytesIO()
    with wave.open(buffer, 'wb') as wf:
        wf.setnchannels(1)          # mono
        wf.setsampwidth(2)          # 2 bytes = 16 bits
        wf.setframerate(16000)      # 16 kHz
        wf.writeframes(pcm_data)
    buffer.seek(0)
    return buffer