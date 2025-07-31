import requests
import time

def test_improved_ai():
    print("🧪 Testing Improved AI Responses...")
    
    # Wait for Flask to start
    time.sleep(3)
    
    test_messages = [
        "hi",
        "how are you?",
        "tell me a joke",
        "what's the weather like?"
    ]
    
    try:
        for i, message in enumerate(test_messages, 1):
            print(f"\n{i}. Testing: '{message}'")
            
            response = requests.post("http://localhost:8080/api/messages", 
                                   json={"text": message}, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    messages = data.get('messages', [])
                    if len(messages) >= 2:
                        ai_response = messages[1].get('text', 'No response')
                        print(f"   🤖 AI Response: {ai_response[:100]}...")
                        
                        # Check if response is improved
                        if "I understand you said" not in ai_response:
                            print("   ✅ Response is improved!")
                        else:
                            print("   ⚠️  Still using old template")
                    else:
                        print("   ❌ No AI response received")
                else:
                    print("   ❌ API request failed")
            else:
                print(f"   ❌ HTTP error: {response.status_code}")
                
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_improved_ai() 