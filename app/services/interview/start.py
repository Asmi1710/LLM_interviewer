import time, hmac, hashlib
from twilio.rest import Client
from xml.sax.saxutils import escape
from urllib.parse import urlencode

from flask import current_app
from app.repositories import _candidate_repository, _job_repository
from app.exceptions import InvalidDataError
from app.constants.questions import introductory_question, python_questions

def call(request):
    candidate_id = request.get('candidate_id')
    job_id = request.get('job_id')
    candidate = ~_candidate_repository().get(candidate_id)
    if not candidate:
        raise InvalidDataError('Invalid request', data="Invalid candidate_id")
    job = ~_job_repository().get(job_id)
    if not job:
        raise InvalidDataError('Invalid request', data="Invalid job_id")
    
    # needs to be verified for twilio trial account using https://console.twilio.com/us1/develop/phone-numbers/manage/verified
    mobile_number = candidate.mobile_number 
    name = candidate.full_name
    introduction = introductory_question(name)

    # make a call to candidate with basic introduction
    # record the answer and score it
    # generate next question and continue this loop for 5 times 
    # after interview is created, repo: after_create: calculate overall score (avg) & summary about the candidate
    # later make provision for additional queries in the call using the request body
    # also handle if the user interrupts

    client = Client(current_app.config['TWILIO_ACCOUNT_SID'], current_app.config['TWILIO_AUTH_TOKEN'])
    params = {
        "candidate_id": candidate_id,
        "job_id": job_id,
        "role": request.get('role')  
    }
    # Escape the & symbols for XML
    redirect_url = escape(f"{current_app.config['AI_INTERVIEWER_BASE_URL']}/api/v1/interviews/create?{urlencode(params)}")

    ts = str(int(time.time()))
    message = f"{introduction}{ts}".encode("utf-8")
    signature = hmac.new(current_app.config['HMAC_SECRET_KEY'].encode(), message, hashlib.sha256).hexdigest()
    audio_prams={
        "text": introduction,
        "ts": ts,
        "sig": signature
    }
    audio_url = f"{current_app.config['AI_INTERVIEWER_BASE_URL']}/api/v1/interviews/audio?{urlencode(audio_prams)}"
    # call = client.calls.create(
    #     twiml=f'''<Response>
    #         <Play>{audio_url}</Play>
    #         <Redirect method="POST">
    #             {redirect_url}
    #         </Redirect>
    #         </Response>''',
    #     to=mobile_number,
    #     from_=current_app.config['TWILIO_PHONE_NUMBER']
    # )
    call = client.calls.create(
        twiml=f'''<Response>
            <Play>{audio_url}</Play>
            <Record 
                action="{redirect_url}"
                method="POST"
                maxLength="30"
                timeout="2"
                transcribe="false"
                playBeep="true"
                />
            </Response>''',
        to=mobile_number,
        from_=current_app.config['TWILIO_PHONE_NUMBER']
    )

    return {"status": "interview started", "call_sid": call.sid}

    # conduct the interview
    # record everything in recordings and trascriptions as:
    # interview = { 'question':'', 'answer': '', 'score':'', 'recordings':''}
    # _interview_repository().create(**interview)
