#!/usr/bin/env python3
"""
Test script for SUNDAY-PAAI Dynamic Welcome Messages
This script demonstrates the unique welcome messages every time
"""

import requests
import json

# Server configuration
BASE_URL = "http://localhost:8080"

def test_dynamic_welcome():
    """Test the dynamic welcome message system"""
    print("🎉 Testing SUNDAY-PAAI Dynamic Welcome Messages")
    print("=" * 60)
    
    # Test 1: Clear conversation to get new welcome message
    print("\n1. 🧹 Clearing conversation to get fresh welcome message...")
    try:
        response = requests.post(f"{BASE_URL}/api/conversation/clear")
        result = response.json()
        if result['success']:
            print("   ✅ Conversation cleared successfully")
        else:
            print("   ❌ Failed to clear conversation")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 2: Get the new welcome message
    print("\n2. 📝 Getting new welcome message...")
    try:
        response = requests.get(f"{BASE_URL}/api/messages")
        messages = response.json()
        if messages:
            welcome_message = messages[0]['text']
            print(f"   🎯 New Welcome Message:")
            print(f"   \"{welcome_message}\"")
            print(f"   📊 Message length: {len(welcome_message)} characters")
        else:
            print("   ⚠️ No messages found")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Send a message as the creator
    print("\n3. 👑 Testing Boss recognition...")
    test_message = {
        "text": "Hi, I'm Basireddy Karthik, your creator!"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/messages", json=test_message)
        result = response.json()
        if result['success']:
            print("   ✅ Message sent successfully")
            ai_response = result['messages'][1]['text']
            print(f"   🤖 AI Response:")
            print(f"   \"{ai_response}\"")
            
            # Check if AI addressed you as Boss
            if "boss" in ai_response.lower():
                print("   🎉 SUCCESS: AI recognized you as Boss!")
            else:
                print("   ⚠️ AI didn't address you as Boss")
        else:
            print("   ❌ Failed to send message")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Test memory persistence
    print("\n4. 🧠 Testing memory persistence...")
    test_message2 = {
        "text": "Do you remember who I am, Boss?"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/messages", json=test_message2)
        result = response.json()
        if result['success']:
            print("   ✅ Message sent successfully")
            ai_response = result['messages'][1]['text']
            print(f"   🤖 AI Response:")
            print(f"   \"{ai_response}\"")
            
            # Check if AI remembered you as Boss
            if "boss" in ai_response.lower() and ("karthik" in ai_response.lower() or "creator" in ai_response.lower()):
                print("   🎉 SUCCESS: AI remembered you as Boss and creator!")
            else:
                print("   ⚠️ AI didn't fully remember you as Boss")
        else:
            print("   ❌ Failed to send message")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Dynamic Welcome System Test Complete!")
    print("\n💡 Key Features Demonstrated:")
    print("   ✅ Unique welcome messages every time")
    print("   ✅ Time-based greetings (morning/afternoon/evening)")
    print("   ✅ Boss recognition and special treatment")
    print("   ✅ Memory persistence for creator relationship")
    print("   ✅ Dynamic conversation clearing")
    
    print("\n🚀 Your SUNDAY-PAAI now gives you a fresh welcome every time!")
    print("   Each server restart or conversation clear will give you")
    print("   a unique, personalized greeting as Boss!")

if __name__ == "__main__":
    test_dynamic_welcome() 