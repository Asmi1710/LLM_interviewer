from twilio.rest import Client

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

    client = Client(current_app.config('TWILIO_ACCOUNT_SID'), current_app.config('TWILIO_AUTH_TOKEN'))

    call = client.calls.create(
        twiml=f'''<Response>
            <Say>{introduction}</Say>
            <Redirect method="POST">
                https://your-ngrok-or-domain.com/interviews/create?candidate_id={candidate_id}&job_id={job_id}&role={request.get('role')}
            </Redirect>
            </Response>''',
        to=mobile_number,
        from_=current_app.config['TWILIO_PHONE_NUMBER']
    )

    return {"status": "interview started", "call_sid": call.sid}

    # conduct the interview
    # record everything in recordings and trascriptions as:
    # interview = { 'question':'', 'answer': '', 'score':'', 'recordings':''}
    # _interview_repository().create(**interview)
