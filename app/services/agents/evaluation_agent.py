from flask import current_app
from app.repositories import _interview_repository
import json

def call(interview, questions):
    client = current_app.extensions['openai_client']
    new_transcript = []
    complete_transcript = ""
    total_score= 0
    for idx, record in enumerate(interview.transcript):
        expected_ans = questions[idx].get('expected_answer')
        interview_transcript= f"Question: {record.get('question')} \n Expected answer: {expected_ans} \n Candidate's Answer: {record.get('answer_txt')}"
        prompt = (f"You are an AI interview evaluator. For each question, you're given: question asked, expected answer and candidate's actual answer. "
                  f"Your task is to evaluate the candidate’s knowledge and suitability for the role taking expected answer as reference."
                  f"Return only a score out of 100, as a float in this exact JSON format WITHOUT EXPLANATION OR CODE BLOCK SYNTAX \n" '{"score": <score>}\n\n'
                  f"{interview_transcript}")
        
        ai_response = client.responses.create(
            model="gpt-4.1-mini",
            input= prompt
        )
        score_text = ai_response.output[0].content[0].text
        if score_text:
            score = (json.loads(score_text))['score']
        else:
            score = 0.0 
        total_score += score
        record['score'] = score
        new_transcript.append(record)
        complete_transcript += f"Question: {record.get('question')} \n Candidate's Answer: {record.get('answer_txt')} Score:{score} \n\n"

    overall_prompt = (f"You are an AI interview evaluator. For each question, you're given: question asked, candidate's actual answer and it's score "
            f"Your task is to evaluate the candidate’s knowledge and suitability for the role taking complete interview into account and give a summary"
            f"Evaluation summary must be brief not exceeding two sentences.\n\n"
            f"{complete_transcript}")
        
    ai_summary_response = client.responses.create(
        model="gpt-4.1-mini",
        input= overall_prompt
    )
    ai_summary = ai_summary_response.output[0].content[0].text
    avg_score = round(total_score/ len(new_transcript), 2)
    update_request= {'transcript': new_transcript, 'overall_score': avg_score, 'summary': ai_summary}
    _interview_repository().update(interview, update_request)
    return 
