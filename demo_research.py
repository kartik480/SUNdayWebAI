#!/usr/bin/env python3
"""
Demonstration of SUNDAY-PAAI's Internet Research Capability
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the research function
from app import research_internet

def demo_research():
    """Demonstrate the research functionality"""
    print("🎯 SUNDAY-PAAI Internet Research Demo")
    print("=" * 60)
    print("This demo shows how SUNDAY-PAAI can research information")
    print("from the internet and provide direct answers in chat!")
    print("=" * 60)
    
    # Demo the specific query from the user
    query = "when is ganesh chaturthi"
    
    print(f"\n🔍 Researching: '{query}'")
    print("⏳ Please wait while I search the internet...")
    print("-" * 60)
    
    try:
        result = research_internet(query)
        print("✅ Research completed!")
        print("\n📋 Full Research Results:")
        print("=" * 60)
        print(result)
        print("=" * 60)
        
        print("\n🎉 How it works:")
        print("1. SUNDAY-PAAI detects research requests automatically")
        print("2. Searches multiple sources on the internet")
        print("3. Extracts relevant information and dates")
        print("4. Provides a comprehensive summary in chat")
        print("5. Opens a web search for additional details")
        
        print("\n💡 Try these research queries in your chat:")
        print("• 'when is ganesh chaturthi'")
        print("• 'diwali date 2025'")
        print("• 'holi festival 2025'")
        print("• 'ramadan 2025'")
        
    except Exception as e:
        print(f"❌ Error during research: {e}")
        print("This might be due to network issues or website changes.")

if __name__ == "__main__":
    demo_research() 