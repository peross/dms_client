# Building Windows Installers from Linux

Since you're developing on Linux but need to create Windows `.exe` installers, here are your options:

## Option 1: GitHub Actions (Recommended) ⭐

**Best for:** Automated builds, no local setup needed

GitHub Actions will build Windows installers automatically in the cloud. This is the easiest and most reliable method.

**Note:** If you get billing errors, see [ALTERNATIVE_BUILD_OPTIONS.md](ALTERNATIVE_BUILD_OPTIONS.md) for solutions. GitHub Actions is free for public repositories, but you may need to add a payment method to your account.

### How to Use

1. **Push your code to GitHub** (if not already done)

2. **Create a release tag** (or use manual trigger):
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```
   This will automatically trigger the build workflow.

   **OR** manually trigger:
   - Go to your GitHub repository
   - Click "Actions" tab
   - Select "Build Installers (Manual)"
   - Click "Run workflow"

3. **Download the built installer**:
   - Go to the "Actions" tab
   - Click on the completed workflow run
   - Download the "windows-build" artifact
   - Extract the ZIP file to get `DocumentManagementClient-Setup.exe`

### Workflow Files

The repository includes two GitHub Actions workflows:
- `.github/workflows/build-release.yml` - Builds on tag releases
- `.github/workflows/build-on-demand.yml` - Manual trigger (use this for testing)

## Option 1b: Fix GitHub Actions Billing

If you're getting billing errors:

1. Go to GitHub Settings → Billing
2. Add a payment method (even if you won't be charged for public repos)
3. GitHub Actions is **free for public repositories** (2000 minutes/month)
4. After adding payment method, workflows will work again

**See [ALTERNATIVE_BUILD_OPTIONS.md](ALTERNATIVE_BUILD_OPTIONS.md) for detailed alternatives.**

## Option 2: Wine (Build Locally) ⚡

**Quick Start:** Use the provided script: `./build_windows_wine.sh`

**Best for:** Quick local builds without cloud services

Wine allows you to run Windows executables on Linux. You can use it to run PyInstaller and create Windows executables.

### Quick Build Script

We've included a script to make this easier:

```bash
# Install Wine first (if not installed)
sudo apt-get install wine

# Install Python in Wine (one time setup)
wget https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe
wine python-3.10.11-amd64.exe
# Make sure to check "Add Python to PATH" during installation

# Build the executable
./build_windows_wine.sh
```

This will create `dist/DocumentManagementClient.exe` - a standalone executable that users can run directly.

### Setup

```bash
# Install Wine (Ubuntu/Debian)
sudo apt-get install wine wine64 wine32

# Install Python in Wine
wget https://www.python.org/ftp/python/3.10.11/python-3.10.11-amd64.exe
wine python-3.10.11-amd64.exe

# Install PyInstaller in Wine Python
wine python.exe -m pip install PyInstaller Pillow
```

### Build

```bash
# Convert paths for Wine
WINEPREFIX=~/.wine wine python.exe -m PyInstaller dms_client.spec
```

**Note:** This can be tricky and may have compatibility issues. GitHub Actions is much more reliable.

## Option 3: Windows VM

**Best for:** Need exact Windows environment, have Windows license

If you have a Windows license, you can:
1. Set up a Windows VM (using VirtualBox, VMware, etc.)
2. Install Python and build tools in the VM
3. Copy your code to the VM
4. Run `build_windows.bat`

## Option 4: Dual Boot or Separate Windows Machine

If you have access to a Windows machine (or dual boot), you can:
1. Copy your project to Windows
2. Run the build scripts there
3. Copy the built installer back

## Recommended Workflow

**For development and releases:**

1. **Develop on Linux** (as you're doing now)
2. **Test Linux builds locally**: `./build_linux.sh`
3. **Push to GitHub**: `git push`
4. **Create a tag or trigger manual build** in GitHub Actions
5. **Download the Windows installer** from GitHub Actions artifacts
6. **Create a GitHub release** and upload both Windows and Linux installers

## Quick Start: Using GitHub Actions

### First Time Setup

1. Make sure your code is pushed to GitHub:
   ```bash
   git add .
   git commit -m "Add build workflows"
   git push
   ```

2. Go to GitHub repository → Actions tab

3. Manually trigger a build:
   - Click "Build Installers (Manual)"
   - Click "Run workflow"
   - Wait for build to complete (~5-10 minutes)

4. Download artifacts:
   - Click on the completed workflow
   - Download "windows-build-XXX" artifact
   - Extract to get your `.exe` file

### Creating a Release

1. Build installers (using GitHub Actions or manually)

2. Create a tag:
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0"
   git push origin v1.0.0
   ```
   This automatically triggers release build and creates a GitHub release.

3. Or manually create release:
   - Go to Releases → "Draft a new release"
   - Upload your built installers
   - Publish

## Troubleshooting GitHub Actions

**Build fails:**
- Check the Actions log for error messages
- Ensure all dependencies are in `requirements.txt`
- Verify `dms_client.spec` is correct

**Installer not created:**
- Check if Inno Setup download succeeded
- The workflow will still upload the standalone `.exe` if installer fails
- You can manually create installer later if needed

**Can't find artifacts:**
- Artifacts are available for 7-30 days (depending on workflow)
- Download them before they expire
- Store them in releases for permanent access

## File Sizes

Expect these sizes:
- Windows installer: ~100-200MB
- Windows executable: ~100-200MB
- Linux AppImage: ~100-200MB

These are normal - they include Python interpreter and all dependencies.

## Summary

**Recommended approach:** Use GitHub Actions (Option 1)
- ✅ No local setup needed
- ✅ Automated and reliable
- ✅ Builds on real Windows environment
- ✅ Free for public repositories
- ✅ Can trigger manually or automatically on tags

Just push your code, trigger the workflow, and download the built installer!

