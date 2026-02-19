# 🚀 PythonAnywhere Deployment Guide

Since FastAPI is an ASGI framework and PythonAnywhere primarily supports WSGI, we use the `a2wsgi` adapter to make it compatible.

## Step 1: Clone the Repository
Open a **Bash Console** on PythonAnywhere and run:
```bash
git clone https://github.com/Gauravsonawane3435/SQL-Query-Generator.git
cd SQL-Query-Generator
```

## Step 2: Create a Virtual Environment
In the same console:
```bash
mkvirtualenv --python=/usr/bin/python3.10 sqlgen-venv
pip install -r requirements.txt
```

## Step 3: Configure the Web App
1.  Go to the **Web** tab on PythonAnywhere.
2.  Click **Add a new web app**.
3.  Select **Manual Configuration** (do NOT select FastAPI).
4.  Choose **Python 3.10** (or higher).
5.  Set your paths:
    - **Source code:** `/home/YOUR_USERNAME/SQL-Query-Generator`
    - **Working directory:** `/home/YOUR_USERNAME/SQL-Query-Generator`
    - **Virtualenv:** `/home/YOUR_USERNAME/.virtualenvs/sqlgen-venv`

## Step 4: Edit the WSGI Configuration File
In the **Web** tab, find the **WSGI configuration file** link and edit it. Replace the entire content with:

```python
import sys
import os

# Set search path for imports
path = '/home/YOUR_USERNAME/SQL-Query-Generator'
if path not in sys.path:
    sys.path.append(path)

# Set environment variable for Gemini
os.environ['GOOGLE_API_KEY'] = 'YOUR_ACTUAL_API_KEY_HERE'

# Import the WSGI-wrapped FastAPI app
from main import wsgi_app as application
```
*(Replace `YOUR_USERNAME` and `YOUR_ACTUAL_API_KEY_HERE` with your actual info)*

## Step 5: Static Files (CRITICAL)
PythonAnywhere doesn't serve the `static` folder automatically in manual mode. 
1.  In the **Web** tab, scroll down to **Static files**.
2.  Add a new entry:
    - **URL:** `/`
    - **Directory:** `/home/YOUR_USERNAME/SQL-Query-Generator/static`

## Step 6: Reload
Click the **Reload** button at the top of the Web tab. Your app should now be live!
