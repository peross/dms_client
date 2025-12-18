# Troubleshooting Guide

## Qt Platform Plugin Error (xcb)

If you encounter the error:
```
qt.qpa.plugin: Could not load the Qt platform plugin "xcb"
This application failed to start because no Qt platform plugin could be initialized.
```

**Solution:** Install the required system libraries. The Qt xcb plugin needs several xcb libraries:

```bash
sudo apt install libxcb-xinerama0 libxcb-cursor0 libxcb-icccm4 libxcb-keysyms1 libxcb-xkb1 libxkbcommon-x11-0
```

If you're still having issues, check for missing dependencies using:
```bash
ldd venv/lib/python3.13/site-packages/PyQt5/Qt5/plugins/platforms/libqxcb.so | grep "not found"
```

This will show which libraries are missing.

## Wayland vs X11

If you're using Wayland and encountering issues, you can:

1. Try running with Wayland explicitly:
```bash
export QT_QPA_PLATFORM=wayland
python main.py
```

2. Or force X11:
```bash
export QT_QPA_PLATFORM=xcb
python main.py
```

## Verify Qt Libraries

To check if Qt libraries are installed:
```bash
ldconfig -p | grep xcb
```

You should see libraries like:
- libxcb.so.1
- libxcb-xinerama.so.0
- libxcb-cursor.so.0

