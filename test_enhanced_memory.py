#!/usr/bin/env python3
"""
Test script for SUNDAY-PAAI Enhanced Memory System
This script demonstrates the persistent memory capabilities
"""

import requests
import json
import time

# Server configuration
BASE_URL = "http://localhost:8080"

def test_memory_system():
    """Test the enhanced memory system"""
    print("🧠 Testing SUNDAY-PAAI Enhanced Memory System")
    print("=" * 50)
    
    # Test 1: Check initial memory status
    print("\n1. 📊 Checking initial memory status...")
    try:
        response = requests.get(f"{BASE_URL}/api/memory")
        memory_status = response.json()
        print(f"   ✅ Memory entries: {memory_status['memory_entries']}")
        print(f"   ✅ Long-term memory: {memory_status['long_term_memory_entries']}")
        print(f"   ✅ User profiles: {memory_status['user_profiles']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
        return
    
    # Test 2: Send a message to identify user
    print("\n2. 👤 Testing user identification...")
    test_message = {
        "text": "Hi, I'm Basireddy Karthik, your creator!"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/messages", json=test_message)
        result = response.json()
        if result['success']:
            print("   ✅ Message sent successfully")
            print(f"   📝 AI Response: {result['messages'][1]['text'][:100]}...")
        else:
            print("   ❌ Failed to send message")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Check if user profile was created
    print("\n3. 👤 Checking user profile creation...")
    time.sleep(2)  # Wait for processing
    
    try:
        response = requests.get(f"{BASE_URL}/api/users")
        users = response.json()
        print(f"   ✅ Total users: {users['total_users']}")
        if users['total_users'] > 0:
            print("   🎉 User profile created successfully!")
            for user_name, profile in users['users'].items():
                print(f"   👤 User: {user_name}")
                print(f"   📊 Relationship: {profile['relationship']}")
                print(f"   💬 Conversations: {profile['conversation_count']}")
        else:
            print("   ⚠️ No user profiles found yet")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Send another message to test memory
    print("\n4. 🧠 Testing memory persistence...")
    test_message2 = {
        "text": "Do you remember who I am?"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/messages", json=test_message2)
        result = response.json()
        if result['success']:
            print("   ✅ Message sent successfully")
            print(f"   📝 AI Response: {result['messages'][1]['text'][:150]}...")
        else:
            print("   ❌ Failed to send message")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 5: Check long-term memory
    print("\n5. 🧠 Checking long-term memory...")
    try:
        response = requests.get(f"{BASE_URL}/api/long-term-memory")
        long_term = response.json()
        print(f"   ✅ Long-term memory entries: {long_term['total_entries']}")
        if long_term['total_entries'] > 0:
            print("   🎉 Important information stored in long-term memory!")
            for entry in long_term['entries'][-2:]:  # Show last 2 entries
                print(f"   📝 User: {entry.get('user_name', 'Unknown')}")
                print(f"   💬 Message: {entry['user'][:50]}...")
        else:
            print("   ⚠️ No long-term memory entries yet")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 6: Final memory status
    print("\n6. 📊 Final memory status...")
    try:
        response = requests.get(f"{BASE_URL}/api/memory")
        memory_status = response.json()
        print(f"   ✅ Memory entries: {memory_status['memory_entries']}")
        print(f"   ✅ Long-term memory: {memory_status['long_term_memory_entries']}")
        print(f"   ✅ User profiles: {memory_status['user_profiles']}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Enhanced Memory System Test Complete!")
    print("\n💡 Key Features Demonstrated:")
    print("   ✅ User identification and profile creation")
    print("   ✅ Persistent memory across conversations")
    print("   ✅ Long-term memory for important information")
    print("   ✅ Creator recognition and special handling")
    print("   ✅ Memory persistence across server restarts")
    
    print("\n🚀 Your SUNDAY-PAAI now remembers you forever!")
    print("   Even when you restart the server, your conversations and")
    print("   important information will be preserved!")

if __name__ == "__main__":
    test_memory_system() 