import subprocess
import sys
import time

def run_command(command, description):
    """Run a command and show output"""
    print(f"🔄 {description}...")
    print(f"📝 Command: {command}")
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print(f"✅ {description} completed successfully!")
            if result.stdout:
                print(f"📄 Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} failed!")
            if result.stderr:
                print(f"📄 Error: {result.stderr.strip()}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏱️ {description} timed out after 5 minutes")
        return False
    except Exception as e:
        print(f"❌ {description} error: {e}")
        return False

def main():
    print("🚀 Setting up MythoMax L2 13B Model...")
    print("=" * 50)
    
    # Step 1: Check if Ollama is running
    print("🔍 Step 1: Checking Ollama status...")
    if not run_command("ollama list", "Checking available models"):
        print("❌ Ollama might not be running. Please start Ollama first:")
        print("   ollama serve")
        return False
    
    # Step 2: Pull the MythoMax model
    print("\n📦 Step 2: Downloading MythoMax model...")
    print("⚠️ This will download ~8GB and may take 10-30 minutes depending on your internet speed")
    
    if not run_command("ollama pull mythomax-l2-13b", "Downloading MythoMax L2 13B"):
        print("❌ Failed to download MythoMax model")
        return False
    
    # Step 3: Verify the model is available
    print("\n✅ Step 3: Verifying model installation...")
    if run_command("ollama list", "Listing models"):
        print("\n🎉 MythoMax L2 13B setup completed successfully!")
        print("📋 You can now use the model with:")
        print("   ollama run mythomax-l2-13b")
        print("   or in your AI app with model name: 'mythomax-l2-13b'")
        return True
    else:
        print("❌ Model verification failed")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎯 Next steps:")
        print("1. Update your AI app to use 'mythomax-l2-13b' as the model")
        print("2. Run: python local_gguf_ai_app.py")
        print("3. Test with: 'who created you?' and other questions")
    else:
        print("\n💡 Troubleshooting:")
        print("1. Make sure Ollama is running: ollama serve")
        print("2. Check your internet connection")
        print("3. Try again: python setup_mythomax.py")
    
    input("\nPress Enter to continue...") 