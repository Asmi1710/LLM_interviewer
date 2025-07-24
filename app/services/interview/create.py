from twilio.twiml.voice_response import VoiceResponse
import hmac, hashlib, time
from xml.sax.saxutils import escape

from flask import current_app, Response
from app.constants.questions import questions_list
from app.repositories import _interview_repository
from app.helpers.interview_helper import save_interview_session, load_interview_session, delete_interview_session, transcribe_recording
from app.services.agents.audio_agent import generate_voice

def call(call_sid, recording_url, candidate_id, job_id, role):
    try: 
        session = load_interview_session(call_sid)
        current_app.logger.info(f"Fetched session: {session}")
        if not session:
            current_app.logger.info(f"creating session")
            session = {
                "candidate_id": candidate_id,
                "job_id": job_id,
                "question_index": 0,
                "questions": questions_list.get(role) or ['Please tell me about yourself.', 'Give me breif description of your work experience.'],
                "transcript": []
            }

        index = session["question_index"]
        questions = session["questions"]
        response = VoiceResponse()

        # Save previous answer
        if recording_url and index > 0:
            current_app.logger.info(f" recording_url: {recording_url}")
            transcript = transcribe_recording(recording_url)
            current_app.logger.info(f" transcript: {transcript}")
            session["transcript"].append({
                "question": questions[index - 1].get('question'),
                "answer_url": recording_url,
                "answer_txt": transcript
            })

        # Ask next question
        if index < len(questions):
            ai_reply = questions[index].get('question')
            current_app.logger.info(f" ai_reply: {ai_reply}")
            ts = str(int(time.time()))
            message = f"{ai_reply}{ts}".encode("utf-8")
            signature = hmac.new(current_app.config['HMAC_SECRET_KEY'].encode(), message, hashlib.sha256).hexdigest()

            audio_url = (
                f"{current_app.config['AI_INTERVIEWER_BASE_URL']}/api/v1/interviews/audio"
                f"?text={ai_reply}&ts={ts}&sig={signature}"
            )
            audio_url_escaped = escape(audio_url)
            current_app.logger.info(f" audio_url: {audio_url}")
            # Play AI question and record user's answer
            response.play(audio_url_escaped)

            record_action_url = escape(
                f"{current_app.config['AI_INTERVIEWER_BASE_URL']}/api/v1/interviews/create"
                f"?candidate_id={candidate_id}&job_id={job_id}&role={role}"
            )
            response.record(
                action=record_action_url,
                method='POST',
                max_length=30,
                transcribe=False
            )
            current_app.logger.info(f" return from recording send")

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
            current_app.logger.info(f" end")
            delete_interview_session(call_sid)

    except Exception as e:
        current_app.logger.error(f"Error occured during call: {str(e)}") 
