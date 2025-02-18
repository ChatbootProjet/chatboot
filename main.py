from flask import Flask, render_template, request, jsonify
import requests
from config import SYSTEM_PROMPT  # Import the system prompt from config.py

# Initialize Flask
app = Flask(__name__)

# List to store previous messages
conversation_history = []

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/send_message", methods=["POST"])
def send_message():
    user_input = request.form["user_input"]
    bot_response = send_message_to_gemini(user_input)
    return jsonify({"user_input": user_input, "bot_response": bot_response})

def send_message_to_gemini(message):
    global conversation_history

    # Add user message to conversation history
    conversation_history.append({"role": "user", "parts": [{"text": message}]})

    # Add System Prompt at the beginning if the conversation is empty
    if len(conversation_history) == 1:
        conversation_history.insert(0, {"role": "model", "parts": [{"text": SYSTEM_PROMPT}]})

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": conversation_history
    }
    params = {
        "key": "AIzaSyByJMeVo9xbPAp_n-Iy1c5I8IBpD-lSLV8"  # Replace with your API key
    }
    try:
        response = requests.post(url, headers=headers, json=data, params=params)
        if response.status_code == 200:
            try:
                # Check response structure
                bot_response = response.json()["candidates"][0]["content"]["parts"][0]["text"]

                # Ensure the bot identifies itself as Ai-O
                bot_response = bot_response.replace("Gemini", "Ai-O").replace("gemini", "Ai-O")
                bot_response = bot_response.replace("Google", "AIO").replace("google", "AIO")

                # Add bot response to conversation history
                conversation_history.append({"role": "model", "parts": [{"text": bot_response}]})
                return bot_response
            except KeyError as e:
                # If the response doesn't contain the expected keys
                print(f"Error in response structure: {e}")
                print(f"Full response: {response.json()}")
                return "Sorry, there was an error processing the response. Please try again later. ❌"
        elif response.status_code == 400:
            # Handle Bad Request (400) error
            error_message = response.json().get("error", {}).get("message", "Unknown error.")
            print(f"Error 400: {error_message}")
            return f"Sorry, there was an error with the request. Details: {error_message} ❌"
        else:
            # Handle other errors
            print(f"Request error: {response.status_code}, {response.text}")
            return f"Sorry, there was an error processing your request. (Error code: {response.status_code}) ❌"
    except Exception as e:
        print(f"General error: {e}")
        return "Sorry, there was an error processing your request. ❌"

@app.route("/clear_context", methods=["POST"])
def clear_context():
    global conversation_history
    conversation_history = []  # Clear current context
    return jsonify({"status": "success", "message": "Context cleared successfully."})

if __name__ == "__main__":
    app.run(debug=True)
