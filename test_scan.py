#!/usr/bin/env python3
"""Test script to diagnose scanning issues."""

print("Testing scanner scan functionality...")
print("=" * 50)

try:
    import pyinsane2
    print("1. Initializing pyinsane2...")
    pyinsane2.init()
    
    print("2. Getting devices...")
    devices = pyinsane2.get_devices()
    
    if not devices:
        print("ERROR: No devices found")
        pyinsane2.exit()
        exit(1)
    
    print(f"Found {len(devices)} device(s)")
    scanner = devices[0]
    print(f"Using scanner: {scanner.name}")
    print(f"  Vendor: {getattr(scanner, 'vendor', 'N/A')}")
    print(f"  Model: {getattr(scanner, 'model', 'N/A')}")
    
    print("\n3. Checking scanner options...")
    try:
        print(f"Available options: {list(scanner.options.keys())[:10]}...")  # First 10
        if 'resolution' in scanner.options:
            print(f"Resolution constraint: {scanner.options['resolution'].constraint}")
        if 'mode' in scanner.options:
            print(f"Mode constraint: {scanner.options['mode'].constraint}")
    except Exception as e:
        print(f"Error checking options: {e}")
    
    print("\n4. Attempting to configure scanner...")
    try:
        if 'resolution' in scanner.options:
            scanner.options['resolution'].value = 300
            print("Set resolution to 300 DPI")
        if 'mode' in scanner.options:
            if 'color' in scanner.options['mode'].constraint:
                scanner.options['mode'].value = 'color'
                print("Set mode to color")
    except Exception as e:
        print(f"Warning configuring scanner: {e}")
    
    print("\n5. Starting scan...")
    try:
        scan_session = scanner.scan(multiple=False)
        print("Scan session created")
        
        print("6. Reading scan data...")
        try:
            while True:
                scan_session.scan.read()
                print("Reading...", end='', flush=True)
        except EOFError:
            print("\nEOF reached")
        
        print("\n7. Getting images...")
        if scan_session.images:
            image = scan_session.images[0]
            print(f"Got image: {type(image)}, size: {getattr(image, 'size', 'N/A')}")
            print("Scan successful!")
        else:
            print("ERROR: No images in scan session")
            
    except Exception as e:
        print(f"\nERROR during scan: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n8. Cleaning up...")
    pyinsane2.exit()
    
except ImportError:
    print("ERROR: pyinsane2 not installed")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 50)
print("Test complete.")

