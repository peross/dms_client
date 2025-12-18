#!/usr/bin/env python3
"""Test script to diagnose scanner detection issues."""

print("Testing scanner detection...")
print("=" * 50)

# Test 1: Check SANE directly
print("\n1. Testing SANE command line...")
import subprocess
try:
    result = subprocess.run(['scanimage', '-L'], capture_output=True, text=True, timeout=5)
    print("SANE output:")
    print(result.stdout)
    if result.stderr:
        print("SANE errors:")
        print(result.stderr)
except FileNotFoundError:
    print("ERROR: scanimage command not found. Install SANE: sudo apt install sane-utils")
except Exception as e:
    print(f"ERROR running scanimage: {e}")

# Test 2: Check pyinsane2
print("\n2. Testing pyinsane2...")
try:
    import pyinsane2
    print("pyinsane2 imported successfully")
    
    print("Initializing pyinsane2...")
    try:
        pyinsane2.init()
        print("pyinsane2 initialized")
    except Exception as e:
        print(f"Warning during init: {e}")
    
    print("Getting devices...")
    devices = pyinsane2.get_devices()
    print(f"Found {len(devices)} device(s)")
    
    if devices:
        for i, device in enumerate(devices):
            print(f"\nDevice {i}:")
            print(f"  Name: {device.name}")
            try:
                print(f"  Vendor: {getattr(device, 'vendor', 'N/A')}")
                print(f"  Model: {getattr(device, 'model', 'N/A')}")
            except:
                pass
    else:
        print("No devices found by pyinsane2")
        print("Trying with force_reload=True...")
        try:
            devices = pyinsane2.get_devices(force_reload=True)
            print(f"Found {len(devices)} device(s) with force_reload")
        except Exception as e:
            print(f"Error with force_reload: {e}")
    
    pyinsane2.exit()
    
except ImportError as e:
    print(f"ERROR: pyinsane2 not installed: {e}")
    print("Install with: pip install pyinsane2")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
print("Test complete.")

