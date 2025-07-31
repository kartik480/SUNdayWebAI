#!/usr/bin/env python3
"""
Quick Ollama Status Test
"""

import requests
import subprocess
import sys

def test_ollama():
    print("🔍 Quick Ollama Status Test")
    print("=" * 40)
    
    # Test 1: Check if ollama command exists
    try:
        result = subprocess.run(["ollama", "--version"], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"✅ Ollama installed: {result.stdout.strip()}")
        else:
            print("❌ Ollama command failed")
            return False
    except Exception as e:
        print(f"❌ Ollama not found: {e}")
        return False
    
    # Test 2: Check if Ollama API is responding
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            print(f"✅ Ollama API responding - Found {len(models)} models")
            for model in models:
                print(f"   📦 {model['name']}")
            return True
        else:
            print(f"❌ Ollama API error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ollama API not responding: {e}")
        print("💡 Try running: ollama serve")
        return False

if __name__ == "__main__":
    success = test_ollama()
    if success:
        print("\n🎉 Ollama is working! Your AI should respond.")
    else:
        print("\n⚠️  Ollama needs to be set up properly.")
        print("📋 Steps to fix:")
        print("1. Install Ollama from https://ollama.ai")
        print("2. Run: ollama serve")
        print("3. Download a model: ollama pull llama2")
        print("4. Create custom model: python setup_custom_model.py") 