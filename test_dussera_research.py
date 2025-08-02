#!/usr/bin/env python3
"""
Test script for Dussera research functionality
"""

import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the functions
from app import detect_action_request, research_internet

def test_dussera_research():
    """Test the Dussera research functionality"""
    print("🧪 Testing Dussera Research Functionality...")
    print("=" * 50)
    
    # Test cases
    test_queries = [
        "when is dussera in 2025",
        "dussera date 2025",
        "when is dussehra",
        "dussehra 2025",
        "navratri 2025"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Testing: '{query}'")
        print("-" * 30)
        
        # Test action detection
        action = detect_action_request(query)
        print(f"Action detected: {action}")
        
        if action and action.startswith('research:'):
            print("✅ Research action correctly detected!")
            
            # Test research function
            try:
                result = research_internet(query)
                print("✅ Research completed successfully!")
                print("📋 Result preview:")
                print(result[:300] + "..." if len(result) > 300 else result)
            except Exception as e:
                print(f"❌ Research error: {e}")
        else:
            print("❌ Research action NOT detected!")
        
        print("\n" + "=" * 50)

if __name__ == "__main__":
    test_dussera_research() 