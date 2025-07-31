from flask import Flask, render_template, request, jsonify
from datetime import datetime
import requests
import re
import time

app = Flask(__name__)

# Hugging Face configuration
HF_API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-medium"
HF_API_KEY = None  # You can add your API key here if needed

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

def get_hf_response(prompt):
    """Get response from Hugging Face API"""
    try:
        # Check for creator questions first
        creator_keywords = ['who created you', 'who made you', 'who built you', 'who developed you', 'who programmed you']
        user_message_lower = prompt.lower()
        
        if any(keyword in user_message_lower for keyword in creator_keywords):
            return "A developer named Basireddy Karthik Reddy created me! 😊 He's the awesome person who brought me to life!"
        
        # Prepare the request to Hugging Face
        headers = {
            "Content-Type": "application/json"
        }
        
        if HF_API_KEY:
            headers["Authorization"] = f"Bearer {HF_API_KEY}"
        
        payload = {
            "inputs": prompt,
            "parameters": {
                "max_length": 150,
                "temperature": 0.8,
                "do_sample": True,
                "top_p": 0.9,
                "return_full_text": False
            }
        }
        
        print(f"🤖 Sending request to Hugging Face API...")
        print(f"📝 User message: {prompt}")
        
        start_time = time.time()
        response = requests.post(HF_API_URL, headers=headers, json=payload, timeout=15)
        end_time = time.time()
        
        print(f"⏱️ HF API response time: {end_time - start_time:.2f} seconds")
        print(f"📊 Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"🔍 Raw API response: {result}")
            
            # Handle different response formats
            if isinstance(result, list) and len(result) > 0:
                # Format: [{"generated_text": "..."}]
                ai_response = result[0].get('generated_text', '')
                print(f"📝 Extracted from list: {ai_response}")
            elif isinstance(result, dict):
                # Format: {"generated_text": "..."}
                ai_response = result.get('generated_text', '')
                print(f"📝 Extracted from dict: {ai_response}")
            else:
                print(f"❌ Unknown response format: {type(result)}")
                return get_fallback_response(prompt)
            
            # Clean up the response
            if ai_response:
                # Remove the original prompt from the response
                cleaned_response = ai_response.replace(prompt, '').strip()
                if cleaned_response:
                    print(f"✅ Cleaned HF AI Response: {cleaned_response[:100]}...")
                    return cleaned_response
                else:
                    print(f"⚠️ Response was empty after cleaning")
                    return get_fallback_response(prompt)
            else:
                print(f"⚠️ No generated_text found in response")
                return get_fallback_response(prompt)
        
        elif response.status_code == 503:
            print(f"⚠️ Model is loading, using fallback")
            return get_fallback_response(prompt)
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"📄 Response text: {response.text}")
            return get_fallback_response(prompt)
        
    except requests.exceptions.Timeout:
        print(f"⏱️ HF API timeout after 15 seconds")
        return get_fallback_response(prompt)
    except requests.exceptions.RequestException as e:
        print(f"❌ HF API error: {e}")
        return get_fallback_response(prompt)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return get_fallback_response(prompt)

def get_fallback_response(prompt):
    """Fallback response when HF API fails"""
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
    
    # Get AI response from Hugging Face
    ai_response_text = get_hf_response(data['text'])
    
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
    return jsonify({
        'processing_power': 90,
        'memory_usage': 40,
        'response_time': '~1-3s',
        'status': 'online',
        'ai_provider': 'Hugging Face',
        'model': 'DialoGPT-medium',
        'custom_model': False
    })

if __name__ == '__main__':
    print("🚀 Starting SUNDAY-PAAI Hugging Face AI Server...")
    print(f"🤖 AI Provider: Hugging Face")
    print(f"🧠 Model: DialoGPT-medium")
    print(f"🌐 Server will be available at: http://localhost:8080")
    print(f"🔗 HF API: {HF_API_URL}")
    print("📋 Press Ctrl+C to stop the server")
    
    try:
        app.run(debug=True, host='127.0.0.1', port=8080)
    except Exception as e:
        print(f"Error starting server: {e}")
        print("Trying port 5000...")
        app.run(debug=True, host='127.0.0.1', port=5000) 