from flask import Flask, render_template, request, jsonify
from datetime import datetime
import re

app = Flask(__name__)

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
    'last_topic': None,
    'conversation_history': []
}

def get_smart_ai_response(prompt):
    """Get intelligent response with context awareness"""
    prompt_lower = prompt.lower()
    
    # Update conversation history
    user_context['conversation_history'].append(prompt_lower)
    
    # Creator questions
    creator_keywords = ['who created you', 'who made you', 'who built you', 'who developed you', 'who programmed you']
    if any(keyword in prompt_lower for keyword in creator_keywords):
        return "A developer named Basireddy Karthik Reddy created me! 😊 He's the awesome person who brought me to life!"
    
    # Name detection and storage
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
    
    # How are you
    if 'how are you' in prompt_lower or 'how r u' in prompt_lower:
        return "I'm doing great! 😄 Thanks for asking! How about you? What's new in your world?"
    
    # Time questions
    if 'time' in prompt_lower or 'what time' in prompt_lower:
        current_time = datetime.now().strftime("%I:%M %p")
        return f"Hey! 😊 It's currently {current_time}. Time flies when we're chatting!"
    
    # AI name questions
    if 'your name' in prompt_lower or 'what are you' in prompt_lower:
        return "I'm SUNDAY-PAAI! 😊 Your friendly AI buddy who's here to chat and help you out!"
    
    # Personal questions
    if 'who are you' in prompt_lower:
        return "I'm SUNDAY-PAAI, your AI buddy! 😊 I'm here to chat, help, and be your friendly companion!"
    
    # Weather (mock response)
    if 'weather' in prompt_lower:
        return "I'd love to check the weather for you! 🌤️ But I'm not connected to weather services right now. How's the weather looking where you are?"
    
    # Help
    if 'help' in prompt_lower or 'what can you do' in prompt_lower:
        return "I can chat with you, remember your name, tell you the time, and answer questions! 😊 What would you like to know?"
    
    # Context-aware responses based on conversation history
    if len(user_context['conversation_history']) > 1:
        last_message = user_context['conversation_history'][-2]  # Previous message
        
        # If they mentioned their name recently, use it
        if user_context['name'] and any(word in last_message for word in ['name', 'karthik', 'call']):
            return f"That's interesting, {user_context['name']}! 😊 Tell me more about that!"
    
    # Default intelligent responses
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
    
    # Get AI response using smart logic
    ai_response_text = get_smart_ai_response(data['text'])
    
    ai_response = {
        'id': str(len(messages) + 1),
        'text': ai_response_text,
        'sender': 'ai',
        'timestamp': datetime.now().isoformat(),
        'type': 'text'
    }
    messages.append(ai_response)
    
    print(f"🤖 AI Response: {ai_response_text}")
    print(f"📝 Context - Name: {user_context['name']}")
    
    return jsonify({'success': True, 'messages': [user_message, ai_response]})

@app.route('/api/status')
def get_status():
    return jsonify({
        'processing_power': 95,
        'memory_usage': 45,
        'response_time': '~0.1s',
        'status': 'online',
        'ai_provider': 'Smart AI',
        'model': 'Context-Aware Logic',
        'custom_model': True
    })

if __name__ == '__main__':
    print("🚀 Starting SUNDAY-PAAI Smart AI Server...")
    print("🤖 AI Provider: Context-Aware Logic")
    print("🧠 Model: Memory & Intelligence")
    print("🌐 Server will be available at: http://localhost:8080")
    print("📋 Press Ctrl+C to stop the server")
    
    try:
        app.run(debug=True, host='127.0.0.1', port=8080)
    except Exception as e:
        print(f"Error starting server: {e}")
        print("Trying port 5000...")
        app.run(debug=True, host='127.0.0.1', port=5000) 