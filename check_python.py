import sys
import subprocess

print("🔍 Checking Python Environment...")
print(f"Python executable: {sys.executable}")
print(f"Python version: {sys.version}")

print("\n📦 Installing Flask...")

try:
    # Try to install Flask
    cmd = [sys.executable, "-m", "pip", "install", "flask", "requests"]
    print(f"Running: {' '.join(cmd)}")
    
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    
    if result.returncode == 0:
        print("✅ Installation successful!")
        if result.stdout:
            print("Output:", result.stdout[:200] + "..." if len(result.stdout) > 200 else result.stdout)
    else:
        print("❌ Installation failed!")
        if result.stderr:
            print("Error:", result.stderr)
            
except subprocess.TimeoutExpired:
    print("⏰ Installation timed out")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n🧪 Testing Flask...")

try:
    import flask
    print("✅ Flask imported successfully!")
    
    from flask import Flask
    app = Flask(__name__)
    print("✅ Flask app created successfully!")
    
    print("🎉 Flask is working!")
    
except ImportError as e:
    print(f"❌ Flask import error: {e}")
except Exception as e:
    print(f"❌ Other error: {e}")

print("\n✅ Check complete!") 