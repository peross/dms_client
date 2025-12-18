# How to Update the Application

## Quick Update (Code Changes Only)

If you've received updated code files (like updated `.py` files), you typically don't need to run setup again. Just:

1. **Close the application** if it's currently running

2. **Run the application again** using one of these methods:
   ```bash
   ./run_app.sh
   ```
   Or double-click the desktop launcher

That's it! The application will use the new code automatically.

## Full Update (If Dependencies Changed)

If the `requirements.txt` file was updated or you want to ensure everything is up-to-date:

1. **Close the application** if it's currently running

2. **Navigate to the application directory**:
   ```bash
   cd /path/to/dms_client
   ```

3. **Re-run the setup script**:
   ```bash
   ./setup.sh
   ```

   The setup script is smart - it will:
   - Skip installing packages that are already installed
   - Only update what's needed
   - Re-create the desktop launcher if needed

4. **Run the application**:
   ```bash
   ./run_app.sh
   ```
   Or use the desktop launcher

## Update After Code Changes (Git Repository)

If you're using git and pulling updates:

1. **Close the application**

2. **Pull the latest changes**:
   ```bash
   cd /path/to/dms_client
   git pull
   ```

3. **If requirements.txt changed**, update dependencies:
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt --upgrade
   ```

4. **Run the application**:
   ```bash
   ./run_app.sh
   ```

## Verify Update

To verify you're running the updated version, you can check:
- The application behavior (new features should be visible)
- Check the console output when starting the app
- Look at file modification dates: `ls -l *.py`

## Troubleshooting

If the application doesn't work after an update:

1. **Re-run the full setup**:
   ```bash
   ./setup.sh
   ```

2. **If that doesn't work, try reinstalling dependencies**:
   ```bash
   source venv/bin/activate
   pip install -r requirements.txt --force-reinstall
   ```

3. **Check for errors** when running:
   ```bash
   ./run_app.sh
   ```

