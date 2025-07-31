print("Testing Flask import...")

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