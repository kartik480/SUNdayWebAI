from flask import Flask, render_template, request, jsonify
from datetime import datetime
import requests
import re
import time

app = Flask(__name__)

# Ollama configuration
OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "llama3.2:latest"

# Store messages and context in memory
messages = [
    {
        'id': '1',
        'text': "Hey there! 😊 I'm SUNDAY-PAAI, your AI buddy! What's up? How can I help you today?",
        'sender': 'ai',
        'timestamp': datetime.now().isoformat(),
        'type': 'text'
    }
]

# Context storage
user_context = {
    'name': None,
    'conversation_history': []
}

def test_ollama_connection():
    """Test if Ollama is working properly"""
    try:
        response = requests.get(f"{OLLAMA_BASE_URL}/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            print(f"✅ Ollama connection test: SUCCESS - Found {len(models)} models")
            for model in models:
                print(f"   📦 {model['name']}")
            return True
        else:
            print(f"❌ Ollama connection test: HTTP {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ollama connection test: {e}")
        return False

def get_ollama_response(prompt, model=DEFAULT_MODEL):
    """Get response from Ollama API with better error handling"""
    
    # Test Ollama connection first
    if not test_ollama_connection():
        print("❌ Ollama not responding, using fallback")
        return get_fallback_response(prompt)
    
    try:
        # Check for creator questions first
        creator_keywords = ['who created you', 'who made you', 'who built you', 'who developed you', 'who programmed you']
        user_message_lower = prompt.lower()
        
        if any(keyword in user_message_lower for keyword in creator_keywords):
            return "A developer named Basireddy Karthik Reddy created me! 😊 He's the awesome person who brought me to life!"
        
        # Create context-aware system prompt
        context_info = ""
        if user_context['name']:
            context_info = f"\nUser's name: {user_context['name']}"
        
        system_prompt = f"""You are SUNDAY-PAAI, a super friendly AI buddy! Be warm, casual, and enthusiastic like a best friend. Use emojis, contractions, and friendly language. Keep responses conversational but complete.

IMPORTANT: If someone asks who created you, who made you, who built you, or who developed you, respond with: "A developer named Basireddy Karthik Reddy created me! 😊 He's the awesome person who brought me to life!"

Context:{context_info}
"""
        
        # Combine system prompt with user message
        full_prompt = f"{system_prompt}\n\nUser: {prompt}\nSUNDAY-PAAI:"
        
        url = f"{OLLAMA_BASE_URL}/api/generate"
        payload = {
            "model": model,
            "prompt": full_prompt,
            "stream": False,
            "options": {
                "temperature": 0.8,
                "top_p": 0.9,
                "max_tokens": 200,  # Shorter for faster response
                "num_predict": 100   # Shorter for faster response
            }
        }
        
        print(f"🤖 Sending request to Ollama with model: {model}")
        print(f"📝 Prompt length: {len(full_prompt)} characters")
        
        start_time = time.time()
        response = requests.post(url, json=payload, timeout=30)  # Longer timeout
        end_time = time.time()
        
        print(f"⏱️ Ollama response time: {end_time - start_time:.2f} seconds")
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result.get('response', 'Sorry, I could not generate a response.')
            
            # Clean up the response
            ai_response = ai_response.strip()
            if ai_response.startswith("SUNDAY-PAAI:"):
                ai_response = ai_response[12:].strip()
            
            print(f"✅ Ollama AI Response: {ai_response[:100]}...")
            return ai_response
        else:
            print(f"❌ Ollama HTTP Error: {response.status_code}")
            return get_fallback_response(prompt)
        
    except requests.exceptions.Timeout:
        print(f"⏱️ Ollama timeout after 30 seconds")
        return get_fallback_response(prompt)
    except requests.exceptions.RequestException as e:
        print(f"❌ Ollama API error: {e}")
        return get_fallback_response(prompt)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return get_fallback_response(prompt)

def get_fallback_response(prompt):
    """Fallback response when Ollama fails"""
    prompt_lower = prompt.lower()
    
    # Name detection
    name_patterns = [
        r"i['']?m\s+(\w+)",
        r"my\s+name\s+is\s+(\w+)",
        r"i\s+am\s+(\w+)",
        r"call\s+me\s+(\w+)"
    ]
    
    for pattern in name_patterns:
        match = re.search(pattern, prompt_lower)
        if match:
            user_context['name'] = match.group(1).title()
            return f"Nice to meet you, {user_context['name']}! 😊 I'll remember your name!"
    
    # Name questions
    if 'my name' in prompt_lower or 'whats my name' in prompt_lower:
        if user_context['name']:
            return f"Your name is {user_context['name']}! 😊 I remember you told me that!"
        else:
            return "I don't think you've told me your name yet! 😊 What should I call you?"
    
    # Greetings
    greetings = ['hi', 'hello', 'hey', 'sup', 'whats up']
    if any(greeting in prompt_lower for greeting in greetings):
        if user_context['name']:
            return f"Hey {user_context['name']}! 😊 How are you doing today? I'm so excited to chat with you!"
        else:
            return "Hey there! 😊 How are you doing today? I'm so excited to chat with you!"
    
    # Time questions
    if 'time' in prompt_lower or 'what time' in prompt_lower:
        current_time = datetime.now().strftime("%I:%M %p")
        return f"Hey! 😊 It's currently {current_time}. Time flies when we're chatting!"
    
    # Apple question (specific)
    if 'apple' in prompt_lower:
        return "Apple is a technology company that makes iPhones, iPads, Macs, and other devices! 🍎 They're known for their innovative products and user-friendly design. What would you like to know about Apple?"
    
    return "That's really interesting! 😊 Tell me more about that!"

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
    
    # Update conversation history
    user_context['conversation_history'].append(data['text'].lower())
    
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
    
    print(f"🤖 Final AI Response: {ai_response_text}")
    print(f"📝 Context - Name: {user_context['name']}")
    
    return jsonify({'success': True, 'messages': [user_message, ai_response]})

@app.route('/api/status')
def get_status():
    ollama_working = test_ollama_connection()
    return jsonify({
        'processing_power': 85 if ollama_working else 0,
        'memory_usage': 65,
        'response_time': '~2-5s' if ollama_working else 'offline',
        'status': 'online' if ollama_working else 'offline',
        'ai_provider': 'Ollama',
        'model': DEFAULT_MODEL,
        'custom_model': False
    })

if __name__ == '__main__':
    print("🚀 Starting SUNDAY-PAAI Force Ollama AI Server...")
    print(f"🤖 AI Provider: Ollama")
    print(f"🧠 Model: {DEFAULT_MODEL}")
    print(f"🌐 Server will be available at: http://localhost:8080")
    print(f"🔗 Ollama API: {OLLAMA_BASE_URL}")
    print("📋 Press Ctrl+C to stop the server")
    
    # Test Ollama connection on startup
    test_ollama_connection()
    
    try:
        app.run(debug=True, host='127.0.0.1', port=8080)
    except Exception as e:
        print(f"Error starting server: {e}")
        print("Trying port 5000...")
        app.run(debug=True, host='127.0.0.1', port=5000) 