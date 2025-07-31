#!/usr/bin/env python3
"""
SUNDAY-PAAI Custom Model Testing Script
This script helps you test your custom kart_2003/sunday model integration
"""

import subprocess
import requests
import json
import time
import sys

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False, e.stderr

def test_ollama_installation():
    """Test if Ollama is installed and running"""
    print("🧪 Testing Ollama Installation...")
    print("=" * 50)
    
    # Check if Ollama is installed
    success, output = run_command("ollama --version", "Checking Ollama installation")
    if not success:
        print("❌ Ollama is not installed!")
        print("📥 Please install Ollama from: https://ollama.ai")
        return False
    
    # Check if Ollama is running
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            print("✅ Ollama is running!")
            return True
        else:
            print("❌ Ollama is not responding!")
            return False
    except:
        print("❌ Ollama is not running!")
        print("🚀 Start Ollama with: ollama serve")
        return False

def test_custom_model_creation():
    """Test creating the custom model"""
    print("\n🧪 Testing Custom Model Creation...")
    print("=" * 50)
    
    # Create Modelfile
    modelfile_content = """FROM llama3.2
SYSTEM You are a friendly assistant named SUNDAY-PAAI. You are helpful, creative, and always ready to assist users with any task or question. You have a warm personality and provide thoughtful, accurate responses.
"""
    
    try:
        with open('Modelfile', 'w') as f:
            f.write(modelfile_content)
        print("✅ Modelfile created successfully!")
    except Exception as e:
        print(f"❌ Failed to create Modelfile: {e}")
        return False
    
    # Pull base model
    success, _ = run_command("ollama pull llama3.2", "Pulling Llama 3.2 base model")
    if not success:
        return False
    
    # Create custom model
    success, _ = run_command("ollama create -f Modelfile kart_2003/sunday", "Creating custom model")
    if not success:
        return False
    
    # List models to verify
    success, output = run_command("ollama list", "Listing available models")
    if success and "kart_2003/sunday" in output:
        print("✅ Custom model 'kart_2003/sunday' found!")
        return True
    else:
        print("❌ Custom model not found!")
        return False

def test_custom_model_response():
    """Test the custom model with a simple query"""
    print("\n🧪 Testing Custom Model Response...")
    print("=" * 50)
    
    test_prompt = "Hello! I'm testing SUNDAY-PAAI. Can you introduce yourself?"
    
    try:
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "kart_2003/sunday",
            "prompt": test_prompt,
            "stream": False
        }
        
        print(f"📤 Sending test prompt: '{test_prompt}'")
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        ai_response = result.get('response', 'No response received')
        
        print("✅ Custom model responded successfully!")
        print(f"🤖 AI Response: {ai_response[:200]}...")
        return True
        
    except Exception as e:
        print(f"❌ Custom model test failed: {e}")
        return False

def test_flask_integration():
    """Test the Flask app integration"""
    print("\n🧪 Testing Flask Integration...")
    print("=" * 50)
    
    try:
        # Test if Flask app is running
        response = requests.get("http://localhost:8080/api/status", timeout=5)
        if response.status_code == 200:
            status = response.json()
            print("✅ Flask app is running!")
            print(f"🤖 AI Provider: {status.get('ai_provider', 'Unknown')}")
            print(f"🧠 Model: {status.get('model', 'Unknown')}")
            print(f"📊 Status: {status.get('status', 'Unknown')}")
            return True
        else:
            print("❌ Flask app is not responding!")
            return False
    except:
        print("❌ Flask app is not running!")
        print("🚀 Start Flask app with: python app.py")
        return False

def test_end_to_end():
    """Test the complete end-to-end functionality"""
    print("\n🧪 Testing End-to-End Functionality...")
    print("=" * 50)
    
    try:
        # Test sending a message through the Flask API
        test_message = "Hello SUNDAY-PAAI! This is a test message."
        
        url = "http://localhost:8080/api/messages"
        payload = {"text": test_message}
        
        print(f"📤 Sending test message: '{test_message}'")
        response = requests.post(url, json=payload, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        if result.get('success'):
            messages = result.get('messages', [])
            if len(messages) >= 2:
                ai_response = messages[1].get('text', 'No response')
                print("✅ End-to-end test successful!")
                print(f"🤖 AI Response: {ai_response[:200]}...")
                return True
            else:
                print("❌ No AI response received!")
                return False
        else:
            print("❌ API request failed!")
            return False
            
    except Exception as e:
        print(f"❌ End-to-end test failed: {e}")
        return False

def main():
    print("🚀 SUNDAY-PAAI Custom Model Testing Suite")
    print("=" * 60)
    
    tests = [
        ("Ollama Installation", test_ollama_installation),
        ("Custom Model Creation", test_custom_model_creation),
        ("Custom Model Response", test_custom_model_response),
        ("Flask Integration", test_flask_integration),
        ("End-to-End Test", test_end_to_end)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("📊 TEST RESULTS SUMMARY")
    print("="*60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall Result: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your SUNDAY-PAAI custom model is working perfectly!")
        print("\n📋 Next steps:")
        print("1. Open your browser to: http://localhost:8080")
        print("2. Start chatting with your custom AI!")
        print("3. Try different prompts to test the model")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure Ollama is installed and running")
        print("2. Ensure your custom model is created")
        print("3. Check that Flask app is running")
        print("4. Verify network connectivity")

if __name__ == "__main__":
    main() 