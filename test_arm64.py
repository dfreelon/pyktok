#!/usr/bin/env python3
"""
Test script for ARM64 compatibility of pyktok
"""

import sys
import platform

def test_imports():
    """Test if all required modules can be imported without SIGILL errors"""
    print("Testing ARM64-compatible imports...")
    
    try:
        import browser_cookie3
        print("✓ browser_cookie3 imported successfully")
    except Exception as e:
        print(f"✗ browser_cookie3 failed: {e}")
        return False
    
    try:
        from bs4 import BeautifulSoup
        print("✓ BeautifulSoup imported successfully")
    except Exception as e:
        print(f"✗ BeautifulSoup failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✓ numpy imported successfully")
    except Exception as e:
        print(f"✗ numpy failed: {e}")
        return False
    
    try:
        import pandas as pd
        print("✓ pandas imported successfully")
    except Exception as e:
        print(f"✗ pandas failed: {e}")
        return False
    
    try:
        import requests
        print("✓ requests imported successfully")
    except Exception as e:
        print(f"✗ requests failed: {e}")
        return False
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        print("✓ selenium imported successfully")
    except Exception as e:
        print(f"✗ selenium failed: {e}")
        return False
    
    try:
        from webdriver_manager.chrome import ChromeDriverManager
        print("✓ webdriver-manager imported successfully")
    except Exception as e:
        print(f"✗ webdriver-manager failed: {e}")
        return False
    
    return True

def test_arm64_module():
    """Test if the ARM64-compatible pyktok module can be imported"""
    print("\nTesting ARM64 pyktok module...")
    
    try:
        from pyktok import pyktok_arm64 as pyktok
        print("✓ pyktok_arm64 imported successfully")
        
        # Test basic functionality
        print("Testing basic functions...")
        
        # Test specify_browser function
        try:
            pyktok.specify_browser('chrome')
            print("✓ specify_browser function works")
        except Exception as e:
            print(f"⚠ specify_browser failed (expected if Chrome not installed): {e}")
        
        # Test deduplicate_metadata function
        try:
            import pandas as pd
            test_df = pd.DataFrame({'video_id': ['test1', 'test2']})
            result = pyktok.deduplicate_metadata('nonexistent.csv', test_df)
            print("✓ deduplicate_metadata function works")
        except Exception as e:
            print(f"✗ deduplicate_metadata failed: {e}")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ pyktok_arm64 import failed: {e}")
        return False

def test_system_info():
    """Display system information"""
    print("System Information:")
    print(f"Platform: {platform.platform()}")
    print(f"Architecture: {platform.architecture()}")
    print(f"Machine: {platform.machine()}")
    print(f"Processor: {platform.processor()}")
    print(f"Python version: {sys.version}")

def main():
    """Main test function"""
    print("=" * 50)
    print("pyktok ARM64 Compatibility Test")
    print("=" * 50)
    
    test_system_info()
    print()
    
    # Test imports
    if not test_imports():
        print("\n❌ Basic imports failed - check dependencies")
        return False
    
    # Test ARM64 module
    if not test_arm64_module():
        print("\n❌ ARM64 module test failed")
        return False
    
    print("\n✅ All tests passed! pyktok ARM64 version is working correctly.")
    print("\nTo use pyktok on ARM64:")
    print("1. from pyktok import pyktok_arm64 as pyktok")
    print("2. pyktok.specify_browser('chrome')")
    print("3. pyktok.save_tiktok('https://www.tiktok.com/@username/video/1234567890')")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
