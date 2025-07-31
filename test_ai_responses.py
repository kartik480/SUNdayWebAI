import requests
import json

def test_ai_response(message):
    """Test the AI response for a given message"""
    try:
        response = requests.post('http://localhost:8080/api/messages', 
                               json={'text': message}, 
                               timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success') and len(data.get('messages', [])) >= 2:
                ai_response = data['messages'][1]['text']
                print(f"✅ Test: '{message}'")
                print(f"🤖 AI Response: {ai_response}")
                print(f"📏 Length: {len(ai_response)} characters")
                print("-" * 50)
                return True
            else:
                print(f"❌ Test failed: {message} - No AI response")
                return False
        else:
            print(f"❌ Test failed: {message} - HTTP {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {message} - Error: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing SUNDAY-PAAI AI Responses...")
    print("=" * 50)
    
    # Test cases
    test_messages = [
        "hi",
        "who created you",
        "who made you",
        "who is karthik",
        "how are you",
        "what can you do"
    ]
    
    success_count = 0
    for message in test_messages:
        if test_ai_response(message):
            success_count += 1
    
    print(f"\n📊 Results: {success_count}/{len(test_messages)} tests passed")
    
    if success_count == len(test_messages):
        print("🎉 All tests passed! AI is working perfectly!")
    else:
        print("⚠️ Some tests failed. Check the Flask server.") 