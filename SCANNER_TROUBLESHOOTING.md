# Scanner Troubleshooting Guide

## Known Issues with pyinsane2

### AssertionError when accessing scanned images

If you encounter an error message like "Scan completed but no image data was received" or AssertionError when scanning, this is a known issue with pyinsane2's daemon communication layer. The scan completes successfully, but retrieving the image data fails.

### Workarounds

1. **Use scanimage command line tool directly:**
   ```bash
   scanimage --format=png --resolution 300 --mode Color > scan_output.png
   ```

2. **Use the scanner's native software:**
   - Brother provides official scanning software for Linux
   - Download from Brother's website for your scanner model

3. **Try alternative Python libraries:**
   - `python-sane` (older library, may have better compatibility)
   - `sane-py` (alternative SANE binding)

4. **Physical troubleshooting:**
   - Unplug and replug the USB cable
   - Power cycle the scanner
   - Ensure no other application is using the scanner
   - Check scanner drivers are up to date

### "Data is invalid" Error

If you get a "Data is invalid (4)" error:

1. **Reset the scanner:**
   - Unplug USB cable
   - Wait 5 seconds
   - Plug back in
   - Power cycle the scanner

2. **Close other applications:**
   - Make sure no other program is accessing the scanner
   - Check for background scanning processes

3. **Restart the application:**
   - Close the DMS Client
   - Restart it to reset scanner state

### Scanner Not Detected

If your scanner isn't detected:

1. **Check SANE detection:**
   ```bash
   scanimage -L
   ```
   This should list your scanner. If not, check:
   - Scanner is powered on
   - USB cable is connected
   - SANE drivers are installed: `sudo apt install sane sane-utils`

2. **Check permissions:**
   - You may need to add your user to the scanner group:
     ```bash
     sudo usermod -a -G scanner $USER
     ```
   - Log out and back in for changes to take effect

3. **Check Brother-specific drivers:**
   - Brother scanners may need specific drivers
   - Visit Brother support website for your model
   - Install `brscan4` or similar for your scanner series

### Alternative: Using scanimage directly

You can use the command-line `scanimage` tool as a workaround:

```bash
# List scanners
scanimage -L

# Scan with options
scanimage --format=png --resolution 300 --mode Color --output-file scan.png

# For your Brother DS-640 specifically
scanimage --device-name="brother5:bus1;dev3" --format=png --resolution 300 > scan.png
```

Then you can import the scanned file into the DMS Client manually.

