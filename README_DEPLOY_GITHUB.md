# Deploy to GitHub (CLI)

Follow these steps to push your current project to GitHub using GitHub CLI and git.

## 1) Create .gitignore (recommended)
Create a `.gitignore` at project root with common ignores for Django projects:

```
# Python
__pycache__/
*.py[cod]
*.egg-info/
.eggs/

# Django
*.sqlite3
*.db
/media/
/staticfiles/
/staticfiles.json

# Virtual env
venv/
.env
.env.*

# OS / IDE
.DS_Store
Thumbs.db
.vscode/
.idea/

# Cache
.cache/
.mypy_cache/
.pytest_cache/

# Build
/dist/
/build/

# Local settings
local_settings.py
```

## 2) Initialize git and push to your repo
Run these commands from the project root (PowerShell):

```
# If not initialized yet
git init

# Add all tracked files
git add .

# First commit
git commit -m "Initial commit: BookMySeat with EmailJS confirmations"

# Add remote (replace if needed)
 git remote add origin https://github.com/Xcaptainind/book-ur-seat.git
# or using SSH if configured:
# git remote add origin git@github.com:Xcaptainind/book-ur-seat.git

# Push main branch
git branch -M main
git push -u origin main
```

## 3) Using GitHub CLI (optional)
If you want to create the repo from CLI (and not pre-create on GitHub):

```
# Authenticate once if needed
gh auth login

# Create repo under your account (private by default: add -p to keep private)
gh repo create Xcaptainind/book-ur-seat --public --source=. --remote=origin --push
```

## 4) Verify
- Open the repo URL: https://github.com/Xcaptainind/book-ur-seat
- Check that no large/sensitive files (e.g., venv, media, db.sqlite3) were uploaded.

## 5) Next steps for deployment
- If deploying to Vercel/Render: connect the repo and set environment variables as needed.
- For static files on production: run `collectstatic` during deploy and serve via WhiteNoise or CDN.
- For EmailJS: no server secrets needed; ensure the EmailJS Public Key is set for client-side.
