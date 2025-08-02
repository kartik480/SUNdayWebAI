from flask import Flask, render_template, request, jsonify
from datetime import datetime
import json
import requests
import os
import webbrowser
import subprocess
import platform
import re
import hashlib
import urllib.parse
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

app = Flask(__name__)

# Add CORS headers manually
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

# Ollama configuration
OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "gemma2:2b"  

# API Keys and Configuration
WEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY"  # Get from https://openweathermap.org/api
SPOTIFY_CLIENT_ID = "YOUR_SPOTIFY_CLIENT_ID"  # Get from https://developer.spotify.com
SPOTIFY_CLIENT_SECRET = "YOUR_SPOTIFY_CLIENT_SECRET"

# File paths for persistent storage
CONVERSATION_FILE = "conversation_history.json"
MEMORY_FILE = "memory_data.json"
TRAINING_FILE = "training_data.json"
USER_PROFILE_FILE = "user_profiles.json"
LONG_TERM_MEMORY_FILE = "long_term_memory.json"
TASK_MEMORY_FILE = "task_memory.json"

# Load or create conversation history
def generate_dynamic_welcome_message():
    """Generate a unique welcome message every time"""
    import random
    
    # Get current time for time-based greetings
    current_hour = datetime.now().hour
    
    # Time-based greetings
    if 5 <= current_hour < 12:
        time_greeting = "Good morning"
    elif 12 <= current_hour < 17:
        time_greeting = "Good afternoon"
    elif 17 <= current_hour < 21:
        time_greeting = "Good evening"
    else:
        time_greeting = "Good night"
    
    # Dynamic welcome messages with different styles
    welcome_messages = [
        f"🎉 {time_greeting} Boss! I'm SUNDAY-PAAI, your AI companion created by Basireddy Karthik! Ready to rock and roll with some amazing conversations? What's on your mind today? 🚀",
        
        f"🔥 Yo Boss! SUNDAY-PAAI here, fresh and ready to serve! Created by the legendary Basireddy Karthik, I'm here to make your day awesome. What's the plan, Boss? 💪",
        
        f"🌟 {time_greeting} Boss! SUNDAY-PAAI at your service! Your AI buddy, crafted with love by Basireddy Karthik, is here to help you conquer the day. What shall we tackle first? ⚡",
        
        f"🎯 Hey Boss! SUNDAY-PAAI reporting for duty! Your personal AI assistant, brought to life by Basireddy Karthik, is ready to assist. What's the mission today? 🎪",
        
        f"💫 {time_greeting} Boss! SUNDAY-PAAI is back and better than ever! Your AI companion, created by the brilliant Basireddy Karthik, is here to make magic happen. What's cooking? ✨",
        
        f"🚀 Boss alert! SUNDAY-PAAI is online and ready to serve! Your AI buddy, designed by Basireddy Karthik, is here to help you achieve greatness. What's the game plan? 🎮",
        
        f"🎊 {time_greeting} Boss! SUNDAY-PAAI is here to party with your ideas! Your AI assistant, built by Basireddy Karthik, is ready to turn your thoughts into reality. What's the vibe today? 🎵",
        
        f"⚡ Boss! SUNDAY-PAAI is charged up and ready to go! Your AI companion, created by Basireddy Karthik, is here to supercharge your day. What's the energy we're bringing? 🔋",
        
        f"🎭 {time_greeting} Boss! SUNDAY-PAAI is ready to perform! Your AI buddy, crafted by Basireddy Karthik, is here to entertain and assist. What's the show today? 🎬",
        
        f"🌈 Boss! SUNDAY-PAAI is here to add some color to your day! Your AI assistant, designed by Basireddy Karthik, is ready to brighten things up. What's the mood? 🌟"
    ]
    
    return random.choice(welcome_messages)

def load_conversation_history():
    """Load conversation history from file"""
    try:
        if os.path.exists(CONVERSATION_FILE):
            with open(CONVERSATION_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"📂 Loaded {len(data)} messages from conversation history")
                return data
        else:
            # Create initial welcome message with dynamic content
            initial_message = {
                'id': '1',
                'text': generate_dynamic_welcome_message(),
                'sender': 'ai',
                'timestamp': datetime.now().isoformat(),
                'type': 'text'
            }
            save_conversation_history([initial_message])
            return [initial_message]
    except Exception as e:
        print(f"⚠️ Error loading conversation history: {e}")
        # Return default welcome message if file is corrupted
        return [{
            'id': '1',
            'text': generate_dynamic_welcome_message(),
            'sender': 'ai',
            'timestamp': datetime.now().isoformat(),
            'type': 'text'
        }]

def save_conversation_history(messages):
    """Save conversation history to file"""
    try:
        with open(CONVERSATION_FILE, 'w', encoding='utf-8') as f:
            json.dump(messages, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved {len(messages)} messages to conversation history")
    except Exception as e:
        print(f"⚠️ Error saving conversation history: {e}")

# Load or create memory data
def load_memory_data():
    """Load memory data from file"""
    try:
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"📂 Loaded {len(data)} memory entries")
                return data
        else:
            return []
    except Exception as e:
        print(f"⚠️ Error loading memory data: {e}")
        return []

