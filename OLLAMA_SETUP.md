# 🤖 SUNDAY-PAAI Ollama Integration Guide

## 🚀 Quick Start

### 1. Install Ollama
Visit [https://ollama.ai](https://ollama.ai) and download Ollama for your operating system.

**Windows:**
```bash
# Download from https://ollama.ai/download
# Run the installer
```

**macOS:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### 2. Start Ollama
```bash
ollama serve
```

### 3. Download a Model
```bash
# Download Llama 2 (recommended for SUNDAY-PAAI)
ollama pull llama2

# Or try other models:
ollama pull mistral
ollama pull codellama
ollama pull llama2:7b
ollama pull llama2:13b
```

### 4. Install Python Dependencies
```bash
pip install -r requirements.txt
```

### 5. Start SUNDAY-PAAI
```bash
python app.py
```

### 6. Access Your AI Assistant
Open your browser and go to: `http://localhost:8080`

## 🧠 Available Models

### Recommended Models for SUNDAY-PAAI:

| Model | Size | Speed | Quality | Use Case |
|-------|------|-------|---------|----------|
| `llama2` | 7B | Fast | Good | General purpose |
| `llama2:13b` | 13B | Medium | Better | Enhanced responses |
| `mistral` | 7B | Fast | Excellent | Creative tasks |
| `codellama` | 7B | Fast | Good | Programming help |
| `llama2:7b` | 7B | Fast | Good | Lightweight option |

### Download Additional Models:
```bash
# Creative writing
ollama pull mistral

# Programming assistance
ollama pull codellama

# Large model for better quality
ollama pull llama2:13b

# Specialized models
ollama pull llama2:7b-chat
ollama pull llama2:13b-chat
```

## ⚙️ Configuration

### Change Default Model
Edit `app.py` and modify the `DEFAULT_MODEL` variable:
```python
DEFAULT_MODEL = "mistral"  # Change to your preferred model
```

### Ollama API Configuration
The default Ollama API URL is `http://localhost:11434`. If you're running Ollama on a different port or host, update the `OLLAMA_BASE_URL` in `app.py`:
```python
OLLAMA_BASE_URL = "http://your-host:your-port"
```

## 🔧 Troubleshooting

### Ollama Not Running
```bash
# Check if Ollama is running
ollama list

# Start Ollama if not running
ollama serve
```

### Model Not Found
```bash
# List available models
ollama list

# Pull the model if not available
ollama pull llama2
```

### Connection Issues
1. **Check Ollama Status:**
   ```bash
   curl http://localhost:11434/api/tags
   ```

2. **Verify Port:**
   - Ollama runs on port 11434 by default
   - SUNDAY-PAAI runs on port 8080 by default

3. **Firewall Issues:**
   - Allow Ollama through your firewall
   - Check if antivirus is blocking the connection

### Performance Issues
1. **Use Smaller Models:**
   ```bash
   ollama pull llama2:7b  # Faster, less memory
   ```

2. **Check System Resources:**
   - Ensure you have enough RAM (8GB+ recommended)
   - Use SSD for better performance

3. **GPU Acceleration:**
   - Install CUDA for NVIDIA GPUs
   - Install ROCm for AMD GPUs

## 🎯 Features

### ✅ What Works:
- ✅ Real AI responses from Ollama
- ✅ Model switching via UI
- ✅ Status monitoring
- ✅ Quick actions
- ✅ Chat interface
- ✅ Error handling

### 🔄 Real-time Features:
- Live AI status monitoring
- Model availability checking
- Response time tracking
- Connection health monitoring

## 📱 Usage Tips

### Best Practices:
1. **Start with Llama 2:** It's well-balanced for general use
2. **Use Mistral for Creativity:** Better for creative writing and brainstorming
3. **Use Code Llama for Programming:** Specialized for code generation
4. **Monitor Resources:** Larger models use more memory and CPU

### Quick Commands:
```bash
# Check Ollama status
ollama list

# Test a model
ollama run llama2 "Hello, how are you?"

# Stop Ollama
pkill ollama

# Restart Ollama
ollama serve
```

## 🔒 Security Notes

- Ollama runs locally on your machine
- No data is sent to external servers
- All conversations are private
- Models are downloaded and stored locally

## 🆘 Support

### Common Issues:

1. **"Ollama not detected"**
   - Make sure Ollama is running: `ollama serve`
   - Check if port 11434 is accessible

2. **"Model not available"**
   - Download the model: `ollama pull llama2`
   - Check available models: `ollama list`

3. **Slow responses**
   - Use smaller models
   - Check system resources
   - Consider GPU acceleration

4. **Connection timeout**
   - Restart Ollama: `pkill ollama && ollama serve`
   - Check firewall settings
   - Verify network connectivity

### Getting Help:
- Ollama Documentation: https://ollama.ai/docs
- SUNDAY-PAAI Issues: Check the project repository
- Community Support: Ollama Discord/Reddit

## 🎉 Enjoy Your AI Assistant!

Your SUNDAY-PAAI is now powered by real AI! Ask it anything and watch it respond with intelligence and creativity. 🚀✨ 