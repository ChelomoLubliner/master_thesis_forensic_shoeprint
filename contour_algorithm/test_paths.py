#!/usr/bin/env python3
"""Test script to verify all path fixes are working"""

import sys
import os

print("=== Testing Path Fixes ===")

try:
    print("1. Testing globals import...")
    import globals
    print("   ✅ globals imported successfully")
    print(f"   ✅ DATA_PATH: {globals.DATA_PATH}")
    print(f"   ✅ SHARED_DATA_PATH: {globals.SHARED_DATA_PATH}")
    print(f"   ✅ PROCESSING_DATA_PATH: {globals.PROCESSING_DATA_PATH}")
    
    # Check if paths exist
    if os.path.exists(globals.DATA_PATH):
        print(f"   ✅ DATA_PATH exists")
    else:
        print(f"   ❌ DATA_PATH does not exist")
        
    if os.path.exists(globals.SHARED_DATA_PATH):
        print(f"   ✅ SHARED_DATA_PATH exists")
    else:
        print(f"   ❌ SHARED_DATA_PATH does not exist")
        
    if os.path.exists(globals.PROCESSING_DATA_PATH):
        print(f"   ✅ PROCESSING_DATA_PATH exists")
    else:
        print(f"   ❌ PROCESSING_DATA_PATH does not exist")

except Exception as e:
    print(f"   ❌ Error importing globals: {e}")

try:
    print("\n2. Testing distance_extremities import...")
    import distance_extremities
    print("   ✅ distance_extremities imported successfully")
    
except Exception as e:
    print(f"   ❌ Error importing distance_extremities: {e}")

try:
    print("\n3. Testing create_files_shoes import...")
    import create_files_shoes
    print("   ✅ create_files_shoes imported successfully")
    
except Exception as e:
    print(f"   ❌ Error importing create_files_shoes: {e}")

print("\n=== Path Fix Test Complete ===")
