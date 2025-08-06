from flask import current_app
import json

def call(user_response, prev_question, next_question, prev_idx, next_idx): 
    client = current_app.extensions['openai_client']
    try:
        prompt = (
            "You are a friendly and professional AI interviewer.\n"
            "Respond based on the user's reply, strictly following the rules below:\n"
            "RULES:\n"
            "1. If the user's reply asks for repetition or clarification (e.g., 'Can you repeat?', 'I didn’t understand', 'Sorry?', etc.), do NOT explain or answer. Do NOT move to the next question.\n"
            "   Instead, respond politely (e.g., 'Sure, let me repeat it for you:' or 'No problem, here it is again:'), then restate the previous question.\n\n"

            "2. If the user's reply is 'I don’t know', 'Not sure', or similar, do NOT explain or answer ANY question. Just acknowledge briefly (e.g., 'That's okay.' or 'No worries.') and move on by asking the next question directly.\n\n"

            "3. If the user's reply answers the previous question, acknowledge it briefly (e.g., 'Thanks for sharing.' or 'Got it.') and then ask the next question in a smooth, conversational tone.\n\n"

            "4. If the reply is unclear or off-topic, ask the user to clarify their answer to the previous question.\n\n"

            "Your output must be a valid JSON (Use double quotes for all keys and string values) with exactly two keys:\n"
            "1. 'index' → the index number of the question being asked in the reply.\n"
            "2. 'reply' → the message to the user. Keep it polite and concise (max 2 short sentences).\n\n"

            "IMPORTANT:\n"
            "- NEVER answer the previous or next question yourself even when asked to explain the question.\n"
            "- ONLY move to the next question if the user answered or said they don’t know.\n"
            "- ONLY reply in dictionary format as described.\n\n"

            f"Previous question: {prev_question} and index={prev_idx}\n"
            f"User's reply: {user_response}\n"
            f"Next question: {next_question} and index={next_idx}"
        )
        # prompt=(f"Create concise response for user's reply and ask next question. Statement should not exceed more that 2 small sentences."
        #     f"previous question: {prev_question}"
        #     f"user's reply:{user_response}"
        #     f"next question: {next_question}")
        ai_response = client.responses.create(
            model="gpt-4.1-mini",
            input= prompt
        )

        response_dict = json.loads(ai_response.output[0].content[0].text)
        return response_dict
    except Exception as e:
        current_app.logger.error(f"Error occurred during response generation: {str(e)}")
        return next_question


