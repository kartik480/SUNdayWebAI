#!/usr/bin/env python3
"""
SUNDAY-PAAI Starter Script
"""

import subprocess
import sys
import time

def check_ollama():
    """Check if Ollama is running"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = data.get('models', [])
            print(f"✅ Ollama is running - Found {len(models)} models")
            for model in models:
                print(f"   📦 {model['name']}")
            return True
        else:
            print("❌ Ollama not responding")
            return False
    except Exception as e:
        print(f"❌ Ollama not running: {e}")
        print("💡 Start Ollama with: ollama serve")
        return False

def start_flask_app():
    """Start the Flask app"""
    print("\n🚀 Starting SUNDAY-PAAI Flask Server...")
    
    try:
        # Import and run the improved app
        from improved_app import app
        
        print("✅ Flask app imported successfully!")
        print("🌐 Server will be available at: http://localhost:8080")
        print("📋 Press Ctrl+C to stop the server")
        
        app.run(debug=True, host='127.0.0.1', port=8080)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure improved_app.py exists")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("💡 Trying alternative port...")
        try:
            app.run(debug=True, host='127.0.0.1', port=5000)
        except Exception as e2:
            print(f"❌ Error with port 5000: {e2}")

def main():
    print("🤖 SUNDAY-PAAI AI Assistant Starter")
    print("=" * 40)
    
    # Check Ollama first
    if not check_ollama():
        print("\n⚠️  Please start Ollama first:")
        print("   ollama serve")
        return
    
    # Start Flask app
    start_flask_app()

if __name__ == "__main__":
    main() 