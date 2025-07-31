import requests

print("Checking available models...")

try:
    response = requests.get("http://localhost:11434/api/tags", timeout=5)
    if response.status_code == 200:
        data = response.json()
        models = data.get('models', [])
        print(f"Found {len(models)} models:")
        for model in models:
            print(f"  ✅ {model['name']}")
        
        if models:
            print("\n🎉 Models are available! Your AI should work now.")
            print("🚀 Start your Flask app: python app.py")
        else:
            print("\n❌ No models found. Please download a model first.")
    else:
        print(f"❌ API error: {response.status_code}")
except Exception as e:
    print(f"❌ Error: {e}") 