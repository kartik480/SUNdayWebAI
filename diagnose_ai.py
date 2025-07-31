#!/usr/bin/env python3
"""
AI System Diagnostic Tool
Checks all components needed for AI functionality
"""

import requests
import subprocess
import sys
import os
import time

def check_ollama_installation():
    """Check if Ollama is installed"""
    print("🔍 Checking Ollama Installation...")
    try:
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Ollama installed: {result.stdout.strip()}")
            return True
        else:
            print("❌ Ollama command failed")
            return False
    except Exception as e:
        print(f"❌ Ollama not found: {e}")
        return False

def check_ollama_running():
    """Check if Ollama service is running"""
    print("\n🔍 Checking if Ollama is running...")
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            print(f"✅ Ollama is running - Found {len(models)} models")
            for model in models:
                print(f"   📦 {model['name']}")
            return True, models
        else:
            print(f"❌ Ollama API error: {response.status_code}")
            return False, []
    except Exception as e:
        print(f"❌ Ollama not responding: {e}")
        return False, []

def check_custom_model(models):
    """Check if custom model exists"""
    print("\n🔍 Checking for custom model...")
    custom_model = "kart_2003/sunday"
    model_names = [model['name'] for model in models]
    
    if custom_model in model_names:
        print(f"✅ Custom model '{custom_model}' found!")
        return True
    else:
        print(f"❌ Custom model '{custom_model}' not found")
        print(f"Available models: {', '.join(model_names)}")
        return False

def test_model_response():
    """Test if a model can respond"""
    print("\n🔍 Testing model response...")
    try:
        # Try with any available model first
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            
            if models:
                test_model = models[0]['name']
                print(f"🧪 Testing with model: {test_model}")
                
                payload = {
                    "model": test_model,
                    "prompt": "Hello! Can you respond?",
                    "stream": False
                }
                
                response = requests.post("http://localhost:11434/api/generate", 
                                       json=payload, timeout=30)
                if response.status_code == 200:
                    result = response.json()
                    ai_response = result.get('response', 'No response')
                    print(f"✅ Model responded: {ai_response[:100]}...")
                    return True
                else:
                    print(f"❌ Model test failed: {response.status_code}")
                    return False
            else:
                print("❌ No models available")
                return False
    except Exception as e:
        print(f"❌ Model test error: {e}")
        return False

def check_flask_app():
    """Check if Flask app is running"""
    print("\n🔍 Checking Flask app...")
    try:
        response = requests.get("http://localhost:8080/api/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Flask app is running!")
            print(f"   🤖 AI Provider: {data.get('ai_provider', 'Unknown')}")
            print(f"   🧠 Model: {data.get('model', 'Unknown')}")
            print(f"   📊 Status: {data.get('status', 'Unknown')}")
            return True
        else:
            print(f"❌ Flask app error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Flask app not responding: {e}")
        return False

def main():
    print("🚀 AI System Diagnostic Tool")
    print("=" * 50)
    
    # Check Ollama installation
    ollama_installed = check_ollama_installation()
    
    if not ollama_installed:
        print("\n❌ Ollama is not installed!")
        print("📥 Please install Ollama from: https://ollama.ai")
        return
    
    # Check if Ollama is running
    ollama_running, models = check_ollama_running()
    
    if not ollama_running:
        print("\n❌ Ollama is not running!")
        print("🚀 Start Ollama with: ollama serve")
        return
    
    # Check custom model
    custom_model_exists = check_custom_model(models)
    
    # Test model response
    model_responding = test_model_response()
    
    # Check Flask app
    flask_running = check_flask_app()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 DIAGNOSTIC SUMMARY")
    print("=" * 50)
    
    print(f"✅ Ollama Installed: {ollama_installed}")
    print(f"✅ Ollama Running: {ollama_running}")
    print(f"✅ Custom Model: {custom_model_exists}")
    print(f"✅ Model Responding: {model_responding}")
    print(f"✅ Flask App: {flask_running}")
    
    if all([ollama_installed, ollama_running, model_responding, flask_running]):
        print("\n🎉 All systems working! Your AI should respond properly.")
        print("🌐 Open your browser to: http://localhost:8080")
    else:
        print("\n⚠️  Some issues detected. Here's how to fix:")
        
        if not ollama_running:
            print("1. Start Ollama: ollama serve")
        
        if not custom_model_exists:
            print("2. Create custom model: python setup_custom_model.py")
        
        if not model_responding:
            print("3. Download a base model: ollama pull llama2")
        
        if not flask_running:
            print("4. Start Flask app: python app.py")

if __name__ == "__main__":
    main() 