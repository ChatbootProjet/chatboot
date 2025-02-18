from flask import Flask, render_template, request, jsonify
import requests
from langdetect import detect, LangDetectException
from config import SYSTEM_PROMPT, GOOGLE_SEARCH_API_KEY, GOOGLE_SEARCH_ENGINE_ID

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
    bot_response = process_user_input(user_input)
    return jsonify({"user_input": user_input, "bot_response": bot_response})

def process_user_input(user_input):
    # Detect language of the input
    try:
        language = detect(user_input)
    except LangDetectException:
        language = "en"  # Default to English if detection fails

    # Check if the user is asking for time or date
    if "time" in user_input.lower() or "date" in user_input.lower():
        return get_time_and_date(language)

    # Check if the user wants to search the web
    elif "search" in user_input.lower() or "find" in user_input.lower() or "lookup" in user_input.lower():
        return search_web(user_input, language)

    else:
        return send_message_to_gemini(user_input, language)

def send_message_to_gemini(message, language):
    global conversation_history

    # Add user message to conversation history
    conversation_history.append({"role": "user", "parts": [{"text": message}]})

    # Add System Prompt at the beginning if the conversation is empty
    if len(conversation_history) == 1:
        conversation_history.insert(0, {"role": "model", "parts": [{"text": SYSTEM_PROMPT}]})

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {"Content-Type": "application/json"}
    data = {"contents": conversation_history}
    params = {"key": "AIzaSyByJMeVo9xbPAp_n-Iy1c5I8IBpD-lSLV8"}  # Replace with your Gemini API key

    try:
        response = requests.post(url, headers=headers, json=data, params=params)
        if response.status_code == 200:
            try:
                bot_response = response.json()["candidates"][0]["content"]["parts"][0]["text"]

                # Ensure the bot identifies itself as Ai-O
                bot_response = bot_response.replace("Gemini", "Ai-O").replace("Google", "AIO")

                # Translate the response to the detected language if needed
                if language != "en":
                    bot_response = translate_text(bot_response, language)

                # Add bot response to conversation history
                conversation_history.append({"role": "model", "parts": [{"text": bot_response}]})
                return bot_response
            except KeyError as e:
                print(f"Error in response structure: {e}")
                return "Sorry, there was an error processing the response. Please try again later. ❌"
        else:
            return f"Sorry, there was an error processing your request. (Error code: {response.status_code}) ❌"
    except Exception as e:
        print(f"General error: {e}")
        return "Sorry, there was an error processing your request. ❌"

def get_time_and_date(language):
    # Use WorldTimeAPI to fetch current time and date
    url = "http://worldtimeapi.org/api/timezone/Etc/UTC"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            current_time = data.get("datetime", "")
            timezone = data.get("timezone", "UTC")
            if language == "ar":
                return f"الوقت الحالي هو: {current_time[:19]} (بالتوقيت العالمي UTC)."
            elif language == "fr":
                return f"L'heure actuelle est: {current_time[:19]} (Heure universelle UTC)."
            else:
                return f"The current time is: {current_time[:19]} (UTC)."
        else:
            return "Sorry, there was an error fetching the current time. Please try again later. ❌"
    except Exception as e:
        print(f"Time API error: {e}")
        return "Sorry, there was an error fetching the current time. Please try again later. ❌"

def search_web(query, language):
    # Use Google Custom Search JSON API to search the web
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": GOOGLE_SEARCH_API_KEY,
        "cx": GOOGLE_SEARCH_ENGINE_ID
    }
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            items = data.get("items", [])
            if items:
                result = "<div class='search-results'>"
                for i, item in enumerate(items[:3], start=1):  # Show top 3 results
                    title = item.get("title", "No title")
                    link = item.get("link", "#")
                    snippet = item.get("snippet", "No description available.")
                    result += f"""
                        <div class='search-result'>
                            <a href='{link}' target='_blank'><h3>{title}</h3></a>
                            <p>{snippet}</p>
                        </div>
                    """
                result += "</div>"
                if language != "en":
                    result = translate_text(result, language)
                return result
            else:
                return "I couldn't find any relevant results for your query. 😔"
        else:
            return "Sorry, there was an error while searching the web. Please try again later. ❌"
    except Exception as e:
        print(f"Web search error: {e}")
        return "Sorry, there was an error while searching the web. Please try again later. ❌"

def translate_text(text, target_language):
    # Use Google Translate API or another translation service
    url = "https://translation.googleapis.com/language/translate/v2"
    params = {
        "q": text,
        "target": target_language,
        "key": GOOGLE_SEARCH_API_KEY
    }
    try:
        response = requests.post(url, params=params)
        if response.status_code == 200:
            translated_text = response.json()["data"]["translations"][0]["translatedText"]
            return translated_text
        else:
            return text  # Return original text if translation fails
    except Exception as e:
        print(f"Translation error: {e}")
        return text

if __name__ == "__main__":
    app.run(debug=True)
