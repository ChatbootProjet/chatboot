from flask import Flask, render_template, request, jsonify
import requests

# تهيئة Flask
app = Flask(__name__)

# قائمة لتخزين الرسائل السابقة
conversation_history = []

def get_current_date_from_web():
    try:
        response = requests.get("http://worldtimeapi.org/api/timezone/Etc/UTC")
        if response.status_code == 200:
            data = response.json()
            date_time = data["datetime"][:10]  # استخراج التاريخ فقط (YYYY-MM-DD)
            return f"التاريخ اليوم هو: {date_time}"
        else:
            return "عذرًا، حدث خطأ أثناء الحصول على التاريخ."
    except Exception as e:
        print(f"خطأ في الحصول على التاريخ من المصدر الخارجي: {e}")
        return "عذرًا، حدث خطأ أثناء الحصول على التاريخ."

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/send_message", methods=["POST"])
def send_message():
    user_input = request.form["user_input"]
    bot_response = send_message_to_gemini(user_input)
    return jsonify({"user_input": user_input, "bot_response": bot_response})

def send_message_to_gemini(message):
    conversation_history.append({"role": "user", "parts": [{"text": message}]})
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "contents": conversation_history
    }
    params = {
        "key": "AIzaSyByJMeVo9xbPAp_n-Iy1c5I8IBpD-lSLV8"  # استبدل بمفتاح API الخاص بك
    }
    try:
        response = requests.post(url, headers=headers, json=data, params=params)
        if response.status_code == 200:
            try:
                # التحقق من بنية الاستجابة
                bot_response = response.json()["candidates"][0]["content"]["parts"][0]["text"]
                conversation_history.append({"role": "model", "parts": [{"text": bot_response}]})
                return bot_response
            except KeyError as e:
                # إذا كانت الاستجابة لا تحتوي على المفاتيح المتوقعة
                print(f"خطأ في بنية الاستجابة: {e}")
                print(f"الاستجابة الكاملة: {response.json()}")
                return "عذرًا، حدث خطأ في معالجة الرد. يرجى المحاولة لاحقًا."
        else:
            print(f"خطأ في الطلب: {response.status_code}, {response.text}")
            return f"عذرًا، حدث خطأ أثناء معالجة طلبك. (رمز الخطأ: {response.status_code})"
    except Exception as e:
        print(f"خطأ عام: {e}")
        return "عذرًا، حدث خطأ أثناء معالجة طلبك."

if __name__ == "__main__":
    app.run(debug=True)
