import requests
import subprocess

print("Testing Ollama...")

# Test 1: Check if ollama command works
try:
    result = subprocess.run(["ollama", "--version"], capture_output=True, text=True)
    print(f"Ollama version: {result.stdout}")
except Exception as e:
    print(f"Ollama not found: {e}")

# Test 2: Check if Ollama API responds
try:
    response = requests.get("http://localhost:11434/api/tags", timeout=5)
    print(f"API response: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        models = data.get('models', [])
        print(f"Found {len(models)} models")
        for model in models:
            print(f"  - {model['name']}")
except Exception as e:
    print(f"API error: {e}")

print("Test complete!") 