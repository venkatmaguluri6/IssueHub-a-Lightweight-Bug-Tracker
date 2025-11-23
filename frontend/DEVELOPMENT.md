# Frontend Development Guide

## Hot Module Replacement (HMR)

Vite automatically reloads changes in development mode. Most changes appear instantly without refreshing the browser.

## Development Workflow

### 1. Start Development Server

```bash
cd frontend
npm run dev
```

You should see:
```
VITE v5.x.x  ready in xxx ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
```

### 2. Make Changes

Edit any file in `src/`:
- `src/pages/*.jsx` - Page components
- `src/pages/*.css` - Page styles
- `src/App.jsx` - Main app component
- `src/utils/*.js` - Utility functions

### 3. Changes Appear Automatically

- **Component changes**: Update instantly (HMR)
- **CSS changes**: Update instantly
- **New files**: May need browser refresh
- **Config changes**: Need server restart

## When to Restart Dev Server

Restart is needed for:
- Changes to `vite.config.js`
- Changes to `package.json`
- Installing new dependencies (`npm install`)
- Environment variable changes (`.env` files)

**To restart:**
1. Press `Ctrl+C` in the terminal
2. Run `npm run dev` again

## Troubleshooting

### Changes Not Appearing?

1. **Check terminal for errors**
   - Look for compilation errors
   - Fix syntax errors first

2. **Hard refresh browser**
   - Windows/Linux: `Ctrl + Shift + R`
   - Mac: `Cmd + Shift + R`

3. **Clear browser cache**
   - Open DevTools (F12)
   - Right-click refresh button → "Empty Cache and Hard Reload"

4. **Check browser console**
   - Press F12
   - Look for JavaScript errors
   - Check Network tab for failed requests

5. **Restart dev server**
   ```bash
   # Stop server (Ctrl+C)
   npm run dev
   ```

### Common Issues

**"Module not found" errors:**
- File path might be wrong
- Check import statements
- Restart dev server

**Styling not updating:**
- Check if CSS file is imported
- Verify class names match
- Hard refresh browser

**API calls failing:**
- Verify backend is running on port 8000
- Check CORS settings
- Verify API URL in `src/utils/api.js`

## Production Build

For production, build the app:

```bash
npm run build
```

This creates optimized files in `dist/` folder.

Preview production build:

```bash
npm run preview
```

## File Structure

```
frontend/
├── src/
│   ├── pages/          # Page components (auto-reload)
│   ├── contexts/       # React contexts (auto-reload)
│   ├── utils/          # Utilities (auto-reload)
│   ├── App.jsx         # Main app (auto-reload)
│   └── main.jsx        # Entry point (may need refresh)
├── index.html          # HTML template (may need refresh)
├── vite.config.js      # Vite config (needs restart)
└── package.json        # Dependencies (needs restart)
```

## Tips

1. **Keep dev server running** while coding
2. **Watch terminal** for compilation errors
3. **Use browser DevTools** to debug
4. **Save files frequently** - changes appear on save
5. **Check network tab** if API calls fail

