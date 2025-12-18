# How to Download and Install from GitHub (Simple Guide)

This is a simple, step-by-step guide for Windows users who want to download and install the Document Management Client from GitHub.

## Step 1: Go to GitHub Releases

1. Open your web browser (Chrome, Firefox, Edge, etc.)
2. Go to: `https://github.com/YOUR_USERNAME/dms_client/releases`
   - **Replace `YOUR_USERNAME` with the actual GitHub username**
   - For example, if the username is `johnsmith`, the URL would be: `https://github.com/johnsmith/dms_client/releases`

## Step 2: Find the Latest Release

1. You'll see a list of releases (versions of the application)
2. The latest release is usually at the top, marked with a "Latest" badge
3. Click on the release title (e.g., "v1.0.0") or scroll down to see the download files

## Step 3: Download the Installer

### For Windows Users:

1. Look for a file named `DocumentManagementClient-Setup.exe`
2. Click on the filename to download it
3. The file will start downloading (you'll see it in your browser's download bar)
4. Wait for the download to complete (the file is ~100-200MB, so it may take a few minutes depending on your internet speed)

**Where did it download?**
- Usually goes to your **Downloads** folder
- You can see the download location in your browser
- Or check: `C:\Users\YourName\Downloads\`

## Step 4: Install the Application

1. **Find the downloaded file:**
   - Open File Explorer
   - Go to your Downloads folder
   - Look for `DocumentManagementClient-Setup.exe`

2. **Windows Security Warning:**
   - When you double-click the file, Windows might show a security warning
   - This is normal - the app isn't code-signed yet
   - Click **"More info"** then click **"Run anyway"**

3. **Run the installer:**
   - Double-click `DocumentManagementClient-Setup.exe`
   - A window will appear asking for permission - click **"Yes"**
   - The installer wizard will open

4. **Follow the installation wizard:**
   - Click **"Next"** through the welcome screen
   - Choose where to install (default is fine: `C:\Program Files\Document Management Client`)
   - Select if you want a Desktop shortcut (recommended: check the box)
   - Click **"Install"**
   - Wait for installation to complete (usually takes 30 seconds to 1 minute)
   - Click **"Finish"**

## Step 5: Run the Application

1. **Method 1: Desktop shortcut**
   - Look on your desktop for "Document Management Client"
   - Double-click it

2. **Method 2: Start Menu**
   - Click the Windows Start button (bottom left)
   - Type "Document Management Client"
   - Click on the application when it appears

3. **Method 3: From installation folder**
   - Go to: `C:\Program Files\Document Management Client`
   - Double-click `DocumentManagementClient.exe`

## First Time Setup

When you first run the application:

1. A dialog will ask you to select a folder to track
2. Click **"Browse"** and choose a folder where you want to manage documents
   - For example: `C:\Users\YourName\Documents\MyDocuments`
3. Click **"Select"**
4. The app will create three default folders:
   - General
   - My Folders
   - Shared With Me
5. You're ready to use the app!

## Troubleshooting

### "Windows protected your PC" warning

**What it means:** Windows is warning that the app isn't from a known publisher.

**What to do:**
1. Click **"More info"**
2. Click **"Run anyway"**
3. The app is safe - it's just not code-signed

### Can't find the download

**Check these places:**
- Downloads folder: `C:\Users\YourName\Downloads\`
- Check your browser's download history
- Try downloading again

### Installation fails

**Try these:**
1. Make sure you have administrator rights (right-click → "Run as administrator")
2. Check you have enough disk space (need ~200MB free)
3. Temporarily disable antivirus software and try again
4. Download the file again in case it was corrupted

### App won't start

**Try these:**
1. Make sure installation completed successfully
2. Try running from the installation folder: `C:\Program Files\Document Management Client\DocumentManagementClient.exe`
3. Check Windows Event Viewer for error messages
4. Reinstall the application

## Uninstalling

If you want to remove the application:

1. Open **Settings** (Windows key + I)
2. Go to **Apps** → **Apps & features**
3. Search for "Document Management Client"
4. Click on it
5. Click **"Uninstall"**
6. Follow the prompts

## Getting Help

If you have problems:

1. Check the [INSTALLER_GUIDE.md](INSTALLER_GUIDE.md) for more detailed instructions
2. Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for common issues
3. Open an issue on GitHub describing your problem

## Quick Summary

1. ✅ Go to GitHub releases page
2. ✅ Download `DocumentManagementClient-Setup.exe`
3. ✅ Run the installer
4. ✅ Click through the installation wizard
5. ✅ Launch from Desktop or Start Menu
6. ✅ Select a folder to track
7. ✅ Start using the app!

That's it! The whole process takes about 5 minutes.

