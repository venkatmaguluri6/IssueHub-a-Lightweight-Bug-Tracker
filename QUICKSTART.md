# Quick Start Guide

## Backend Setup

1. **Activate virtual environment**
   ```bash
   # Windows (PowerShell)
   # If you get execution policy error, run first:
   # Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   .\venv\Scripts\activate
   
   # Windows (CMD/Command Prompt)
   venv\Scripts\activate.bat
   
   # Windows (Git Bash)
   source venv/Scripts/activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

2. **Run migrations**
   ```bash
   python manage.py migrate
   ```

3. **Seed demo data** (optional)
   ```bash
   python manage.py shell
   >>> exec(open('seed_data.py').read())
   >>> exit()
   ```

4. **Start server**
   ```bash
   python manage.py runserver
   ```
   Backend runs on `http://localhost:8000`

## Frontend Setup

1. **Install dependencies** (first time only)
   ```bash
   cd frontend
   npm install
   ```

2. **Start dev server**
   ```bash
   npm run dev
   ```
   Frontend runs on `http://localhost:5173`
   
   **Note**: Keep this terminal running! Changes to code will automatically appear in the browser (Hot Module Replacement).

## Test the Application

1. Open `http://localhost:5173` in your browser
2. Sign up with a new account or use demo credentials:
   - Email: `user1@example.com`
   - Password: `password123`
3. Create a project
4. Add issues and start tracking!

## Running Tests

```bash
# Backend tests
python manage.py test

# Run specific test suite
python manage.py test users
python manage.py test projects
python manage.py test issues
```

## Common Issues

**Backend won't start:**
- Make sure virtual environment is activated
- Run `python manage.py migrate` if you see migration errors

**Frontend can't connect to backend:**
- Verify backend is running on port 8000
- Check CORS settings in `issuehub_backend/settings.py`

**Can't login:**
- Make sure you've run migrations
- Try creating a new account via signup

**Frontend changes not appearing:**
- Make sure dev server is running (`npm run dev`)
- Save the file (Ctrl+S / Cmd+S)
- Hard refresh browser: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)
- Check terminal for compilation errors
- Restart dev server if needed (Ctrl+C, then `npm run dev`)

**"npm: command not found" or "node: command not found":**
- **Node.js is not installed**: Download and install from [nodejs.org](https://nodejs.org/)
  - Choose the LTS (Long Term Support) version
  - Make sure to check "Add to PATH" during installation
- **After installation**: 
  - Close and reopen your terminal (Git Bash/PowerShell/CMD)
  - Verify installation: `node --version` and `npm --version`
- **If still not working in Git Bash**:
  - Try using PowerShell or CMD instead
  - Or add Node.js to Git Bash PATH manually
- **Alternative**: Use Windows Command Prompt or PowerShell for frontend commands