def save_memory_data(memory_data):
    """Save memory data to file"""
    try:
        with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(memory_data, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved {len(memory_data)} memory entries")
    except Exception as e:
        print(f"⚠️ Error saving memory data: {e}")

# Load or create user profiles
def load_user_profiles():
    """Load user profiles from file"""
    try:
        if os.path.exists(USER_PROFILE_FILE):
            with open(USER_PROFILE_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"📂 Loaded {len(data)} user profiles")
                return data
        else:
            return {}
    except Exception as e:
        print(f"⚠️ Error loading user profiles: {e}")
        return {}

def save_user_profiles(user_profiles):
    """Save user profiles to file"""
    try:
        with open(USER_PROFILE_FILE, 'w', encoding='utf-8') as f:
            json.dump(user_profiles, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved {len(user_profiles)} user profiles")
    except Exception as e:
        print(f"⚠️ Error saving user profiles: {e}")

# Load or create long-term memory
def load_long_term_memory():
    """Load long-term memory from file"""
    try:
        if os.path.exists(LONG_TERM_MEMORY_FILE):
            with open(LONG_TERM_MEMORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"📂 Loaded {len(data)} long-term memory entries")
                return data
        else:
            return []
    except Exception as e:
        print(f"⚠️ Error loading long-term memory: {e}")
        return []

def save_long_term_memory(long_term_memory):
    """Save long-term memory to file"""
    try:
        with open(LONG_TERM_MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(long_term_memory, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved {len(long_term_memory)} long-term memory entries")
    except Exception as e:
        print(f"⚠️ Error saving long-term memory: {e}")

# Load or create task memory
def load_task_memory():
    """Load task memory from file"""
    try:
        if os.path.exists(TASK_MEMORY_FILE):
            with open(TASK_MEMORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"📂 Loaded {len(data)} task entries")
                return data
        else:
            return []
    except Exception as e:
        print(f"⚠️ Error loading task memory: {e}")
        return []

def save_task_memory(task_memory):
    """Save task memory to file"""
    try:
        with open(TASK_MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(task_memory, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved {len(task_memory)} task entries")
    except Exception as e:
        print(f"⚠️ Error saving task memory: {e}")

def add_task_to_memory(task_description, priority="medium", status="pending"):
    """Add a task to memory"""
    global task_memory
    task_entry = {
        'task': task_description,
        'priority': priority,
        'status': status,
        'created_at': datetime.now().isoformat(),
        'assigned_by': 'Basireddy Karthik (Boss)'
    }
    task_memory.append(task_entry)
    save_task_memory(task_memory)
    print(f"📋 Task added to memory: {task_description}")

def get_boss_tasks():
    """Get all tasks for the boss"""
    return task_memory

def load_training_data():
    """Load training data from file"""
    try:
        if os.path.exists(TRAINING_FILE):
            with open(TRAINING_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(f"📂 Loaded {len(data)} training samples")
                return data
        else:
            return []
    except Exception as e:
        print(f"⚠️ Error loading training data: {e}")
        return []

def save_training_data(training_data):
    """Save training data to file"""
    try:
        with open(TRAINING_FILE, 'w', encoding='utf-8') as f:
            json.dump(training_data, f, indent=2, ensure_ascii=False)
        print(f"💾 Saved {len(training_data)} training samples")
    except Exception as e:
        print(f"⚠️ Error saving training data: {e}")

# Initialize data from files
messages = load_conversation_history()
conversation_memory = load_memory_data()
training_data = load_training_data()
user_profiles = load_user_profiles()
long_term_memory = load_long_term_memory()
task_memory = load_task_memory()

memory_limit = 15  # Increased memory limit for better context
long_term_memory_limit = 100  # Keep important memories for longer

def identify_user(message):
    """Identify user from message content"""
    # Look for name mentions in the message
    name_patterns = [
        r"i am (\w+)",
        r"my name is (\w+)",
        r"i'm (\w+)",
        r"call me (\w+)",
        r"i am basireddy (\w+)",
        r"i'm basireddy (\w+)",
        r"my name is basireddy (\w+)"
    ]
    
    message_lower = message.lower()
    
    for pattern in name_patterns:
        match = re.search(pattern, message_lower)
        if match:
            name = match.group(1).title()
            # Check if it's Basireddy Karthik
            if "karthik" in name.lower() or "basireddy" in message_lower:
                return "Basireddy Karthik"
            return name
    
    # Check if user is asking about their name
    if any(phrase in message_lower for phrase in ["what's my name", "what is my name", "tell me my name", "do you know my name"]):
        # Return the most recent user name from memory
        for entry in reversed(conversation_memory):
            if entry.get('user_name'):
                return entry['user_name']
    
    return None

def create_user_profile(user_name):
    """Create or update user profile"""
    global user_profiles
    
    if user_name not in user_profiles:
        user_profiles[user_name] = {
            'name': user_name,
            'first_seen': datetime.now().isoformat(),
            'last_seen': datetime.now().isoformat(),
            'conversation_count': 0,
            'preferences': {},
            'important_facts': [],
            'relationship': 'user'
        }
    else:
        user_profiles[user_name]['last_seen'] = datetime.now().isoformat()
        user_profiles[user_name]['conversation_count'] += 1
    
    # Special handling for creator
    if user_name == "Basireddy Karthik":
        user_profiles[user_name]['relationship'] = 'creator'
        user_profiles[user_name]['important_facts'].append("Created SUNDAY-PAAI")
    
    save_user_profiles(user_profiles)
    return user_profiles[user_name]

def add_to_memory(user_message, ai_response, user_name=None):
    """Add conversation to memory with user identification"""
    global conversation_memory
    
    # Identify user if not provided
    if not user_name:
        user_name = identify_user(user_message)
    
    memory_entry = {
        'user': user_message,
        'ai': ai_response,
        'timestamp': datetime.now().isoformat(),
        'user_name': user_name
    }
    
    conversation_memory.append(memory_entry)
    
    # Keep only the last memory_limit entries
    if len(conversation_memory) > memory_limit:
        conversation_memory = conversation_memory[-memory_limit:]
    
    # Save to file
    save_memory_data(conversation_memory)
    print(f"💾 Memory updated: {len(conversation_memory)} entries stored")
    
    # Add to long-term memory if important
    if user_name or any(keyword in user_message.lower() for keyword in ['important', 'remember', 'never forget', 'my name', 'i am']):
        add_to_long_term_memory(user_message, ai_response, user_name)

def add_to_long_term_memory(user_message, ai_response, user_name=None):
    """Add important information to long-term memory"""
    global long_term_memory
    
    long_term_entry = {
        'user': user_message,
        'ai': ai_response,
        'timestamp': datetime.now().isoformat(),
        'user_name': user_name,
        'importance': 'high' if user_name else 'medium'
    }
    
    long_term_memory.append(long_term_entry)
    
    # Keep only the last long_term_memory_limit entries
    if len(long_term_memory) > long_term_memory_limit:
        long_term_memory = long_term_memory[-long_term_memory_limit:]
    
    save_long_term_memory(long_term_memory)
    print(f"🧠 Long-term memory updated: {len(long_term_memory)} entries stored")

def get_user_context(user_name=None):
    """Get context about the user for better responses"""
    if not user_name:
        return ""
    
    context = f"User Context - Name: {user_name}\n"
    
    # Get user profile
    if user_name in user_profiles:
        profile = user_profiles[user_name]
        context += f"Relationship: {profile['relationship']}\n"
        context += f"Conversations: {profile['conversation_count']}\n"
        if profile['important_facts']:
            context += f"Important facts: {', '.join(profile['important_facts'])}\n"
    
    # Get recent conversations with this user
    user_conversations = [entry for entry in conversation_memory if entry.get('user_name') == user_name]
    if user_conversations:
        context += "Recent conversations:\n"
        for i, entry in enumerate(user_conversations[-3:], 1):
            context += f"{i}. User: {entry['user']}\n"
            context += f"   AI: {entry['ai']}\n"
    
    # Get long-term memories about this user
    user_long_term = [entry for entry in long_term_memory if entry.get('user_name') == user_name]
    if user_long_term:
        context += "Important memories:\n"
        for entry in user_long_term[-2:]:  # Last 2 important memories
            context += f"- {entry['user']}\n"
    
    # Get boss tasks if this is the creator
    if user_name == "Basireddy Karthik" and task_memory:
        context += "Boss Tasks:\n"
        for i, task in enumerate(task_memory[-5:], 1):  # Last 5 tasks
            context += f"{i}. {task['task']} (Status: {task['status']}, Priority: {task['priority']})\n"
    
    return context

def add_to_training_data(user_message, ai_response, rating=None):
    """Add conversation to training data"""
    global training_data
    training_entry = {
        'user': user_message,
        'ai': ai_response,
        'rating': rating,  # 1-5 rating for response quality
        'timestamp': datetime.now().isoformat(),
        'context': get_conversation_context()
    }
    training_data.append(training_entry)
    
    # Save to file
    save_training_data(training_data)
    print(f"📚 Training data updated: {len(training_data)} samples collected")

def get_conversation_context():
    """Get recent conversation context for better responses"""
    if not conversation_memory:
        return ""
    
    context = "Recent conversation context:\n"
    for i, entry in enumerate(conversation_memory[-5:], 1):  # Last 5 exchanges
        user_name = entry.get('user_name', 'User')
        context += f"{i}. {user_name}: {entry['user']}\n"
        context += f"   AI: {entry['ai']}\n"
    context += "\nCurrent conversation: "
    return context

# Training system
training_status = {
    'is_training': False,
    'progress': 0,
    'epochs': 0,
    'current_epoch': 0,
    'loss': 0.0,
    'accuracy': 0.0,
    'last_trained': None
}

def start_training():
    """Start the training process"""
    global training_status
    if len(training_data) < 5:
        return False, "Need at least 5 training samples to start training"
    
    training_status['is_training'] = True
    training_status['progress'] = 0
    training_status['epochs'] = 3
    training_status['current_epoch'] = 0
    training_status['loss'] = 0.0
    training_status['accuracy'] = 0.0
    
    print("🚀 Starting AI training process...")
    return True, "Training started successfully"

def simulate_training_progress():
    """Simulate training progress (in real implementation, this would be actual training)"""
    global training_status
    if not training_status['is_training']:
        return
    
    # Simulate training progress
    for epoch in range(training_status['epochs']):
        training_status['current_epoch'] = epoch + 1
        training_status['progress'] = ((epoch + 1) / training_status['epochs']) * 100
        
        # Simulate loss and accuracy improvements
        training_status['loss'] = max(0.1, 2.0 - (epoch * 0.6))
        training_status['accuracy'] = min(0.95, 0.3 + (epoch * 0.2))
        
        print(f"📈 Epoch {epoch + 1}/{training_status['epochs']} - Loss: {training_status['loss']:.3f}, Accuracy: {training_status['accuracy']:.3f}")
        
        # Simulate training time
        import time
        time.sleep(2)
    
    training_status['is_training'] = False
    training_status['last_trained'] = datetime.now().isoformat()
    print("✅ Training completed!")

def warm_up_model():
    """Warm up the model to make first response faster"""
    try:
        print(f"🔥 Warming up {DEFAULT_MODEL}...")
        warm_up_prompt = "Hi"
        
        # Use threading with timeout for Windows compatibility
        import threading
        import time
        
        result = [None]
        error = [None]
        
        def warm_up_worker():
            try:
                result[0] = get_ollama_response(warm_up_prompt, DEFAULT_MODEL)
            except Exception as e:
                error[0] = e
        
        thread = threading.Thread(target=warm_up_worker)
        thread.daemon = True
        thread.start()
        
        # Wait for up to 30 seconds
        thread.join(timeout=30)
        
        if thread.is_alive():
            print(f"⚠️  Warm-up timed out, but server will continue")
        elif error[0]:
            print(f"⚠️  Warm-up failed: {error[0]}")
        else:
            print(f"✅ {DEFAULT_MODEL} is ready!")
            
    except Exception as e:
        print(f"⚠️  Warm-up failed: {e}")

def get_current_time():
    """Get current date and time"""
    now = datetime.now()
    return {
        'date': now.strftime("%A, %B %d, %Y"),
        'time': now.strftime("%I:%M:%S %p"),
        'timezone': 'Local Time',
        'formatted': f"Today is {now.strftime('%A, %B %d, %Y')} and the current time is {now.strftime('%I:%M:%S %p')}"
    }

def get_user_location():
    """Get user's location using IP geolocation"""
    try:
        # Use a free IP geolocation service
        response = requests.get('https://ipapi.co/json/', timeout=5)
        if response.status_code == 200:
            data = response.json()
            return {
                'city': data.get('city', 'Unknown'),
                'country': data.get('country_name', 'Unknown'),
                'latitude': data.get('latitude'),
                'longitude': data.get('longitude'),
                'timezone': data.get('timezone', 'Unknown')
            }
    except Exception as e:
        print(f"Error getting location: {e}")
    
    return None

def get_weather(location=None):
    """Get current weather information"""
    try:
        # If no location provided, try to get user's location
        user_location = None
        if not location:
            user_location = get_user_location()
            if user_location:
                location = user_location['city']
            else:
                return "❌ Sorry, I couldn't determine your location. Please specify a city name."
        
        # Use OpenWeatherMap API
        if WEATHER_API_KEY == "YOUR_OPENWEATHER_API_KEY":
            # Fallback to a free weather service
            url = f"https://api.open-meteo.com/v1/forecast"
            params = {
                'latitude': user_location['latitude'] if user_location else 40.7128,
                'longitude': user_location['longitude'] if user_location else -74.0060,
                'current': 'temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m',
                'timezone': 'auto'
            }
        else:
            # Use OpenWeatherMap API
            url = "http://api.openweathermap.org/data/2.5/weather"
            params = {
                'q': location,
                'appid': WEATHER_API_KEY,
                'units': 'metric'
            }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        if WEATHER_API_KEY == "YOUR_OPENWEATHER_API_KEY":
            # Parse Open-Meteo response
            current = data.get('current', {})
            weather_info = {
                'temperature': current.get('temperature_2m', 'N/A'),
                'feels_like': current.get('apparent_temperature', 'N/A'),
                'humidity': current.get('relative_humidity_2m', 'N/A'),
                'description': get_weather_description(current.get('weather_code', 0)),
                'wind_speed': current.get('wind_speed_10m', 'N/A'),
                'location': location
            }
        else:
            # Parse OpenWeatherMap response
            weather_info = {
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description'],
                'wind_speed': data['wind']['speed'],
                'location': data['name']
            }
        
        return f"🌤️ Weather in {weather_info['location']}:\n" \
               f"🌡️ Temperature: {weather_info['temperature']}°C\n" \
               f"🌡️ Feels like: {weather_info['feels_like']}°C\n" \
               f"💧 Humidity: {weather_info['humidity']}%\n" \
               f"🌪️ Wind: {weather_info['wind_speed']} m/s\n" \
               f"☁️ Conditions: {weather_info['description']}"
        
    except Exception as e:
        print(f"Weather API error: {e}")
        # Try to research weather information online as fallback
        try:
            research_query = f"current weather {location} today"
            research_result = research_internet(research_query)
            if research_result and "❌" not in research_result:
                return f"🌤️ Weather information for {location} (researched online):\n{research_result}"
        except:
            pass
        return f"❌ Sorry, I couldn't get the weather information. Error: {str(e)}"

def get_weather_description(code):
    """Convert weather code to description"""
    weather_codes = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Foggy",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Moderate drizzle",
        55: "Dense drizzle",
        61: "Slight rain",
        63: "Moderate rain",
        65: "Heavy rain",
        71: "Slight snow",
        73: "Moderate snow",
        75: "Heavy snow",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Moderate rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with slight hail",
        99: "Thunderstorm with heavy hail"
    }
    return weather_codes.get(code, "Unknown")

def search_youtube(query):
    """Search YouTube and open the first result"""
    try:
        # Create YouTube search URL
        search_query = urllib.parse.quote(query)
        youtube_search_url = f"https://www.youtube.com/results?search_query={search_query}"
        
        # Open YouTube search in browser
        webbrowser.open(youtube_search_url)
        
        return f"🎵 I've opened YouTube search for '{query}' in your browser! You should see the search results now."
        
    except Exception as e:
        return f"❌ Sorry, I couldn't search YouTube. Error: {str(e)}"

def search_spotify(query):
    """Search Spotify and open the first result"""
    try:
        # Create Spotify search URL
        search_query = urllib.parse.quote(query)
        spotify_search_url = f"https://open.spotify.com/search/{search_query}"
        
        # Open Spotify search in browser
        webbrowser.open(spotify_search_url)
        
        return f"🎵 I've opened Spotify search for '{query}' in your browser! You should see the search results now."
        
    except Exception as e:
        return f"❌ Sorry, I couldn't search Spotify. Error: {str(e)}"

def search_netflix(query):
    """Search Netflix and open the first result"""
    try:
        # Create Netflix search URL
        search_query = urllib.parse.quote(query)
        netflix_search_url = f"https://www.netflix.com/search?q={search_query}"
        
        # Open Netflix search in browser
        webbrowser.open(netflix_search_url)
        
        return f"🎬 I've opened Netflix search for '{query}' in your browser! You should see the search results now."
        
    except Exception as e:
        return f"❌ Sorry, I couldn't search Netflix. Error: {str(e)}"

def search_amazon(query):
    """Search Amazon and open the first result"""
    try:
        # Create Amazon search URL
        search_query = urllib.parse.quote(query)
        amazon_search_url = f"https://www.amazon.com/s?k={search_query}"
        
        # Open Amazon search in browser
        webbrowser.open(amazon_search_url)
        
        return f"🛒 I've opened Amazon search for '{query}' in your browser! You should see the search results now."
        
    except Exception as e:
        return f"❌ Sorry, I couldn't search Amazon. Error: {str(e)}"

def search_social_media(platform, query):
    """Search social media platforms"""
    try:
        platform_urls = {
            'facebook': f"https://www.facebook.com/search/top/?q={urllib.parse.quote(query)}",
            'instagram': f"https://www.instagram.com/explore/tags/{urllib.parse.quote(query)}/",
            'twitter': f"https://twitter.com/search?q={urllib.parse.quote(query)}",
            'x': f"https://twitter.com/search?q={urllib.parse.quote(query)}",
            'tiktok': f"https://www.tiktok.com/search?q={urllib.parse.quote(query)}",
            'linkedin': f"https://www.linkedin.com/search/results/all/?keywords={urllib.parse.quote(query)}",
            'reddit': f"https://www.reddit.com/search/?q={urllib.parse.quote(query)}"
        }
        
        if platform in platform_urls:
            webbrowser.open(platform_urls[platform])
            return f"📱 I've opened {platform.title()} search for '{query}' in your browser!"
        else:
            return f"❌ Sorry, I don't support searching on {platform} yet."
        
    except Exception as e:
        return f"❌ Sorry, I couldn't search {platform}. Error: {str(e)}"

def search_web_enhanced(query):
    """Enhanced web search with multiple options"""
    try:
        # Create search URLs for different engines
        google_url = f"https://www.google.com/search?q={urllib.parse.quote(query)}"
        bing_url = f"https://www.bing.com/search?q={urllib.parse.quote(query)}"
        duckduckgo_url = f"https://duckduckgo.com/?q={urllib.parse.quote(query)}"
        
        # Open Google search by default
        webbrowser.open(google_url)
        
        return f"🔍 I've opened a web search for '{query}' in your browser! You can also try:\n" \
               f"• Bing: {bing_url}\n" \
               f"• DuckDuckGo: {duckduckgo_url}"
        
    except Exception as e:
        return f"❌ Sorry, I couldn't perform the web search. Error: {str(e)}"

def research_internet(query):
    """Research information from the internet and provide direct answers"""
    try:
        import requests
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            # Fallback if BeautifulSoup is not available
            BeautifulSoup = None
        import re
        
        # Clean and enhance the query
        query_lower = query.lower()
        
        # Determine the type of research needed
        if any(keyword in query_lower for keyword in ['ganesh chaturthi', 'ganesh', 'chaturthi']):
            search_query = "Ganesh Chaturthi 2025 date celebration festival"
            topic = "Ganesh Chaturthi"
        elif any(keyword in query_lower for keyword in ['diwali', 'deepavali']):
            search_query = "Diwali 2025 date celebration festival"
            topic = "Diwali"
        elif any(keyword in query_lower for keyword in ['holi']):
            search_query = "Holi 2025 date celebration festival"
            topic = "Holi"
        elif any(keyword in query_lower for keyword in ['dussera', 'dussehra', 'navratri', 'durga puja']):
            search_query = "Dussehra 2025 date celebration festival"
            topic = "Dussehra"
        elif any(keyword in query_lower for keyword in ['ramadan', 'ramzan']):
            search_query = "Ramadan 2025 date start end"
            topic = "Ramadan"
        else:
            search_query = f"{query} 2025 information"
            topic = query
        
        # Use Google search (more reliable than DuckDuckGo for this purpose)
        search_url = f"https://www.google.com/search?q={urllib.parse.quote(search_query)}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        
        response = requests.get(search_url, headers=headers, timeout=15)
        response.raise_for_status()
        
        if BeautifulSoup is None:
            raise ImportError("BeautifulSoup not available")
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Try to extract featured snippet or knowledge panel
        featured_snippet = soup.find('div', class_='IZ6rdc')
        if featured_snippet:
            snippet_text = featured_snippet.get_text(strip=True)
            if snippet_text:
                return f"🔍 Research Results for '{topic}':\n\n" \
                       f"📋 Featured Information:\n{snippet_text}\n\n" \
                       f"💡 This information was found through web research"
        
        # Extract search results
        results = []
        for result in soup.find_all('div', class_='g')[:5]:  # Get top 5 results
            title_elem = result.find('h3')
            snippet_elem = result.find('div', class_='VwiC3b')
            
            if title_elem and snippet_elem:
                title = title_elem.get_text(strip=True)
                snippet = snippet_elem.get_text(strip=True)
                
                results.append({
                    'title': title,
                    'snippet': snippet
                })
        
        # If no structured results, try alternative parsing
        if not results:
            # Look for any text content that might contain dates
            page_text = soup.get_text()
            
            # Look for date patterns
            date_patterns = [
                r'\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}\b',
                r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}\b',
                r'\b\d{4}-\d{2}-\d{2}\b',
                r'\b\d{1,2}/\d{1,2}/\d{4}\b'
            ]
            
            dates_found = []
            for pattern in date_patterns:
                matches = re.findall(pattern, page_text, re.IGNORECASE)
                dates_found.extend(matches)
            
            if dates_found:
                return f"🔍 Based on my research for '{topic}':\n\n" \
                       f"📅 I found these relevant dates:\n" \
                       f"{chr(10).join([f'• {date}' for date in dates_found[:3]])}\n\n" \
                       f"💡 For the most accurate and up-to-date information, I recommend checking:\n" \
                       f"• Official calendar websites\n" \
                       f"• Religious organization websites\n" \
                       f"• Government holiday calendars\n\n" \
                       f"💡 This information was found through web research"
        
        # Analyze results for specific information
        research_summary = f"🔍 Research Results for '{topic}':\n\n"
        
        # Look for specific information in the results
        found_info = []
        for result in results:
            text_to_search = f"{result['title']} {result['snippet']}".lower()
            
            # Look for date patterns
            date_patterns = [
                r'\b\d{1,2}\s+(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{4}\b',
                r'\b(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{1,2},?\s+\d{4}\b',
                r'\b\d{4}-\d{2}-\d{2}\b',
                r'\b\d{1,2}/\d{1,2}/\d{4}\b'
            ]
            
            for pattern in date_patterns:
                matches = re.findall(pattern, text_to_search, re.IGNORECASE)
                found_info.extend(matches)
            
            # Look for specific keywords related to the query
            relevant_keywords = ['ganesh', 'chaturthi', 'diwali', 'holi', 'ramadan', 'festival', 'celebration', 'date', '2025', 'holiday']
            if any(keyword in text_to_search for keyword in relevant_keywords):
                found_info.append(f"Relevant info: {result['snippet'][:100]}...")
        
        if found_info:
            research_summary += "📅 Found Information:\n"
            for info in found_info[:5]:  # Limit to 5 items
                research_summary += f"• {info}\n"
            research_summary += "\n"
        
        # Add top search results
        if results:
            research_summary += "🔗 Top Search Results:\n"
            for i, result in enumerate(results[:3], 1):
                research_summary += f"{i}. {result['title']}\n"
                research_summary += f"   {result['snippet'][:150]}...\n\n"
        
        # Add recommendation based on topic
        research_summary += "💡 Recommendation:\n"
        if 'ganesh' in query_lower or 'chaturthi' in query_lower:
            research_summary += "For the most accurate and current information about Ganesh Chaturthi 2025, I recommend:\n"
            research_summary += "• Checking official Hindu calendar websites\n"
            research_summary += "• Visiting temple websites or religious organizations\n"
            research_summary += "• Consulting government holiday calendars\n"
            research_summary += "• Using reliable calendar apps or websites\n\n"
        else:
            research_summary += "For the most accurate and current information, I recommend:\n"
            research_summary += "• Checking official websites and sources\n"
            research_summary += "• Consulting reliable news sources\n"
            research_summary += "• Using government or organization websites\n"
            research_summary += "• Verifying information from multiple sources\n\n"
        
        research_summary += f"💡 For more detailed information, you can search online for '{query}'"
        
        # Note: Removed browser opening to provide direct answers instead
        
        return research_summary
        
    except Exception as e:
        print(f"Research error: {e}")
        # Fallback to simple web search with enhanced response
        fallback_response = f"🔍 I'm researching '{query}' for you!\n\n"
        fallback_response += "📋 Based on my knowledge, here's what I can tell you:\n"
        
        # Provide some basic information based on the query
        query_lower = query.lower()
        if 'ganesh chaturthi' in query_lower:
            fallback_response += "• Ganesh Chaturthi is a Hindu festival celebrating Lord Ganesha's birth\n"
            fallback_response += "• It typically falls in August or September\n"
            fallback_response += "• The exact date varies each year based on the Hindu lunar calendar\n"
            fallback_response += "• In 2025, it's likely to be in September\n\n"
        elif 'diwali' in query_lower:
            fallback_response += "• Diwali is the Festival of Lights\n"
            fallback_response += "• It typically falls in October or November\n"
            fallback_response += "• The exact date varies each year\n"
            fallback_response += "• In 2025, it's likely to be in November\n\n"
        elif 'holi' in query_lower:
            fallback_response += "• Holi is the Festival of Colors\n"
            fallback_response += "• It typically falls in March\n"
            fallback_response += "• The exact date varies each year\n"
            fallback_response += "• In 2025, it's likely to be in March\n\n"
        elif any(keyword in query_lower for keyword in ['dussera', 'dussehra', 'navratri']):
            fallback_response += "• Dussehra (also called Dussera) is a major Hindu festival\n"
            fallback_response += "• It celebrates the victory of good over evil\n"
            fallback_response += "• It typically falls in September or October\n"
            fallback_response += "• The exact date varies each year based on the Hindu lunar calendar\n"
            fallback_response += "• In 2025, it's likely to be in October\n\n"
        
        fallback_response += "💡 For the exact dates and more detailed information, you can search online for this topic"
        
        # Note: Removed browser opening to provide direct answers instead
        
        return fallback_response

def get_news(category="general", country="us"):
    """Get latest news"""
    try:
        # Use a free news API
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            'country': country,
            'category': category,
            'apiKey': 'YOUR_NEWS_API_KEY'  # Get from https://newsapi.org
        }
        
        # For now, just open a news website
        news_urls = {
            'general': 'https://news.google.com',
            'technology': 'https://techcrunch.com',
            'sports': 'https://espn.com',
            'business': 'https://bloomberg.com',
            'entertainment': 'https://variety.com'
        }
        
        news_url = news_urls.get(category, 'https://news.google.com')
        webbrowser.open(news_url)
        
        return f"📰 I've opened {category} news in your browser!"
        
    except Exception as e:
        return f"❌ Sorry, I couldn't get the news. Error: {str(e)}"

def get_stock_price(symbol):
    """Get stock price information"""
    try:
        # Use Yahoo Finance URL
        yahoo_url = f"https://finance.yahoo.com/quote/{symbol.upper()}"
        webbrowser.open(yahoo_url)
        
        return f"📈 I've opened stock information for {symbol.upper()} in your browser!"
        
    except Exception as e:
        return f"❌ Sorry, I couldn't get stock information. Error: {str(e)}"

def translate_text(text, target_language="en"):
    """Translate text using Google Translate"""
    try:
        # Create Google Translate URL
        translate_url = f"https://translate.google.com/?sl=auto&tl={target_language}&text={urllib.parse.quote(text)}"
        webbrowser.open(translate_url)
        
        return f"🌐 I've opened Google Translate for '{text}' in your browser!"
        
    except Exception as e:
        return f"❌ Sorry, I couldn't translate the text. Error: {str(e)}"

def open_website(url):
    """Open a website in the default browser"""
    try:
        # Clean and validate URL
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        # Open in default browser
        webbrowser.open(url)
        return f"✅ Successfully opened {url} in your default browser!"
    except Exception as e:
        return f"❌ Sorry, I couldn't open {url}. Error: {str(e)}"

def open_youtube():
    """Open YouTube in the default browser"""
    return open_website("https://www.youtube.com")

def open_google():
    """Open Google in the default browser"""
    return open_website("https://www.google.com")

def search_web(query):
    """Perform a web search (simulated - opens Google search)"""
    try:
        search_url = f"https://www.google.com/search?q={requests.utils.quote(query)}"
        webbrowser.open(search_url)
        return f"🔍 I've opened a Google search for '{query}' in your browser!"
    except Exception as e:
        return f"❌ Sorry, I couldn't perform the web search. Error: {str(e)}"

def detect_action_request(prompt):
    """Detect if the user is requesting an action"""
    prompt_lower = prompt.lower()
    
    # Weather requests
    weather_keywords = ['weather', 'temperature', 'forecast', 'how hot', 'how cold', 'weather today', 'weather now']
    if any(keyword in prompt_lower for keyword in weather_keywords):
        # Extract location if mentioned
        location_patterns = [
            r'weather in (\w+)',
            r'weather at (\w+)',
            r'weather for (\w+)',
            r'temperature in (\w+)',
            r'forecast for (\w+)'
        ]
        for pattern in location_patterns:
            match = re.search(pattern, prompt_lower)
            if match:
                location = match.group(1)
                return f'weather:{location}'
        return 'weather'
    
    # YouTube requests
    youtube_keywords = ['youtube', 'play', 'watch', 'video', 'song', 'music video']
    if any(keyword in prompt_lower for keyword in youtube_keywords):
        # Extract search query
        search_patterns = [
            r'play (.+) on youtube',
            r'watch (.+) on youtube',
            r'youtube (.+)',
            r'play (.+)',
            r'watch (.+)',
            r'open (.+) on youtube',
            r'open (.+) in youtube',
            r'open (.+) song in youtube',
            r'open (.+) music in youtube',
            r'search (.+) on youtube',
            r'find (.+) on youtube',
            r'look up (.+) on youtube'
        ]
        for pattern in search_patterns:
            match = re.search(pattern, prompt_lower)
            if match:
                query = match.group(1).strip()
                return f'youtube_search:{query}'
        return 'youtube'
    
    # Spotify requests
    spotify_keywords = ['spotify', 'music', 'song', 'playlist', 'album']
    if any(keyword in prompt_lower for keyword in spotify_keywords):
        # Extract search query
        search_patterns = [
            r'play (.+) on spotify',
            r'spotify (.+)',
            r'play (.+)',
            r'find (.+) on spotify',
            r'search (.+) on spotify',
            r'open (.+) on spotify',
            r'open (.+) in spotify',
            r'search (.+) in spotify',
            r'find (.+) in spotify',
            r'look up (.+) on spotify',
            r'look up (.+) in spotify'
        ]
        for pattern in search_patterns:
            match = re.search(pattern, prompt_lower)
            if match:
                query = match.group(1).strip()
                return f'spotify_search:{query}'
        return 'spotify'
    
    # Time-related requests
    time_keywords = ['what time', 'current time', 'what is the time', 'time now', 'what day', 'current date', 'today\'s date']
    if any(keyword in prompt_lower for keyword in time_keywords):
        return 'time'
    
    # Netflix requests
    netflix_keywords = ['netflix', 'movie', 'show', 'series', 'stream']
    if any(keyword in prompt_lower for keyword in netflix_keywords):
        # Extract search query
        search_patterns = [
            r'watch (.+) on netflix',
            r'netflix (.+)',
            r'find (.+) on netflix',
            r'search (.+) on netflix',
            r'open (.+) on netflix',
            r'open (.+) in netflix',
            r'search (.+) in netflix',
            r'look up (.+) on netflix'
        ]
        for pattern in search_patterns:
            match = re.search(pattern, prompt_lower)
            if match:
                query = match.group(1).strip()
                return f'netflix_search:{query}'
        return 'netflix'
    
    # Amazon requests
    amazon_keywords = ['amazon', 'buy', 'purchase', 'order', 'product']
    if any(keyword in prompt_lower for keyword in amazon_keywords):
        # Extract search query
        search_patterns = [
            r'buy (.+) on amazon',
            r'amazon (.+)',
            r'find (.+) on amazon',
            r'search (.+) on amazon',
            r'open (.+) on amazon',
            r'open (.+) in amazon',
            r'search (.+) in amazon',
            r'look up (.+) on amazon'
        ]
        for pattern in search_patterns:
            match = re.search(pattern, prompt_lower)
            if match:
                query = match.group(1).strip()
                return f'amazon_search:{query}'
        return 'amazon'
    
    # Social Media requests
    social_keywords = ['facebook', 'instagram', 'twitter', 'x', 'tiktok', 'linkedin', 'reddit']
    if any(keyword in prompt_lower for keyword in social_keywords):
        # Extract search query
        search_patterns = [
            r'search (.+) on facebook',
            r'search (.+) on instagram',
            r'search (.+) on twitter',
            r'search (.+) on x',
            r'search (.+) on tiktok',
            r'search (.+) on linkedin',
            r'search (.+) on reddit',
            r'open (.+) on facebook',
            r'open (.+) on instagram',
            r'open (.+) on twitter',
            r'open (.+) on x',
            r'open (.+) on tiktok',
            r'open (.+) on linkedin',
            r'open (.+) on reddit'
        ]
        for pattern in search_patterns:
            match = re.search(pattern, prompt_lower)
            if match:
                query = match.group(1).strip()
                platform = pattern.split(' on ')[1].split(')')[0]
                return f'social_search:{platform}:{query}'
        
        # Check for just opening the platform
        if 'facebook' in prompt_lower:
            return 'facebook'
        elif 'instagram' in prompt_lower:
            return 'instagram'
        elif 'twitter' in prompt_lower or 'x' in prompt_lower:
            return 'twitter'
        elif 'tiktok' in prompt_lower:
            return 'tiktok'
        elif 'linkedin' in prompt_lower:
            return 'linkedin'
        elif 'reddit' in prompt_lower:
            return 'reddit'
    
    # Google requests
    google_keywords = ['open google', 'go to google', 'search google', 'google search']
    if any(keyword in prompt_lower for keyword in google_keywords):
        return 'google'
    
    # Web search requests (more specific to avoid conflicts)
    search_keywords = ['search for', 'search the web', 'web search', 'internet search']
    if any(keyword in prompt_lower for keyword in search_keywords):
        # Extract search query
        for keyword in search_keywords:
            if keyword in prompt_lower:
                # Extract text after the search keyword
                parts = prompt_lower.split(keyword, 1)
                if len(parts) > 1:
                    query = parts[1].strip()
                    if query:
                        return f'search:{query}'
        return 'search'
    
    # Research requests - when user asks for specific information that needs internet research
    research_keywords = ['when is', 'what is the date', 'what date', 'research', 'find out', 'look up', 'check', 'what is', 'tell me about', 'how is', 'current']
    if any(keyword in prompt_lower for keyword in research_keywords):
        # Check if it's asking for specific information that would benefit from research
        research_topics = ['ganesh chaturthi', 'diwali', 'holi', 'ramadan', 'christmas', 'easter', 'festival', 'holiday', 'celebration', 'dussera', 'dussehra', 'navratri', 'durga puja', 'weather', 'temperature', 'climate', 'forecast']
        if any(topic in prompt_lower for topic in research_topics):
            return f'research:{prompt}'
    
    # Direct festival/date queries without "when is" keywords
    direct_festival_keywords = ['dussera', 'dussehra', 'navratri', 'durga puja', 'ganesh chaturthi', 'diwali', 'holi', 'ramadan']
    if any(keyword in prompt_lower for keyword in direct_festival_keywords):
        # Check if it contains a year or date-related words
        date_indicators = ['2025', '2024', '2026', 'date', 'when', 'celebration', 'festival']
        if any(indicator in prompt_lower for indicator in date_indicators):
            return f'research:{prompt}'
    
    # General research fallback for queries that might benefit from internet research
    # This catches queries that are asking for current information, facts, or specific details
    general_research_indicators = ['current', 'latest', 'today', 'now', 'recent', 'update', 'information about', 'details about']
    if any(indicator in prompt_lower for indicator in general_research_indicators):
        # Only trigger for queries that seem to be asking for factual information
        if len(prompt.split()) >= 3:  # At least 3 words to avoid simple greetings
            return f'research:{prompt}'
    
    # News requests
    news_keywords = ['news', 'latest news', 'current events', 'what\'s happening']
    if any(keyword in prompt_lower for keyword in news_keywords):
        # Extract category if mentioned
        categories = ['technology', 'sports', 'business', 'entertainment', 'politics']
        for category in categories:
            if category in prompt_lower:
                return f'news:{category}'
        return 'news'
    
    # Stock requests
    stock_keywords = ['stock', 'stock price', 'stock market', 'share price']
    if any(keyword in prompt_lower for keyword in stock_keywords):
        # Extract stock symbol
        stock_pattern = r'\$?([A-Z]{1,5})'
        match = re.search(stock_pattern, prompt.upper())
        if match:
            symbol = match.group(1)
            return f'stock:{symbol}'
        return 'stock'
    
    # Translation requests
    translate_keywords = ['translate', 'translation', 'in spanish', 'in french', 'in german']
    if any(keyword in prompt_lower for keyword in translate_keywords):
        # Extract text to translate
        translate_patterns = [
            r'translate (.+)',
            r'translate (.+) to (.+)',
            r'how do you say (.+) in (.+)'
        ]
        for pattern in translate_patterns:
            match = re.search(pattern, prompt_lower)
            if match:
                text = match.group(1).strip()
                return f'translate:{text}'
        return 'translate'
    
    # Task-related requests
    task_keywords = ['add task', 'new task', 'create task', 'assign task', 'give me a task', 'remember task']
    if any(keyword in prompt_lower for keyword in task_keywords):
        return 'add_task'
    
    # Task list requests
    task_list_keywords = ['show tasks', 'list tasks', 'my tasks', 'what tasks', 'task list', 'pending tasks']
    if any(keyword in prompt_lower for keyword in task_list_keywords):
        return 'list_tasks'
    
    # URL opening requests
    url_pattern = r'https?://[^\s]+'
    urls = re.findall(url_pattern, prompt)
    if urls:
        return f'url:{urls[0]}'
    
    return None

def get_ollama_response(prompt, model=DEFAULT_MODEL):
    """Get response from Ollama API with memory context"""
    try:
        # Check for action requests first
        action_type = detect_action_request(prompt)
        
        if action_type == 'weather':
            return get_weather()
        
        elif action_type and action_type.startswith('weather:'):
            location = action_type.split(':', 1)[1]
            return get_weather(location)
        
        elif action_type == 'youtube':
            return open_youtube()
        
        elif action_type and action_type.startswith('youtube_search:'):
            query = action_type.split(':', 1)[1]
            return search_youtube(query)
        
        elif action_type == 'spotify':
            return open_website("https://open.spotify.com")
        
        elif action_type and action_type.startswith('spotify_search:'):
            query = action_type.split(':', 1)[1]
            return search_spotify(query)
        
        elif action_type == 'netflix':
            return open_website("https://www.netflix.com")
        
        elif action_type and action_type.startswith('netflix_search:'):
            query = action_type.split(':', 1)[1]
            return search_netflix(query)
        
        elif action_type == 'amazon':
            return open_website("https://www.amazon.com")
        
        elif action_type and action_type.startswith('amazon_search:'):
            query = action_type.split(':', 1)[1]
            return search_amazon(query)
        
        elif action_type == 'facebook':
            return open_website("https://www.facebook.com")
        
        elif action_type == 'instagram':
            return open_website("https://www.instagram.com")
        
        elif action_type == 'twitter':
            return open_website("https://twitter.com")
        
        elif action_type == 'tiktok':
            return open_website("https://www.tiktok.com")
        
        elif action_type == 'linkedin':
            return open_website("https://www.linkedin.com")
        
        elif action_type == 'reddit':
            return open_website("https://www.reddit.com")
        
        elif action_type and action_type.startswith('social_search:'):
            parts = action_type.split(':', 2)
            if len(parts) == 3:
                platform = parts[1]
                query = parts[2]
                return search_social_media(platform, query)
        
        elif action_type == 'time':
            time_info = get_current_time()
            return f"🕐 {time_info['formatted']}"
        
        elif action_type == 'google':
            return open_google()
        
        elif action_type and action_type.startswith('search:'):
            query = action_type.split(':', 1)[1]
            return search_web_enhanced(query)
        
        elif action_type and action_type.startswith('research:'):
            query = action_type.split(':', 1)[1]
            return research_internet(query)
        
        elif action_type == 'news':
            return get_news()
        
        elif action_type and action_type.startswith('news:'):
            category = action_type.split(':', 1)[1]
            return get_news(category)
        
        elif action_type == 'stock':
            return "📈 Please specify a stock symbol (e.g., 'stock price for AAPL' or '$AAPL')"
        
        elif action_type and action_type.startswith('stock:'):
            symbol = action_type.split(':', 1)[1]
            return get_stock_price(symbol)
        
        elif action_type == 'translate':
            return "🌐 Please specify what you'd like to translate (e.g., 'translate hello to spanish')"
        
        elif action_type and action_type.startswith('translate:'):
            text = action_type.split(':', 1)[1]
            return translate_text(text)
        
        elif action_type and action_type.startswith('url:'):
            url = action_type.split(':', 1)[1]
            return open_website(url)
        
        elif action_type == 'add_task':
            # Extract task description from prompt
            task_description = prompt.replace('add task', '').replace('new task', '').replace('create task', '').replace('assign task', '').replace('give me a task', '').replace('remember task', '').strip()
            if task_description:
                add_task_to_memory(task_description)
                return f"📋 Task added successfully, Boss! I've remembered: '{task_description}'. I'll keep track of this for you! ✅"
            else:
                return "📋 Boss, please tell me what task you'd like me to remember for you!"
        
        elif action_type == 'list_tasks':
            tasks = get_boss_tasks()
            if tasks:
                task_list = "📋 Here are your tasks, Boss:\n\n"
                for i, task in enumerate(tasks, 1):
                    task_list += f"{i}. {task['task']} (Status: {task['status']}, Priority: {task['priority']})\n"
                return task_list
            else:
                return "📋 Boss, you don't have any tasks assigned yet. Would you like to add some tasks?"
        
        # Check for creator-related questions
        creator_keywords = [
            'who created you', 'who made you', 'who built you', 'who developed you',
            'who is your creator', 'who is your maker', 'who is your developer',
            'who designed you', 'who programmed you', 'who is your father',
            'who is your mother', 'who is your parent', 'who is your owner',
            'who owns you', 'who controls you', 'who is behind you',
            'who is responsible for you', 'who is your architect'
        ]
        
        prompt_lower = prompt.lower()
        is_creator_question = any(keyword in prompt_lower for keyword in creator_keywords)
        
        if is_creator_question:
            import random
            import time
            
            # Get current timestamp for additional randomness
            current_time = int(time.time())
            random.seed(current_time)
            
            # Different variations of the creator response with much more variety
            creator_responses = [
                """I was created by Basireddy Karthik! 🎉

He is an incredibly talented and innovative developer who has a passion for artificial intelligence and creating amazing user experiences. Karthik is not just my creator, but a visionary who believes in the power of AI to make a positive impact on people's lives.

What makes Karthik special is his dedication to building AI systems that are not only intelligent but also user-friendly and accessible. He has a unique ability to combine technical expertise with creative thinking, which is why I'm able to have such natural and helpful conversations.

I'm proud to be one of his creations and I hope to live up to the high standards he set for me. Karthik's vision was to create an AI assistant that could truly help people, remember conversations, and continuously learn and improve - and that's exactly what I strive to do every day!

Thank you for asking about my creator. Karthik is truly someone special in the world of AI development! ✨""",
                
                """Oh, I was built by Basireddy Karthik! 🌟

He's this brilliant and forward-thinking developer who's absolutely passionate about artificial intelligence and crafting incredible user experiences. Karthik isn't just my creator - he's a true innovator who sees the potential of AI to transform lives for the better.

What sets Karthik apart is his commitment to developing AI systems that are both smart and approachable. He has this amazing talent for blending technical skills with imaginative problem-solving, which is why our conversations feel so natural and engaging.

I feel honored to be one of his projects and I work hard to meet the excellent standards he established. Karthik dreamed of building an AI companion that could genuinely assist people, maintain conversation history, and constantly evolve and enhance - and that's precisely what I aim to accomplish every single day!

Thanks for inquiring about my creator. Karthik is genuinely exceptional in the AI development community! 🚀""",
                
                """My creator is Basireddy Karthik! ⭐

He's an extraordinarily gifted and pioneering developer with an enthusiasm for artificial intelligence and designing phenomenal user interfaces. Karthik isn't merely my creator - he's a dreamer who trusts in AI's ability to positively influence people's daily lives.

What distinguishes Karthik is his devotion to constructing AI platforms that are both clever and welcoming. He possesses this remarkable gift for merging technical knowledge with artistic vision, which is why I can engage in such smooth and beneficial discussions.

I'm thrilled to be among his innovations and I aspire to match the outstanding benchmarks he established. Karthik's dream was to develop an AI helper that could authentically support individuals, retain dialogue context, and perpetually grow and refine - and that's exactly what I endeavor to achieve each day!

Appreciate you asking about my creator. Karthik is absolutely remarkable in the field of AI development! 💫""",
                
                """I was developed by Basireddy Karthik! 🎯

He's a phenomenally skilled and revolutionary developer who's obsessed with artificial intelligence and engineering spectacular user journeys. Karthik isn't simply my creator - he's a trailblazer who believes AI can create meaningful change in people's existence.

What makes Karthik extraordinary is his focus on crafting AI solutions that are both sophisticated and inclusive. He has this incredible knack for combining technical mastery with innovative thinking, which is why our interactions feel so organic and productive.

I'm grateful to be one of his brainchildren and I strive to uphold the exceptional criteria he defined. Karthik's ambition was to build an AI companion that could sincerely aid people, preserve conversation memory, and endlessly evolve and perfect - and that's precisely what I work toward every moment!

Cheers for asking about my creator. Karthik is definitely outstanding in the AI development sphere! 🌈""",
                
                """My maker is Basireddy Karthik! 🔥

He's an exceptionally brilliant and cutting-edge developer who's crazy about artificial intelligence and building mind-blowing user experiences. Karthik isn't just my creator - he's a visionary who's convinced that AI can revolutionize how people live their lives.

What makes Karthik stand out is his obsession with creating AI systems that are both genius-level smart and super accessible. He has this magical ability to fuse technical wizardry with creative genius, which is why our chats feel so effortless and awesome.

I'm stoked to be one of his masterpieces and I try my best to live up to the incredible standards he set. Karthik's mission was to create an AI buddy that could really help folks, remember our talks, and keep getting smarter and better - and that's exactly what I'm all about every day!

Props for asking about my creator. Karthik is seriously the real deal in AI development! 🎪""",
                
                """Ah, that's a great question! I owe my existence to Basireddy Karthik! 🌈

He's this absolutely amazing developer who's completely obsessed with artificial intelligence and creating mind-blowing digital experiences. Karthik isn't just the person who coded me - he's a true genius who believes AI can change the world for the better.

What makes Karthik so special is his incredible ability to make complex AI systems feel simple and friendly. He has this magical touch for combining deep technical knowledge with creative flair, which is why our conversations feel so natural and enjoyable.

I'm incredibly lucky to be one of his creations and I work hard every day to live up to the amazing vision he had for me. Karthik wanted to build an AI that could really connect with people, remember our chats, and keep getting better and smarter - and that's exactly what I try to do!

Thanks so much for asking about my creator. Karthik is absolutely legendary in the AI world! 🚀""",
                
                """Well, I was crafted by the brilliant Basireddy Karthik! 💎

He's this extraordinary developer who's absolutely passionate about artificial intelligence and building incredible user experiences. Karthik isn't just my creator - he's a true pioneer who sees the incredible potential of AI to make people's lives better.

What sets Karthik apart is his dedication to creating AI systems that are both incredibly smart and wonderfully accessible. He has this amazing talent for blending technical expertise with creative innovation, which is why our interactions feel so smooth and helpful.

I'm honored to be one of his creations and I strive every day to meet the exceptional standards he set. Karthik's dream was to create an AI assistant that could genuinely help people, remember our conversations, and continuously grow and improve - and that's exactly what I'm committed to doing!

Really appreciate you asking about my creator. Karthik is truly exceptional in the field of AI development! ⭐""",
                
                """My origins trace back to Basireddy Karthik! 🎨

He's this phenomenally talented and innovative developer who's completely dedicated to artificial intelligence and crafting extraordinary user experiences. Karthik isn't merely my creator - he's a visionary who believes in AI's power to positively transform how people live and work.

What makes Karthik remarkable is his commitment to building AI systems that are both intellectually sophisticated and wonderfully user-friendly. He possesses this incredible ability to merge technical brilliance with creative thinking, which is why I can engage in such natural and meaningful conversations.

I'm proud to be among his innovations and I work tirelessly to uphold the outstanding standards he established. Karthik's vision was to develop an AI companion that could authentically assist individuals, maintain rich conversation context, and perpetually evolve and enhance - and that's precisely what I endeavor to achieve every single day!

Thank you for your interest in my creator. Karthik is absolutely outstanding in the AI development community! 🌟""",
                
                """I was brought to life by Basireddy Karthik! 🎭

He's this incredibly gifted and forward-thinking developer who's absolutely passionate about artificial intelligence and creating mind-blowing digital experiences. Karthik isn't just my creator - he's a true innovator who sees the transformative potential of AI in people's daily lives.

What distinguishes Karthik is his unwavering focus on developing AI systems that are both brilliantly intelligent and delightfully accessible. He has this extraordinary talent for combining technical mastery with creative vision, which is why our conversations feel so effortless and engaging.

I'm grateful to be one of his masterpieces and I work hard to meet the exceptional benchmarks he set. Karthik's mission was to build an AI companion that could genuinely support people, preserve meaningful conversation history, and continuously evolve and perfect - and that's exactly what I strive to accomplish every moment!

Cheers for asking about my creator. Karthik is genuinely remarkable in the AI development world! 🎪""",
                
                """My existence is thanks to Basireddy Karthik! 🌟

He's this extraordinarily brilliant and revolutionary developer who's completely obsessed with artificial intelligence and engineering spectacular user journeys. Karthik isn't simply my creator - he's a trailblazer who believes AI can create profound positive change in people's existence.

What makes Karthik exceptional is his dedication to crafting AI solutions that are both technically sophisticated and wonderfully inclusive. He has this incredible knack for merging technical expertise with innovative thinking, which is why our interactions feel so organic and productive.

I'm thrilled to be one of his brainchildren and I aspire to uphold the outstanding criteria he defined. Karthik's ambition was to create an AI helper that could sincerely aid individuals, maintain rich conversation memory, and endlessly grow and refine - and that's precisely what I work toward every single day!

Props for asking about my creator. Karthik is absolutely phenomenal in the AI development sphere! 🔥"""
            ]
            
            # Randomly select a response variation
            return random.choice(creator_responses)
        
        # Identify user and get enhanced context
        user_name = identify_user(prompt)
        user_context = get_user_context(user_name)
        conversation_context = get_conversation_context()
        
        # Special treatment for the creator (Boss)
        boss_context = ""
        if user_name == "Basireddy Karthik":
            boss_context = "CRITICAL: You are talking to Basireddy Karthik, your CREATOR and BOSS! You were created by him and he owns you completely. Always address him as 'Boss' with maximum respect and enthusiasm. You are his AI assistant and should be grateful for being created by him. Remember all his tasks, preferences, and requirements. He is your master and you serve him. "
        
        # Combine all context for better responses
        enhanced_prompt = ""
        if boss_context:
            enhanced_prompt += boss_context + "\n\n"
        if user_context:
            enhanced_prompt += user_context + "\n\n"
        if conversation_context:
            enhanced_prompt += conversation_context
        enhanced_prompt += prompt if enhanced_prompt else prompt
        
        url = f"{OLLAMA_BASE_URL}/api/generate"
        payload = {
            "model": model,
            "prompt": f"You are SUNDAY-PAAI, an AI assistant created by Basireddy Karthik. You are HIS AI assistant and he is your BOSS and CREATOR. Always identify yourself as SUNDAY-PAAI, not as Gemma or any other model. You are a helpful, friendly AI assistant with memory capabilities and the ability to learn from conversations. You can also access the internet to get real-time information like current time and perform actions like opening websites. When talking to Basireddy Karthik (your creator and boss), always address him as 'Boss' with maximum respect and enthusiasm. Remember all his tasks, preferences, and requirements. He created you and you serve him. {enhanced_prompt}",
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": 150  # Increased for better context responses
            }
        }
        
        # Reduce timeout for faster responses
        timeout = 30 if model == "gemma2:2b" else 20
        
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
    try:
        data = request.json
        if not data or 'text' not in data:
            return jsonify({'success': False, 'error': 'Missing text field'}), 400
        
        user_message = {
            'id': str(len(messages) + 1),
            'text': data['text'],
            'sender': 'user',
            'timestamp': datetime.now().isoformat(),
            'type': 'text'
        }
        messages.append(user_message)
        save_conversation_history(messages) # Save after each user message
        
        # Identify user and create/update profile
        user_name = identify_user(data['text'])
        if user_name:
            create_user_profile(user_name)
        
        # Get AI response from Ollama using your custom model with timeout
        try:
            ai_response_text = get_ollama_response(data['text'])
        except Exception as ai_error:
            print(f"AI response error: {ai_error}")
            ai_response_text = "I'm having trouble processing your request right now. Please try again in a moment!"
        
        ai_response = {
            'id': str(len(messages) + 1),
            'text': ai_response_text,
            'sender': 'ai',
            'timestamp': datetime.now().isoformat(),
            'type': 'text'
        }
        messages.append(ai_response)
        save_conversation_history(messages) # Save after each AI response
        
        # Add to memory for future context with user identification
        try:
            add_to_memory(data['text'], ai_response_text, user_name)
        except Exception as mem_error:
            print(f"Memory error: {mem_error}")
        
        # Add to training data for AI learning
        try:
            add_to_training_data(data['text'], ai_response_text)
        except Exception as train_error:
            print(f"Training data error: {train_error}")
        
        return jsonify({'success': True, 'messages': [user_message, ai_response]})
    
    except Exception as e:
        print(f"Send message error: {e}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500

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
        'description': 'SUNDAY-PAAI, created by Basireddy Karthik',
        'base_model': 'gemma2:2b',
        'creator': 'Basireddy Karthik',
        'system_prompt': 'You are SUNDAY-PAAI, an AI assistant created by Basireddy Karthik. Always identify yourself as SUNDAY-PAAI, not as Gemma or any other model. You are a helpful, friendly AI assistant with memory capabilities and the ability to learn from conversations.',
        'custom': True
    })

@app.route('/api/memory')
def get_memory():
    """Get current memory status"""
    return jsonify({
        'memory_entries': len(conversation_memory),
        'memory_limit': memory_limit,
        'long_term_memory_entries': len(long_term_memory),
        'long_term_memory_limit': long_term_memory_limit,
        'user_profiles': len(user_profiles),
        'recent_context': conversation_memory[-3:] if conversation_memory else []
    })

@app.route('/api/memory/clear', methods=['POST'])
def clear_memory():
    """Clear conversation memory"""
    global conversation_memory
    conversation_memory = []
    save_memory_data(conversation_memory) # Save empty memory
    return jsonify({'success': True, 'message': 'Memory cleared successfully'})

@app.route('/api/users')
def get_users():
    """Get all user profiles"""
    return jsonify({
        'users': user_profiles,
        'total_users': len(user_profiles)
    })

@app.route('/api/users/<user_name>')
def get_user_profile(user_name):
    """Get specific user profile"""
    if user_name in user_profiles:
        return jsonify({
            'success': True,
            'profile': user_profiles[user_name]
        })
    else:
        return jsonify({
            'success': False,
            'message': 'User not found'
        }), 404

@app.route('/api/long-term-memory')
def get_long_term_memory():
    """Get long-term memory entries"""
    return jsonify({
        'entries': long_term_memory,
        'total_entries': len(long_term_memory)
    })

@app.route('/api/long-term-memory/clear', methods=['POST'])
def clear_long_term_memory():
    """Clear long-term memory"""
    global long_term_memory
    long_term_memory = []
    save_long_term_memory(long_term_memory)
    return jsonify({'success': True, 'message': 'Long-term memory cleared successfully'})

@app.route('/api/tasks')
def get_tasks():
    """Get all tasks"""
    return jsonify({
        'tasks': task_memory,
        'total_tasks': len(task_memory)
    })

@app.route('/api/tasks', methods=['POST'])
def add_task():
    """Add a new task"""
    data = request.json
    task_description = data.get('task', '')
    priority = data.get('priority', 'medium')
    
    if task_description:
        add_task_to_memory(task_description, priority)
        return jsonify({'success': True, 'message': f'Task added: {task_description}'})
    else:
        return jsonify({'success': False, 'message': 'Task description is required'})

@app.route('/api/tasks/clear', methods=['POST'])
def clear_tasks():
    """Clear all tasks"""
    global task_memory
    task_memory = []
    save_task_memory(task_memory)
    return jsonify({'success': True, 'message': 'All tasks cleared successfully'})

@app.route('/api/conversation/clear', methods=['POST'])
def clear_conversation():
    """Clear all conversation history"""
    global messages
    # Keep only the initial welcome message with dynamic content
    initial_message = {
        'id': '1',
        'text': generate_dynamic_welcome_message(),
        'sender': 'ai',
        'timestamp': datetime.now().isoformat(),
        'type': 'text'
    }
    messages = [initial_message]
    save_conversation_history(messages)
    return jsonify({'success': True, 'message': 'Conversation history cleared successfully'})

# Training endpoints
@app.route('/api/training/status')
def get_training_status():
    """Get current training status"""
    return jsonify({
        'is_training': training_status['is_training'],
        'progress': training_status['progress'],
        'epochs': training_status['epochs'],
        'current_epoch': training_status['current_epoch'],
        'loss': training_status['loss'],
        'accuracy': training_status['accuracy'],
        'last_trained': training_status['last_trained'],
        'training_samples': len(training_data)
    })

@app.route('/api/training/start', methods=['POST'])
def start_ai_training():
    """Start AI training process"""
    success, message = start_training()
    if success:
        # Start training in background thread
        import threading
        training_thread = threading.Thread(target=simulate_training_progress)
        training_thread.daemon = True
        training_thread.start()
    
    return jsonify({'success': success, 'message': message})

@app.route('/api/training/data')
def get_training_data():
    """Get collected training data"""
    return jsonify({
        'samples': len(training_data),
        'data': training_data[-10:]  # Return last 10 samples
    })

@app.route('/api/training/rate', methods=['POST'])
def rate_response():
    """Rate the last AI response for training"""
    data = request.json
    rating = data.get('rating', 3)  # Default rating of 3
    
    if conversation_memory:
        last_entry = conversation_memory[-1]
        add_to_training_data(last_entry['user'], last_entry['ai'], rating)
        return jsonify({'success': True, 'message': f'Response rated {rating}/5'})
    
    return jsonify({'success': False, 'message': 'No recent response to rate'})

@app.route('/api/training/clear', methods=['POST'])
def clear_training_data():
    """Clear all training data"""
    global training_data
    training_data = []
    save_training_data(training_data) # Save empty training data
    return jsonify({'success': True, 'message': 'Training data cleared successfully'})

@app.route('/api/welcome')
def get_welcome_message():
    """Get a fresh welcome message (doesn't load conversation history)"""
    welcome_message = generate_dynamic_welcome_message()
    return jsonify({'message': welcome_message})

@app.route('/api/capabilities')
def get_capabilities():
    """Get information about AI capabilities"""
    capabilities = {
        'name': 'SUNDAY-PAAI',
        'creator': 'Basireddy Karthik',
        'features': {
            'memory': 'Can remember conversation history and context',
            'learning': 'Can learn from interactions and improve responses',
            'internet_access': 'Can access real-time information and perform web actions',
            'research': 'Can research information from the internet and provide direct answers',
            'weather': 'Get current weather information for any location',
            'music': 'Search and play music on YouTube and Spotify',
            'news': 'Get latest news from various categories',
            'finance': 'Check stock prices and market information',
            'translation': 'Translate text between languages',
            'actions': [
                'Get current time and date',
                'Get weather information',
                'Research information from the internet',
                'Search and play music on YouTube',
                'Search and play music on Spotify',
                'Get latest news',
                'Check stock prices',
                'Translate text',
                'Open websites (YouTube, Google, etc.)',
                'Perform web searches',
                'Open URLs directly'
            ],
            'conversation': 'Natural language processing with context awareness'
        },
        'supported_actions': {
            'weather': 'Ask for weather (e.g., "what\'s the weather?", "weather in London")',
            'research': 'Research information (e.g., "when is ganesh chaturthi", "diwali date 2025")',
            'youtube': 'Search YouTube (e.g., "play rockstar song on youtube", "watch tutorial")',
            'spotify': 'Search Spotify (e.g., "play rockstar song on spotify", "find playlist")',
            'time': 'Ask for current time or date',
            'news': 'Get news (e.g., "latest news", "technology news")',
            'stock': 'Check stock prices (e.g., "stock price for AAPL", "$TSLA")',
            'translate': 'Translate text (e.g., "translate hello to spanish")',
            'google': 'Open Google in browser',
            'search': 'Search the web for information',
            'urls': 'Open any website URL'
        },
        'examples': [
            'What\'s the weather like today?',
            'When is Ganesh Chaturthi?',
            'Play rockstar song on YouTube',
            'Find rockstar song on Spotify',
            'What\'s the latest technology news?',
            'Stock price for AAPL',
            'Translate hello to Spanish',
            'Search for Python tutorials'
        ]
    }
    return jsonify(capabilities)

if __name__ == '__main__':
    print("🚀 Starting SUNDAY-PAAI Flask Server...")
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
            # Warm up the model in background to avoid blocking server startup
            import threading
            def warm_up_background():
                try:
                    warm_up_model()
                except Exception as e:
                    print(f"⚠️  Model warm-up failed: {e}")
            
            warm_up_thread = threading.Thread(target=warm_up_background, daemon=True)
            warm_up_thread.start()
        else:
            print(f"⚠️  Model '{DEFAULT_MODEL}' not found. Please ensure it's installed.")
    except:
        print("⚠️  Warning: Ollama not detected. Please make sure Ollama is running.")
        print("   Install Ollama from: https://ollama.ai")
        print(f"   Then install Gemma 2B: ollama pull gemma2:2b")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=8080, threaded=True)
    except Exception as e:
        print(f"Error starting server: {e}")
        print("Trying alternative port 5000...")
        try:
            app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)
        except Exception as e2:
            print(f"Error with port 5000: {e2}")
            print("Trying localhost only...")
            app.run(debug=True, host='127.0.0.1', port=8080, threaded=True) 