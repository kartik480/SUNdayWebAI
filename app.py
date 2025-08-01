from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import requests
import os

app = Flask(__name__)

# Ollama configuration
OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "gemma2:2b"  # Use Gemma 2B as default model

# Store messages in memory (in production, use a database)
messages = [
    {
        'id': '1',
        'text': "Hello! I'm your SUNDAY-PAAI powered by Gemma 2B. I have memory capabilities and can remember our conversations. How can I help you today?",
        'sender': 'ai',
        'timestamp': datetime.now().isoformat(),
        'type': 'text'
    }
]

# Memory system
conversation_memory = []
memory_limit = 10  # Keep last 10 exchanges for context

def add_to_memory(user_message, ai_response):
    """Add conversation to memory"""
    global conversation_memory
    memory_entry = {
        'user': user_message,
        'ai': ai_response,
        'timestamp': datetime.now().isoformat()
    }
    conversation_memory.append(memory_entry)
    
    # Keep only the last memory_limit entries
    if len(conversation_memory) > memory_limit:
        conversation_memory = conversation_memory[-memory_limit:]
    
    print(f"💾 Memory updated: {len(conversation_memory)} entries stored")

def get_conversation_context():
    """Get recent conversation context for better responses"""
    if not conversation_memory:
        return ""
    
    context = "Recent conversation context:\n"
    for i, entry in enumerate(conversation_memory[-3:], 1):  # Last 3 exchanges
        context += f"{i}. User: {entry['user']}\n"
        context += f"   AI: {entry['ai']}\n"
    context += "\nCurrent conversation: "
    return context

def warm_up_model():
    """Warm up the model to make first response faster"""
    try:
        print(f"🔥 Warming up {DEFAULT_MODEL}...")
        warm_up_prompt = "Hi"
        get_ollama_response(warm_up_prompt, DEFAULT_MODEL)
        print(f"✅ {DEFAULT_MODEL} is ready!")
    except Exception as e:
        print(f"⚠️  Warm-up failed: {e}")

def get_ollama_response(prompt, model=DEFAULT_MODEL):
    """Get response from Ollama API with memory context"""
    try:
        # Get conversation context for better responses
        context = get_conversation_context()
        enhanced_prompt = context + prompt if context else prompt
        
        url = f"{OLLAMA_BASE_URL}/api/generate"
        payload = {
            "model": model,
            "prompt": enhanced_prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": 150  # Increased for better context responses
            }
        }
        
        # Increase timeout for first response, especially for Gemma 2B
        timeout = 60 if model == "gemma2:2b" else 30
        
        response = requests.post(url, json=payload, timeout=timeout)
        response.raise_for_status()
        
        result = response.json()
        return result.get('response', 'Sorry, I could not generate a response.')
        
    except requests.exceptions.Timeout as e:
        print(f"Ollama API timeout: {e}")
        return "I'm taking longer than expected to respond. Please try again with a shorter question."
    except requests.exceptions.RequestException as e:
        print(f"Ollama API error: {e}")
        return f"I'm having trouble connecting to my AI brain right now. Error: {str(e)}"
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "I encountered an unexpected error. Please try again."

def get_available_models():
    """Get list of available Ollama models"""
    try:
        url = f"{OLLAMA_BASE_URL}/api/tags"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        result = response.json()
        models = [model['name'] for model in result.get('models', [])]
        
        # Ensure our custom model is in the list
        if DEFAULT_MODEL not in models:
            models.insert(0, DEFAULT_MODEL)
            
        return models
        
    except Exception as e:
        print(f"Error getting models: {e}")
        return [DEFAULT_MODEL]

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
    
    # Get AI response from Ollama using your custom model
    ai_response_text = get_ollama_response(data['text'])
    
    ai_response = {
        'id': str(len(messages) + 1),
        'text': ai_response_text,
        'sender': 'ai',
        'timestamp': datetime.now().isoformat(),
        'type': 'text'
    }
    messages.append(ai_response)
    
    # Add to memory for future context
    add_to_memory(data['text'], ai_response_text)
    
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
        'custom_model': True
    })

@app.route('/api/models')
def get_models():
    """Get available Ollama models"""
    models = get_available_models()
    return jsonify({
        'models': models,
        'current_model': DEFAULT_MODEL,
        'custom_model': DEFAULT_MODEL
    })

@app.route('/api/change-model', methods=['POST'])
def change_model():
    """Change the current AI model"""
    global DEFAULT_MODEL
    data = request.json
    new_model = data.get('model')
    
    if new_model:
        available_models = get_available_models()
        if new_model in available_models:
            DEFAULT_MODEL = new_model
            return jsonify({'success': True, 'model': DEFAULT_MODEL})
        else:
            return jsonify({'success': False, 'error': 'Model not available'})
    
    return jsonify({'success': False, 'error': 'No model specified'})

@app.route('/api/model-info')
def get_model_info():
    """Get information about the current model"""
    return jsonify({
        'name': DEFAULT_MODEL,
        'description': 'SUNDAY-PAAI powered by Google Gemma 2B',
        'base_model': 'gemma2:2b',
        'creator': 'Google',
        'system_prompt': 'You are a friendly and helpful AI assistant.',
        'custom': False
    })

@app.route('/api/memory')
def get_memory():
    """Get current memory status"""
    return jsonify({
        'memory_entries': len(conversation_memory),
        'memory_limit': memory_limit,
        'recent_context': conversation_memory[-3:] if conversation_memory else []
    })

@app.route('/api/memory/clear', methods=['POST'])
def clear_memory():
    """Clear conversation memory"""
    global conversation_memory
    conversation_memory = []
    return jsonify({'success': True, 'message': 'Memory cleared successfully'})

if __name__ == '__main__':
    print("🚀 Starting SUNDAY-PAAI Flask Server with Gemma 2B Integration...")
    print(f"🤖 AI Provider: Ollama")
    print(f"🧠 Model: {DEFAULT_MODEL}")
    print(f"🌐 Server will be available at: http://localhost:8080")
    print(f"🔗 Ollama API: {OLLAMA_BASE_URL}")
    print("📋 Press Ctrl+C to stop the server")
    
    # Check if Ollama is available
    try:
        models = get_available_models()
        print(f"✅ Available models: {', '.join(models)}")
        if DEFAULT_MODEL in models:
            print(f"🎯 Model '{DEFAULT_MODEL}' is available!")
            # Warm up the model for faster first response
            warm_up_model()
        else:
            print(f"⚠️  Model '{DEFAULT_MODEL}' not found. Please ensure it's installed.")
    except:
        print("⚠️  Warning: Ollama not detected. Please make sure Ollama is running.")
        print("   Install Ollama from: https://ollama.ai")
        print(f"   Then install Gemma 2B: ollama pull gemma2:2b")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=8080)
    except Exception as e:
        print(f"Error starting server: {e}")
        print("Trying alternative port 5000...")
        try:
            app.run(debug=True, host='0.0.0.0', port=5000)
        except Exception as e2:
            print(f"Error with port 5000: {e2}")
            print("Trying localhost only...")
            app.run(debug=True, host='127.0.0.1', port=8080) 