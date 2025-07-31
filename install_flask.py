import subprocess
import sys

print("Installing Flask...")

try:
    # Install Flask using subprocess
    result = subprocess.run([sys.executable, "-m", "pip", "install", "flask", "requests"], 
                          capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Flask installed successfully!")
        print("Output:", result.stdout)
    else:
        print("❌ Flask installation failed!")
        print("Error:", result.stderr)
        
except Exception as e:
    print(f"❌ Installation error: {e}")

print("\nTesting Flask import...")

try:
    import flask
    print("✅ Flask imported successfully!")
    
    from flask import Flask
    app = Flask(__name__)
    print("✅ Flask app created successfully!")
    
    print("✅ Flask is working properly!")
    
except ImportError as e:
    print(f"❌ Flask import error: {e}")
except Exception as e:
    print(f"❌ Other error: {e}")

print("Test complete!") 