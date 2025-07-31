#!/usr/bin/env python3
"""
SUNDAY-PAAI Custom Model Setup Script
This script helps you create and configure your custom kart_2003/sunday model
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a shell command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed!")
        print(f"Error: {e.stderr}")
        return False

def create_modelfile():
    """Create the Modelfile for the custom model"""
    modelfile_content = """FROM llama3.2
SYSTEM You are a friendly assistant named SUNDAY-PAAI. You are helpful, creative, and always ready to assist users with any task or question. You have a warm personality and provide thoughtful, accurate responses.
"""
    
    try:
        with open('Modelfile', 'w') as f:
            f.write(modelfile_content)
        print("✅ Modelfile created successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to create Modelfile: {e}")
        return False

def main():
    print("🚀 SUNDAY-PAAI Custom Model Setup")
    print("=" * 50)
    
    # Check if Ollama is installed
    if not run_command("ollama --version", "Checking Ollama installation"):
        print("❌ Ollama is not installed. Please install it first from https://ollama.ai")
        return
    
    # Pull the base model
    if not run_command("ollama pull llama3.2", "Pulling Llama 3.2 base model"):
        print("❌ Failed to pull Llama 3.2. Please check your internet connection.")
        return
    
    # Create Modelfile
    if not create_modelfile():
        return
    
    # Create the custom model
    if not run_command("ollama create -f Modelfile kart_2003/sunday", "Creating custom model kart_2003/sunday"):
        print("❌ Failed to create custom model.")
        return
    
    # List models to verify
    if run_command("ollama list", "Listing available models"):
        print("\n🎉 Custom model setup completed successfully!")
        print("\n📋 Next steps:")
        print("1. Start Ollama: ollama serve")
        print("2. Start SUNDAY-PAAI: python app.py")
        print("3. Access your AI: http://localhost:8080")
        print("\n🎯 Your custom model 'kart_2003/sunday' is now ready!")
    else:
        print("❌ Failed to verify model creation.")

if __name__ == "__main__":
    main() 