from flask import current_app

def call(user_response, prev_question, next_question): 
    client = current_app.extensions['openai_client']
    try:
        prompt = (
            f"Act like a friendly and professional interviewer. Read user's response to previous question and acknowledge it briefly to make the conversation feel natural and engaging. "
            f"Then, smoothly transition into next question in a conversational tone."
            f"Keep the response concise (no more than 2 short sentences). "
            f"\nPrevious question: {prev_question}"
            f"\nUser's reply: {user_response}"
            f"\nNext question: {next_question}"
        )
        # prompt=(f"Create concise response for user's reply and ask next question. Statement should not exceed more that 2 small sentences."
        #     f"previous question: {prev_question}"
        #     f"user's reply:{user_response}"
        #     f"next question: {next_question}")
        ai_response = client.responses.create(
            model="gpt-4.1-mini",
            input= prompt
        )
        return ai_response.output[0].content[0].text
    except Exception as e:
        current_app.logger.error(f"Error occurred during response generation: {str(e)}")
        return next_question