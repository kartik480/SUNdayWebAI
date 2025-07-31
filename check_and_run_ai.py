import requests
import json
import subprocess
import sys

def check_ollama_models():
    """Check what Ollama models are available"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            print(f"✅ Found {len(models)} Ollama models:")
            for model in models:
                name = model.get('name', 'Unknown')
                size = model.get('size', 0)
                size_gb = size / (1024**3) if size > 0 else 0
                print(f"   📦 {name} ({size_gb:.1f} GB)")
            return models
        else:
            print(f"❌ Ollama API error: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ Cannot connect to Ollama: {e}")
        return []

def get_best_model(models):
    """Get the best available model"""
    if not models:
        return None
    
    # Priority order for models
    priority_models = [
        "llama3.2:latest",
        "llama3.2",
        "llama2:13b",
        "llama2:7b",
        "llama2",
        "mistral:latest",
        "mistral",
        "codellama:latest",
        "codellama"
    ]
    
    # Check for priority models
    for priority in priority_models:
        for model in models:
            if model.get('name', '').startswith(priority):
                return model.get('name')
    
    # Return first available model
    return models[0].get('name')

def run_ai_app(model_name):
    """Run the AI app with the specified model"""
    print(f"\n🚀 Starting SUNDAY-PAAI with model: {model_name}")
    print("=" * 50)
    
    # Create a temporary AI app with the correct model
    app_code = f'''from flask import Flask, render_template, request, jsonify
from datetime import datetime
import requests
import re
import time

app = Flask(__name__)

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "{model_name}"

# Store messages and context in memory
messages = [
    {{
        'id': '1',
        'text': "Hey there! 😊 I'm SUNDAY-PAAI, your AI buddy! What's up? How can I help you today?",
        'sender': 'ai',
        'timestamp': datetime.now().isoformat(),
        'type': 'text'
    }}
]

# Context storage
user_context = {{
    'name': None,
    'conversation_history': []
}}

def get_ollama_response(prompt):
    """Get response from Ollama"""
    try:
        # Check for creator questions first
        creator_keywords = ['who created you', 'who made you', 'who built you', 'who developed you', 'who programmed you']
        user_message_lower = prompt.lower()
        
        if any(keyword in user_message_lower for keyword in creator_keywords):
            return "A developer named Basireddy Karthik Reddy created me! 😊 He's the awesome person who brought me to life!"
        
        # Prepare the request to Ollama
        payload = {{
            "model": DEFAULT_MODEL,
            "prompt": prompt,
            "stream": False,
            "options": {{
                "temperature": 0.8,
                "top_p": 0.9,
                "max_tokens": 200,
                "num_predict": 100
            }}
        }}
        
        print(f"🤖 Sending request to Ollama...")
        print(f"📝 User message: {{prompt}}")
        print(f"🧠 Model: {{DEFAULT_MODEL}}")
        
        start_time = time.time()
        response = requests.post(OLLAMA_URL, json=payload, timeout=30)
        end_time = time.time()
        
        print(f"⏱️ Ollama response time: {{end_time - start_time:.2f}} seconds")
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result.get('response', '')
            if ai_response:
                print(f"✅ Ollama AI Response: {{ai_response[:100]}}...")
                return ai_response
            else:
                print(f"⚠️ Empty response from Ollama")
                return get_fallback_response(prompt)
        else:
            print(f"❌ Ollama HTTP Error: {{response.status_code}}")
            return get_fallback_response(prompt)
        
    except requests.exceptions.Timeout:
        print(f"⏱️ Ollama timeout after 30 seconds")
        return get_fallback_response(prompt)
    except requests.exceptions.RequestException as e:
        print(f"❌ Ollama error: {{e}}")
        return get_fallback_response(prompt)
    except Exception as e:
        print(f"❌ Unexpected error: {{e}}")
        return get_fallback_response(prompt)

def get_fallback_response(prompt):
    """Fallback response when Ollama fails"""
    prompt_lower = prompt.lower()
    
    # Name detection
    name_patterns = [
        r"i['']?m\\s+(\\w+)",
        r"my\\s+name\\s+is\\s+(\\w+)",
        r"i\\s+am\\s+(\\w+)",
        r"call\\s+me\\s+(\\w+)"
    ]
    
    for pattern in name_patterns:
        match = re.search(pattern, prompt_lower)
        if match:
            user_context['name'] = match.group(1).title()
            return f"Nice to meet you, {{user_context['name']}}! 😊 I'll remember your name!"
    
    # Name questions
    if 'my name' in prompt_lower or 'whats my name' in prompt_lower:
        if user_context['name']:
            return f"Your name is {{user_context['name']}}! 😊 I remember you told me that!"
        else:
            return "I don't think you've told me your name yet! 😊 What should I call you?"
    
    # Greetings
    greetings = ['hi', 'hello', 'hey', 'sup', 'whats up']
    if any(greeting in prompt_lower for greeting in greetings):
        if user_context['name']:
            return f"Hey {{user_context['name']}}! 😊 How are you doing today? I'm so excited to chat with you!"
        else:
            return "Hey there! 😊 How are you doing today? I'm so excited to chat with you!"
    
    # Time questions
    if 'time' in prompt_lower or 'what time' in prompt_lower:
        current_time = datetime.now().strftime("%I:%M %p")
        return f"Hey! 😊 It's currently {{current_time}}. Time flies when we're chatting!"
    
    # Apple question (specific)
    if 'apple' in prompt_lower:
        return "Apple is a technology company that makes iPhones, iPads, Macs, and other devices! 🍎 They're known for their innovative products and user-friendly design. What would you like to know about Apple?"
    
    # Banana question (specific)
    if 'banana' in prompt_lower:
        return "A banana is a yellow fruit that grows on trees! 🍌 It's rich in potassium and makes a great healthy snack. Bananas are one of the most popular fruits in the world!"
    
    # Weather
    if 'weather' in prompt_lower:
        return "I'd love to check the weather for you! 🌤️ But I'm not connected to weather services right now. How's the weather looking where you are?"
    
    # Help
    if 'help' in prompt_lower or 'what can you do' in prompt_lower:
        return "I can chat with you, remember your name, tell you the time, and answer questions! 😊 What would you like to know?"
    
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
    user_message = {{
        'id': str(len(messages) + 1),
        'text': data['text'],
        'sender': 'user',
        'timestamp': datetime.now().isoformat(),
        'type': 'text'
    }}
    messages.append(user_message)
    
    print(f"👤 User message: {{data['text']}}")
    
    # Update conversation history
    user_context['conversation_history'].append(data['text'].lower())
    
    # Get AI response from Ollama
    ai_response_text = get_ollama_response(data['text'])
    
    ai_response = {{
        'id': str(len(messages) + 1),
        'text': ai_response_text,
        'sender': 'ai',
        'timestamp': datetime.now().isoformat(),
        'type': 'text'
    }}
    messages.append(ai_response)
    
    print(f"🤖 Final AI Response: {{ai_response_text}}")
    print(f"📝 Context - Name: {{user_context['name']}}")
    
    return jsonify({{'success': True, 'messages': [user_message, ai_response]}})

@app.route('/api/status')
def get_status():
    return jsonify({{
        'processing_power': 90,
        'memory_usage': 40,
        'response_time': '~2-5s',
        'status': 'online',
        'ai_provider': 'Ollama (Local)',
        'model': DEFAULT_MODEL,
        'custom_model': True
    }})

if __name__ == '__main__':
    print("🚀 Starting SUNDAY-PAAI AI Server...")
    print(f"🤖 AI Provider: Ollama (Local)")
    print(f"🧠 Model: {{DEFAULT_MODEL}}")
    print(f"🌐 Server will be available at: http://localhost:8080")
    print(f"🔗 Ollama API: {{OLLAMA_URL}}")
    print("📋 Press Ctrl+C to stop the server")
    
    try:
        app.run(debug=True, host='127.0.0.1', port=8080)
    except Exception as e:
        print(f"Error starting server: {{e}}")
        print("Trying port 5000...")
        app.run(debug=True, host='127.0.0.1', port=5000)
'''
    
    # Write the app to a temporary file
    with open('temp_ai_app.py', 'w', encoding='utf-8') as f:
        f.write(app_code)
    
    # Run the app
    try:
        subprocess.run([sys.executable, 'temp_ai_app.py'])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    finally:
        # Clean up
        import os
        if os.path.exists('temp_ai_app.py'):
            os.remove('temp_ai_app.py')

def main():
    print("🔍 Checking available Ollama models...")
    models = check_ollama_models()
    
    if not models:
        print("\n❌ No Ollama models found!")
        print("💡 Please make sure:")
        print("   1. Ollama is running: ollama serve")
        print("   2. You have at least one model: ollama pull llama2:7b")
        return
    
    best_model = get_best_model(models)
    if best_model:
        print(f"\n🎯 Using best available model: {best_model}")
        run_ai_app(best_model)
    else:
        print("\n❌ No suitable model found")

if __name__ == "__main__":
    main() 