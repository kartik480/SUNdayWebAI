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

app = Flask(__name__)

# Ollama configuration
OLLAMA_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "gemma2:2b"  

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
        get_ollama_response(warm_up_prompt, DEFAULT_MODEL)
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
    
    # Time-related requests
    time_keywords = ['what time', 'current time', 'what is the time', 'time now', 'what day', 'current date', 'today\'s date']
    if any(keyword in prompt_lower for keyword in time_keywords):
        return 'time'
    
    # YouTube requests
    youtube_keywords = ['open youtube', 'go to youtube', 'youtube', 'play youtube', 'watch youtube']
    if any(keyword in prompt_lower for keyword in youtube_keywords):
        return 'youtube'
    
    # Google requests
    google_keywords = ['open google', 'go to google', 'search google', 'google search']
    if any(keyword in prompt_lower for keyword in google_keywords):
        return 'google'
    
    # Web search requests
    search_keywords = ['search for', 'search', 'find', 'look up', 'google']
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
        
        if action_type == 'time':
            time_info = get_current_time()
            return f"🕐 {time_info['formatted']}"
        
        elif action_type == 'youtube':
            return open_youtube()
        
        elif action_type == 'google':
            return open_google()
        
        elif action_type and action_type.startswith('search:'):
            query = action_type.split(':', 1)[1]
            return search_web(query)
        
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
            
            # Different variations of the creator response
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

Props for asking about my creator. Karthik is seriously the real deal in AI development! 🎪"""
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
    save_conversation_history(messages) # Save after each user message
    
    # Identify user and create/update profile
    user_name = identify_user(data['text'])
    if user_name:
        create_user_profile(user_name)
    
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
    save_conversation_history(messages) # Save after each AI response
    
    # Add to memory for future context with user identification
    add_to_memory(data['text'], ai_response_text, user_name)
    
    # Add to training data for AI learning
    add_to_training_data(data['text'], ai_response_text)
    
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
            'actions': [
                'Get current time and date',
                'Open websites (YouTube, Google, etc.)',
                'Perform web searches',
                'Open URLs directly'
            ],
            'conversation': 'Natural language processing with context awareness'
        },
        'supported_actions': {
            'time': 'Ask for current time or date',
            'youtube': 'Open YouTube in browser',
            'google': 'Open Google in browser',
            'search': 'Search the web for information',
            'urls': 'Open any website URL'
        }
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