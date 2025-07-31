import requests
import time

def test_ollama_direct():
    """Test Ollama directly to see response time"""
    url = "http://localhost:11434/api/generate"
    
    payload = {
        "model": "llama2:7b",
        "prompt": "Say hello in one sentence",
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": 100,
            "num_predict": 50
        }
    }
    
    print("🧪 Testing Ollama directly...")
    print(f"📤 Sending request to: {url}")
    print(f"🤖 Model: {payload['model']}")
    
    start_time = time.time()
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            ai_response = result.get('response', 'No response')
            response_time = end_time - start_time
            
            print(f"✅ Success!")
            print(f"🤖 Response: {ai_response}")
            print(f"⏱️ Time taken: {response_time:.2f} seconds")
            return True
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print(f"❌ Timeout after 10 seconds")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    test_ollama_direct() 