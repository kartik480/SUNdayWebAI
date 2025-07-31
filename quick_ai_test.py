import requests
import time

print("🧪 Quick AI Test")
print("=" * 30)

# Wait for Flask to start
time.sleep(3)

try:
    # Test 1: Check status
    print("1. Checking Flask app status...")
    response = requests.get("http://localhost:8080/api/status", timeout=5)
    if response.status_code == 200:
        data = response.json()
        print(f"   ✅ Status: {data.get('status')}")
        print(f"   🤖 AI Provider: {data.get('ai_provider')}")
        print(f"   🧠 Model: {data.get('model')}")
    else:
        print(f"   ❌ Error: {response.status_code}")
        exit(1)
    
    # Test 2: Send a simple message
    print("\n2. Testing AI response...")
    test_message = "Hello! How are you today?"
    print(f"   📤 Sending: '{test_message}'")
    
    response = requests.post("http://localhost:8080/api/messages", 
                           json={"text": test_message}, timeout=60)
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            messages = data.get('messages', [])
            if len(messages) >= 2:
                ai_response = messages[1].get('text', 'No response')
                print(f"   ✅ AI responded!")
                print(f"   🤖 Response: {ai_response[:150]}...")
                print("\n🎉 SUCCESS! Your AI is working!")
                print("🌐 Open: http://localhost:8080")
            else:
                print("   ❌ No AI response received")
        else:
            print("   ❌ API request failed")
    else:
        print(f"   ❌ HTTP error: {response.status_code}")
        
except Exception as e:
    print(f"❌ Test failed: {e}")
    print("\n💡 Make sure:")
    print("1. Ollama is running: ollama serve")
    print("2. Flask app is running: python simple_app.py")
    print("3. You have models downloaded: ollama list") 