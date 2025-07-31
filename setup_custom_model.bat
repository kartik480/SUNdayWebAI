@echo off
echo 🚀 SUNDAY-PAAI Custom Model Setup
echo ================================================

echo.
echo 🔄 Checking Ollama installation...
ollama --version
if %errorlevel% neq 0 (
    echo ❌ Ollama is not installed. Please install it first from https://ollama.ai
    pause
    exit /b 1
)

echo.
echo 🔄 Pulling Llama 3.2 base model...
ollama pull llama3.2
if %errorlevel% neq 0 (
    echo ❌ Failed to pull Llama 3.2. Please check your internet connection.
    pause
    exit /b 1
)

echo.
echo 🔄 Creating Modelfile...
(
echo FROM llama3.2
echo SYSTEM You are a friendly assistant named SUNDAY-PAAI. You are helpful, creative, and always ready to assist users with any task or question. You have a warm personality and provide thoughtful, accurate responses.
) > Modelfile

echo ✅ Modelfile created successfully!

echo.
echo 🔄 Creating custom model kart_2003/sunday...
ollama create -f Modelfile kart_2003/sunday
if %errorlevel% neq 0 (
    echo ❌ Failed to create custom model.
    pause
    exit /b 1
)

echo.
echo 🔄 Listing available models...
ollama list

echo.
echo 🎉 Custom model setup completed successfully!
echo.
echo 📋 Next steps:
echo 1. Start Ollama: ollama serve
echo 2. Start SUNDAY-PAAI: python app.py
echo 3. Access your AI: http://localhost:8080
echo.
echo 🎯 Your custom model 'kart_2003/sunday' is now ready!
echo.
pause 