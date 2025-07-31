from huggingface_hub import hf_hub_download
import os

def download_model():
    """Download the MythoMax model"""
    print("🚀 Starting MythoMax model download...")
    print("📦 Model: TheBloke/MythoMax-L2-13B-GGUF")
    print("📁 File: mythomax-l2-13b.q4_K_M.gguf")
    print("⏳ This may take a while (file is ~8GB)...")
    
    try:
        # Download the model
        model_path = hf_hub_download(
            repo_id="TheBloke/MythoMax-L2-13B-GGUF",
            filename="mythomax-l2-13b.q4_K_M.gguf",
            local_dir=".",
            local_dir_use_symlinks=False
        )
        
        print(f"✅ Model downloaded successfully!")
        print(f"📁 Location: {model_path}")
        print(f"📊 File size: {os.path.getsize(model_path) / (1024**3):.2f} GB")
        
        return model_path
        
    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        return None

if __name__ == "__main__":
    download_model() 