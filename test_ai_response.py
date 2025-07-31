import requests
import time

def test_ai_response():
    print("🧪 Testing AI Response...")
    
    # Wait a moment for Flask to start
    time.sleep(2)
    
    try:
        # Test 1: Check if Flask app is running
        response = requests.get("http://localhost:8080/api/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Flask app running - Status: {data.get('status')}")
            print(f"🤖 AI Provider: {data.get('ai_provider')}")
            print(f"🧠 Model: {data.get('model')}")
        else:
            print(f"❌ Flask app error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Flask app not responding: {e}")
        return False
    
    # Test 2: Send a test message
    try:
        test_message = "Hello! Can you respond to this test message?"
        print(f"\n📤 Sending test message: '{test_message}'")
        
        response = requests.post("http://localhost:8080/api/messages", 
                               json={"text": test_message}, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                messages = data.get('messages', [])
                if len(messages) >= 2:
                    ai_response = messages[1].get('text', 'No response')
                    print(f"✅ AI responded successfully!")
                    print(f"🤖 AI Response: {ai_response[:200]}...")
                    return True
                else:
                    print("❌ No AI response received")
                    return False
            else:
                print("❌ API request failed")
                return False
        else:
            print(f"❌ HTTP error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_ai_response()
    if success:
        print("\n🎉 SUCCESS! Your AI is working properly!")
        print("🌐 Open your browser to: http://localhost:8080")
        print("💬 Start chatting with your AI assistant!")
    else:
        print("\n⚠️  AI test failed. Check the errors above.") 