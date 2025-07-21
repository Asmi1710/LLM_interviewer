from twilio.twiml.voice_response import VoiceResponse
import time

from app.constants.questions import questions_list
from app.repositories import _interview_repository
from app.helpers.interview_helper import save_interview_session, load_interview_session, delete_interview_session, transcribe_recording

def call(call_sid, recording_url, candidate_id, job_id, role):
    session = load_interview_session(call_sid)
    if not session:
        session = {
            "candidate_id": candidate_id,
            "job_id": job_id,
            "question_index": 0,
            "questions": questions_list.get(role) if questions_list.get(role) else ['Please tell me about yourself.', 'Give me breif description of your work experience.'],
            "transcript": []
        }

    index = session["question_index"]
    questions = session["questions"]
    response = VoiceResponse()

    # Save previous answer
    if recording_url and index > 0:
        transcript = transcribe_recording(recording_url)
        session["transcript"].append({
            "question": questions[index - 1],
            "answer_url": recording_url,
            "answer_txt": transcript
        })

    # Ask next question
    if index < len(questions):
        audio_url = f"https://your-public-url/audio/q{index}.mp3"
        response.play(audio_url)
        response.record(
            action=f"/interviews/handle",
            max_length=30,
            transcribe=False
        )
        session["question_index"] += 1
        save_interview_session(call_sid, session)
    else:
        # End of interview
        response.say("Thank you. Your interview is now complete.")
        _interview_repository().create(
            candidate_id=session["candidate_id"],
            job_id=session["job_id"],
            transcript=session["transcript"]
        )
        delete_interview_session(call_sid)

    return response
