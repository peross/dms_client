# Creating GitHub Releases

This guide explains how to create releases on GitHub so users can easily download and install the application.

## Overview

GitHub Releases allow you to package and distribute your application installers. Users can download pre-built installers without needing to build from source.

## Prerequisites

1. **Build the installers** (see [BUILD.md](BUILD.md))
   - Windows: `build_windows.bat` → `build/windows/build_installer.bat`
   - Linux: `./build_linux.sh`

2. **Have the installer files ready:**
   - `dist/DocumentManagementClient-Setup.exe` (Windows installer)
   - `dist/DocumentManagementClient-x86_64.AppImage` (Linux AppImage, optional)
   - `dist/DocumentManagementClient.exe` (Windows portable, optional)

## Step-by-Step: Creating a Release

### Step 1: Build the Installers

#### Windows
```cmd
cd dms_client
build_windows.bat
build\windows\build_installer.bat
```

This creates:
- `dist/DocumentManagementClient.exe` (standalone executable)
- `dist/DocumentManagementClient-Setup.exe` (installer - recommended for distribution)

#### Linux
```bash
cd dms_client
chmod +x build_linux.sh
./build_linux.sh
```

This creates:
- `dist/DocumentManagementClient` (standalone executable)
- `dist/DocumentManagementClient-x86_64.AppImage` (portable - recommended for distribution)

### Step 2: Create a Git Tag (Optional but Recommended)

Tagging releases helps with version management:

```bash
# Create and push a tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0
```

Or via GitHub web interface:
1. Go to your repository
2. Click "Releases" → "Draft a new release"
3. GitHub will prompt you to create a tag

### Step 3: Create the Release on GitHub

#### Via GitHub Web Interface (Recommended)

1. **Go to your repository on GitHub**

2. **Click "Releases"** (on the right sidebar, or go to `https://github.com/yourusername/dms_client/releases`)

3. **Click "Draft a new release"**

4. **Fill in the release information:**
   - **Tag version:** `v1.0.0` (or create a new tag)
   - **Release title:** `Document Management Client v1.0.0` or just `v1.0.0`
   - **Description:** Add release notes, for example:
     ```markdown
     ## What's New
     - Initial release
     - Windows installer support
     - Linux AppImage support
     - Scanner integration
     
     ## Installation
     - **Windows:** Download `DocumentManagementClient-Setup.exe` and run it
     - **Linux:** Download `DocumentManagementClient-x86_64.AppImage`, make it executable (`chmod +x`), and run it
     
     ## System Requirements
     - Windows 7 or later (Windows 10/11 recommended)
     - Linux: Any modern distribution
     - 200MB free disk space
     - 512MB RAM minimum
     ```

5. **Attach binaries:**
   - Click "Attach binaries by dropping them here or selecting them"
   - Upload:
     - `DocumentManagementClient-Setup.exe` (Windows installer)
     - `DocumentManagementClient-x86_64.AppImage` (Linux AppImage)
     - Optionally: `DocumentManagementClient.exe` (Windows portable version)

6. **Click "Publish release"**

### Step 4: Update README with Download Links

Update your README.md to point to the releases:

```markdown
## For End Users - Quick Install

### Windows
1. Go to [Releases](https://github.com/yourusername/dms_client/releases)
2. Download `DocumentManagementClient-Setup.exe` from the latest release
3. Run the installer and follow the setup wizard

### Linux
1. Go to [Releases](https://github.com/yourusername/dms_client/releases)
2. Download `DocumentManagementClient-x86_64.AppImage` from the latest release
3. Make it executable: `chmod +x DocumentManagementClient-x86_64.AppImage`
4. Run it: `./DocumentManagementClient-x86_64.AppImage`
```

## Alternative: Using GitHub CLI

If you prefer command-line:

```bash
# Install GitHub CLI first: https://cli.github.com/

# Create a release
gh release create v1.0.0 \
  --title "Document Management Client v1.0.0" \
  --notes "Initial release with Windows and Linux support" \
  dist/DocumentManagementClient-Setup.exe \
  dist/DocumentManagementClient-x86_64.AppImage
```

## File Naming Conventions

Recommended naming:
- `DocumentManagementClient-Setup-v1.0.0.exe` (Windows installer)
- `DocumentManagementClient-v1.0.0.exe` (Windows portable)
- `DocumentManagementClient-x86_64-v1.0.0.AppImage` (Linux AppImage)

However, keeping simple names like `DocumentManagementClient-Setup.exe` is also fine - users will see the version in the release notes.

## User Download Process

Once you've created a release, here's what users will see:

1. **Go to your repository:** `https://github.com/yourusername/dms_client`
2. **See the release:** They'll see "Latest" badge if you marked it as latest, or find it under "Releases"
3. **Download:** Click on the release to see download links for each file
4. **Install/Run:** Follow platform-specific installation steps

### What Users Will See

When users visit your releases page, they'll see:
- Release title and version
- Release notes/description
- Download links for each file (automatically shown with file size)
- Release date

## Best Practices

1. **Always test installers** on clean systems before releasing
2. **Write clear release notes** - describe what's new, fixed, or changed
3. **Use semantic versioning** (v1.0.0, v1.1.0, v2.0.0)
4. **Mark releases as "Latest"** for the most recent stable version
5. **Create pre-releases** for testing (beta/alpha versions)
6. **Keep older versions available** for users who can't upgrade yet

## Updating Releases

To update a release:
1. Go to the release page
2. Click "Edit release"
3. Add new files or update description
4. Save changes

Note: You can't replace files, but you can delete and re-upload them.

## Automating Releases (Advanced)

You can automate release creation using GitHub Actions. Create `.github/workflows/release.yml`:

```yaml
name: Build and Release

on:
  push:
    tags:
      - 'v*'

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: pip install -r build_requirements.txt -r requirements.txt
      - name: Build
        run: build_windows.bat
      - name: Create installer
        run: build\windows\build_installer.bat
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: windows-installer
          path: dist/DocumentManagementClient-Setup.exe

  build-linux:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          pip install -r build_requirements.txt -r requirements.txt
          wget https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage
          chmod +x appimagetool-x86_64.AppImage
          sudo mv appimagetool-x86_64.AppImage /usr/local/bin/appimagetool
      - name: Build
        run: ./build_linux.sh
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: linux-appimage
          path: dist/DocumentManagementClient-x86_64.AppImage

  create-release:
    needs: [build-windows, build-linux]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Download artifacts
        uses: actions/download-artifact@v3
      - name: Create Release
        uses: softprops/action-gh-release@v1
        with:
          files: |
            windows-installer/DocumentManagementClient-Setup.exe
            linux-appimage/DocumentManagementClient-x86_64.AppImage
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
```

## Troubleshooting

**File size limits:**
- GitHub allows up to 2GB per file
- Your installers should be ~100-200MB, well within limits

**Users can't download:**
- Ensure files are uploaded to the release (not just in the repository)
- Check file permissions are correct

**Release not showing:**
- Make sure you clicked "Publish release" (not just saved as draft)
- Check if you marked it as "Latest release"

