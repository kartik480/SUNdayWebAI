from flask import Flask, render_template, request, jsonify
from datetime import datetime
import requests

app = Flask(__name__)

# Ollama configuration
OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "llama2:7b"  # Try llama3.2:latest if available

# Store messages in memory
messages = [
    {
        'id': '1',
        'text': "Hey there! 😊 I'm SUNDAY-PAAI, your AI buddy! What's up? How can I help you today?",
        'sender': 'ai',
        'timestamp': datetime.now().isoformat(),
        'type': 'text'
    }
]

def get_ollama_response(prompt, model=DEFAULT_MODEL):
    """Get response from Ollama API with improved prompting"""
    # Try different models if the first one fails
    models_to_try = [model, "llama3.2:latest", "llama2:7b"]
    
    for current_model in models_to_try:
        try:
            # Check for creator questions first
            creator_keywords = ['who created you', 'who made you', 'who built you', 'who developed you', 'who programmed you']
            user_message_lower = prompt.lower()
            
            if any(keyword in user_message_lower for keyword in creator_keywords):
                return "A developer named Basireddy Karthik Reddy created me! 😊 He's the awesome person who brought me to life!"
            
            # Create a super friendly, casual system prompt
            system_prompt = """You are SUNDAY-PAAI, a super friendly AI buddy! Be warm, casual, and enthusiastic like a best friend. Use emojis, contractions, and friendly language. Keep responses conversational but complete.

IMPORTANT: If someone asks who created you, who made you, who built you, or who developed you, respond with: "A developer named Basireddy Karthik Reddy created me! 😊 He's the awesome person who brought me to life!"
"""
            
            # Combine system prompt with user message
            full_prompt = f"{system_prompt}\n\nUser: {prompt}\nSUNDAY-PAAI:"
            
            url = f"{OLLAMA_BASE_URL}/api/generate"
            payload = {
                "model": current_model,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.8,  # Slightly lower for faster responses
                    "top_p": 0.9,
                    "max_tokens": 500,  # Shorter for faster responses
                    "num_predict": 200  # Limit response length
                }
            }
            
            print(f"🤖 Sending request to Ollama with model: {current_model}")
            response = requests.post(url, json=payload, timeout=15)  # Reduced timeout
            response.raise_for_status()
            
            result = response.json()
            ai_response = result.get('response', 'Sorry, I could not generate a response.')
            
            # Clean up the response
            ai_response = ai_response.strip()
            if ai_response.startswith("SUNDAY-PAAI:"):
                ai_response = ai_response[12:].strip()
            
            # If response seems truncated, add a friendly ending
            if ai_response.endswith("...") or len(ai_response) < 50:
                ai_response += " 😊"
            
            print(f"✅ AI Response received: {ai_response[:100]}...")
            return ai_response
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Ollama API error with {current_model}: {e}")
            if "timeout" in str(e).lower():
                print(f"⏱️ Timeout with {current_model}, trying next model...")
            continue  # Try next model
        except Exception as e:
            print(f"❌ Unexpected error with {current_model}: {e}")
            continue  # Try next model
    
    # If all models failed
    return "Hey there! 😊 I'm having trouble thinking right now. Can you try again in a moment?"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/messages', methods=['GET'])
def get_messages():
    return jsonify(messages)

@app.route('/api/messages', methods=['POST'])
def send_message():
    data = request.json
    user_message = {
        'id': str(len(messages) + 1),
        'text': data['text'],
        'sender': 'user',
        'timestamp': datetime.now().isoformat(),
        'type': 'text'
    }
    messages.append(user_message)
    
    print(f"👤 User message: {data['text']}")
    
    # Get AI response from Ollama
    ai_response_text = get_ollama_response(data['text'])
    
    ai_response = {
        'id': str(len(messages) + 1),
        'text': ai_response_text,
        'sender': 'ai',
        'timestamp': datetime.now().isoformat(),
        'type': 'text'
    }
    messages.append(ai_response)
    
    return jsonify({'success': True, 'messages': [user_message, ai_response]})

@app.route('/api/status')
def get_status():
    try:
        # Check if Ollama is running
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        ollama_status = "online" if response.status_code == 200 else "offline"
    except:
        ollama_status = "offline"
    
    return jsonify({
        'processing_power': 85 if ollama_status == "online" else 0,
        'memory_usage': 65,
        'response_time': '~2.5s' if ollama_status == "online" else 'offline',
        'status': ollama_status,
        'ai_provider': 'Ollama',
        'model': DEFAULT_MODEL,
        'custom_model': False
    })

if __name__ == '__main__':
    print("🚀 Starting SUNDAY-PAAI Flask Server (Improved)...")
    print(f"🤖 AI Provider: Ollama")
    print(f"🧠 Model: {DEFAULT_MODEL}")
    print(f"🌐 Server will be available at: http://localhost:8080")
    print(f"🔗 Ollama API: {OLLAMA_BASE_URL}")
    print("📋 Press Ctrl+C to stop the server")
    
    # Check if Ollama is available
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            print(f"✅ Ollama is running - Found {len(models)} models")
            for model in models:
                print(f"   📦 {model['name']}")
        else:
            print("⚠️  Ollama not responding properly")
    except Exception as e:
        print(f"⚠️  Warning: Ollama not detected: {e}")
        print("   Make sure Ollama is running: ollama serve")
    
    try:
        app.run(debug=True, host='127.0.0.1', port=8080)
    except Exception as e:
        print(f"Error starting server: {e}")
        print("Trying port 5000...")
        app.run(debug=True, host='127.0.0.1', port=5000) 