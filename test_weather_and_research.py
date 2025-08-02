#!/usr/bin/env python3
"""
Comprehensive test for weather and research functionality
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the functions
from app import get_weather, research_internet, detect_action_request, get_ollama_response

def test_weather_and_research():
    """Test both weather and research functionality"""
    print("🧪 Testing Weather and Research Functionality...")
    print("=" * 60)
    
    # Test weather functionality
    print("\n🌤️ Testing Weather Functionality:")
    print("-" * 40)
    
    try:
        weather_result = get_weather()
        print(f"✅ Weather Result: {weather_result[:100]}...")
    except Exception as e:
        print(f"❌ Weather Error: {e}")
    
    # Test research functionality for various queries
    print("\n🔍 Testing Research Functionality:")
    print("-" * 40)
    
    test_queries = [
        "what is the weather in my location",
        "current weather today",
        "when is dussera in 2025",
        "what is the latest technology news",
        "current stock market status",
        "latest sports updates"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Testing: '{query}'")
        print("-" * 30)
        
        # Test action detection
        action = detect_action_request(query)
        print(f"Action detected: {action}")
        
        # Test research function directly
        try:
            if action and action.startswith('research:'):
                research_query = action.split(':', 1)[1]
                result = research_internet(research_query)
                print(f"✅ Research Result: {result[:150]}...")
            else:
                print("❌ No research action detected")
        except Exception as e:
            print(f"❌ Research Error: {e}")
    
    # Test full AI response for weather query
    print("\n🤖 Testing Full AI Response for Weather:")
    print("-" * 40)
    
    try:
        weather_query = "what's the weather in my location"
        ai_response = get_ollama_response(weather_query)
        print(f"✅ AI Response: {ai_response[:200]}...")
    except Exception as e:
        print(f"❌ AI Response Error: {e}")

if __name__ == "__main__":
    test_weather_and_research() 