from twilio.twiml.voice_response import VoiceResponse
import hmac, hashlib, time
from urllib.parse import urlencode

from flask import current_app, Response
from app.constants.questions import questions_list
from app.repositories import _interview_repository
from app.helpers.interview_helper import save_interview_session, load_interview_session, delete_interview_session
from app.services.agents import transcribing_agent, reply_generating_agent, evaluation_agent

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
                "role": role,
                "questions": questions_list.get(role) or ['Please tell me about yourself.', 'Give me breif description of your work experience.'],
                "transcript": []
            }
            current_app.logger.info(f"session :{session}")

        index = session["question_index"]
        questions = session["questions"]
        response = VoiceResponse()

        # Save previous answer
        if recording_url and index > 0:
            current_app.logger.info(f" recording_url: {recording_url}")
            transcript = transcribing_agent.call(recording_url)
            current_app.logger.info(f" transcript: {transcript}")
            session["transcript"].append({
                "question": questions[index - 1].get('question'),
                "answer_url": recording_url,
                "answer_txt": transcript
            })
        elif recording_url and index == 0:
            transcript = transcribing_agent.call(recording_url)

        # Ask next question
        if index < len(questions):
            next_question = questions[index].get('question')
            current_app.logger.info(f" next_question: {next_question}")
            if index == 0:
                ai_reply = reply_generating_agent.call(transcript, 'Hello. This is a recruitment call for conducting the telephonic interview. How are you doing today?', next_question)
            else:
                ai_reply = reply_generating_agent.call(transcript, questions[index - 1].get('question'), next_question)  

            current_app.logger.info(f" ai_reply: {ai_reply}")
            ts = str(int(time.time()))
            message = f"{ai_reply}{ts}".encode("utf-8")
            signature = hmac.new(current_app.config['HMAC_SECRET_KEY'].encode(), message, hashlib.sha256).hexdigest()

            audio_prams={
                "text": ai_reply,
                "ts": ts,
                "sig": signature
            }
            audio_url = f"{current_app.config['AI_INTERVIEWER_BASE_URL']}/api/v1/interviews/audio?{urlencode(audio_prams)}"
            # audio_url_escaped = escape(audio_url)
            current_app.logger.info(f" audio_url: {audio_url}")
            # Play AI question and record user's answer
            response.play(audio_url)

            record_params = {
                "candidate_id": candidate_id,
                "job_id": job_id,
                "role": role
            }
            record_action_url = f"{current_app.config['AI_INTERVIEWER_BASE_URL']}/api/v1/interviews/create?{urlencode(record_params)}"
            response.record(
                action=record_action_url,
                method='POST',
                max_length=30,
                transcribe=False,
                timeout=2,
            )
            current_app.logger.info(f" return from recording send")

            session["question_index"] += 1
            save_interview_session(call_sid, session)
        else:
            # End of interview
            ts = str(int(time.time()))
            message = f"{"Thank you. Your interview is now complete."}{ts}".encode("utf-8")
            signature = hmac.new(current_app.config['HMAC_SECRET_KEY'].encode(), message, hashlib.sha256).hexdigest()

            audio_prams={
                "text": "Thank you. Your interview is now complete.",
                "ts": ts,
                "sig": signature
            }
            audio_url = f"{current_app.config['AI_INTERVIEWER_BASE_URL']}/api/v1/interviews/audio?{urlencode(audio_prams)}"
            response.play(audio_url)
            params = {
                "candidate_id": session["candidate_id"],
                'job_id': session["job_id"],
                "transcript": session["transcript"],
                "role": session['role']
            }
            interview = _interview_repository().create(**params)
            current_app.logger.info(f"Interview ends")
            evaluation_agent(interview, session["questions"])
            delete_interview_session(call_sid)

        return Response(str(response), mimetype='text/xml') 
    
    except Exception as e:
        current_app.logger.error(f"Error occured during call: {str(e)}") 
