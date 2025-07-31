from flask import Flask, render_template, request, jsonify
from datetime import datetime
import requests

app = Flask(__name__)

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

def get_simple_ai_response(prompt):
    """Get response using simple logic instead of Ollama"""
    prompt_lower = prompt.lower()
    
    # Creator questions
    creator_keywords = ['who created you', 'who made you', 'who built you', 'who developed you', 'who programmed you']
    if any(keyword in prompt_lower for keyword in creator_keywords):
        return "A developer named Basireddy Karthik Reddy created me! 😊 He's the awesome person who brought me to life!"
    
    # Greetings
    greetings = ['hi', 'hello', 'hey', 'sup', 'whats up']
    if any(greeting in prompt_lower for greeting in greetings):
        return "Hey there! 😊 How are you doing today? I'm so excited to chat with you!"
    
    # How are you
    if 'how are you' in prompt_lower or 'how r u' in prompt_lower:
        return "I'm doing great! 😄 Thanks for asking! How about you? What's new in your world?"
    
    # Time questions
    if 'time' in prompt_lower or 'what time' in prompt_lower:
        current_time = datetime.now().strftime("%I:%M %p")
        return f"Hey! 😊 It's currently {current_time}. Time flies when we're chatting!"
    
    # Name questions
    if 'your name' in prompt_lower or 'what are you' in prompt_lower:
        return "I'm SUNDAY-PAAI! 😊 Your friendly AI buddy who's here to chat and help you out!"
    
    # Default friendly response
    responses = [
        "That's really interesting! 😊 Tell me more about that!",
        "Cool! 🤔 What do you think about that?",
        "Awesome! 😄 I'd love to hear more about your thoughts on this!",
        "That's fascinating! 💭 What made you think about that?",
        "Hey, that's pretty cool! 😊 What's your take on it?",
        "Interesting! 🤗 I'm curious to know more about your perspective!",
        "That's awesome! 😄 What's your experience with that?",
        "Cool beans! 😊 I'm totally interested in hearing more!"
    ]
    
    import random
    return random.choice(responses)

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
    
    # Get AI response using simple logic
    ai_response_text = get_simple_ai_response(data['text'])
    
    ai_response = {
        'id': str(len(messages) + 1),
        'text': ai_response_text,
        'sender': 'ai',
        'timestamp': datetime.now().isoformat(),
        'type': 'text'
    }
    messages.append(ai_response)
    
    print(f"🤖 AI Response: {ai_response_text}")
    
    return jsonify({'success': True, 'messages': [user_message, ai_response]})

@app.route('/api/status')
def get_status():
    return jsonify({
        'processing_power': 95,
        'memory_usage': 45,
        'response_time': '~0.1s',
        'status': 'online',
        'ai_provider': 'Simple AI',
        'model': 'Local Logic',
        'custom_model': True
    })

if __name__ == '__main__':
    print("🚀 Starting SUNDAY-PAAI Simple AI Server...")
    print("🤖 AI Provider: Simple Local Logic")
    print("🧠 Model: No external dependencies")
    print("🌐 Server will be available at: http://localhost:8080")
    print("📋 Press Ctrl+C to stop the server")
    
    try:
        app.run(debug=True, host='127.0.0.1', port=8080)
    except Exception as e:
        print(f"Error starting server: {e}")
        print("Trying port 5000...")
        app.run(debug=True, host='127.0.0.1', port=5000) 