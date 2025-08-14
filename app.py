from flask import Flask, jsonify, request
import google.generativeai as genai
import os
from dotenv import load_dotenv


#load the env variables
load_dotenv()

#initialize the flask app
app = Flask(__name__)

#configure the gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY')) #type: ignore
model = genai.GenerativeModel('gemini-2.5-flash')

@app.route('/health')
def health():
    return jsonify({"status": "healthy", "message": "AI agent API is running!"})

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '')

        if not user_message:
            return jsonify({"error":"No message provided"}), 400

        #generate response using gemini
        response = model.generate_content(user_message)
        ai_response = response.text

        return jsonify({
            "user_message": user_message,
            "ai_response": ai_response,
            "status": "success"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
