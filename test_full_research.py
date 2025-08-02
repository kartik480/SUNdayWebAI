#!/usr/bin/env python3
"""
Comprehensive test for full research functionality
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the functions
from app import get_ollama_response

def test_full_research():
    """Test the full research functionality end-to-end"""
    print("🧪 Testing Full Research Functionality...")
    print("=" * 60)
    
    # Test cases that should trigger research
    test_queries = [
        "when is dussera in 2025",
        "when is ganesh chaturthi",
        "diwali date 2025",
        "when is holi"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Testing: '{query}'")
        print("-" * 40)
        
        try:
            # This simulates what happens when user asks in chat
            response = get_ollama_response(query)
            
            print("✅ AI Response generated successfully!")
            print("📋 Response preview:")
            print(response[:400] + "..." if len(response) > 400 else response)
            
            # Check if it's a research response (not just opening browser)
            if "🔍 Research Results" in response or "Based on my knowledge" in response:
                print("✅ Research functionality working correctly!")
            elif "opened" in response.lower() and "browser" in response.lower():
                print("⚠️  Response only opens browser - research not triggered")
            else:
                print("ℹ️  Response type unclear")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "=" * 60)

if __name__ == "__main__":
    test_full_research() 