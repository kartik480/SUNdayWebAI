#!/usr/bin/env python3
"""
Test script for internet research functionality
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the research function
from app import research_internet

def test_research():
    """Test the research functionality"""
    print("🧪 Testing Internet Research Functionality...")
    print("=" * 50)
    
    # Test cases
    test_queries = [
        "when is ganesh chaturthi",
        "ganesh chaturthi 2025",
        "diwali date 2025",
        "holi festival 2025"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Testing: '{query}'")
        print("-" * 30)
        
        try:
            result = research_internet(query)
            print("✅ Research completed successfully!")
            print("📋 Result preview:")
            print(result[:300] + "..." if len(result) > 300 else result)
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("\n" + "=" * 50)

if __name__ == "__main__":
    test_research() 