# IssueHub - A Lightweight Bug Tracker

IssueHub is a minimal bug tracker where teams can create projects, file issues, comment on them, and track status. Built with Django REST Framework backend and React frontend.

## Features

- **User Authentication**: Sign up, login, and logout with JWT tokens
- **Project Management**: Create projects and manage team members
- **Issue Tracking**: Create, update, delete, and track issues with status and priority
- **Comments**: Add comments to issues for collaboration
- **Filtering & Search**: Filter issues by status, priority, assignee, and search by text
- **Sorting**: Sort issues by date, priority, or status
- **Role-Based Access**: Maintainers can manage projects and change issue status/assignee
- **Responsive UI**: Clean, modern interface that works on all devices

## Tech Stack

### Backend
- **Django 5.2.8**: Web framework
- **Django REST Framework**: REST API
- **djangorestframework-simplejwt**: JWT authentication
- **PostgreSQL**: Database (SQLite for local development)
- **django-cors-headers**: CORS handling

### Frontend
- **React 18**: UI library
- **Vite**: Build tool and dev server
- **React Router**: Client-side routing
- **Axios**: HTTP client

## Tech Choices & Trade-offs

### Backend Framework: Django vs FastAPI/Flask

**Choice: Django**

**Rationale:**
- **Pros**: 
  - Built-in ORM for rapid development
  - Admin interface for data management
  - Comprehensive authentication system
  - Mature ecosystem with excellent documentation
  - Automatic migrations
  - Built-in security features (CSRF, XSS protection)
- **Trade-offs**:
  - More opinionated than FastAPI/Flask
  - Slightly heavier than micro-frameworks
  - Less suitable for high-performance async workloads (though Django 3.1+ supports async)

**Alternative Considered**: FastAPI would offer better async performance and automatic API docs, but Django's ORM and admin panel significantly speed up development for this use case.

### Database: PostgreSQL vs SQLite

**Choice: PostgreSQL (production) / SQLite (development)**

**Rationale:**
- **PostgreSQL Pros**: 
  - Production-ready with ACID compliance
  - Better concurrency handling
  - Advanced features (JSON fields, full-text search)
  - Better for multi-user scenarios
- **SQLite Pros**:
  - Zero configuration for local development
  - Perfect for MVP and testing
  - Single file database
- **Trade-off**: SQLite doesn't handle concurrent writes well, but sufficient for development and small teams.

### Frontend: React vs Vue

**Choice: React**

**Rationale:**
- **Pros**:
  - Larger ecosystem and community
  - More job market relevance
  - Excellent tooling (Vite, React Router)
  - Hooks API for clean state management
- **Trade-off**: Vue might be easier for beginners, but React's ecosystem is more mature.

### Build Tool: Vite vs Create React App

**Choice: Vite**

**Rationale:**
- **Pros**:
  - Much faster development server
  - Better HMR (Hot Module Replacement)
  - Modern ES modules
  - Smaller bundle sizes
- **Trade-off**: CRA is more established, but Vite is the future of React tooling.

### State Management: Context API vs Redux

**Choice: Context API**

**Rationale:**
- **Pros**:
  - Built into React, no extra dependencies
  - Simpler for small-to-medium apps
  - Less boilerplate
- **Trade-off**: Redux would be better for complex state management, but overkill for this MVP.

### Authentication: JWT vs Session-based

**Choice: JWT**

**Rationale:**
- **Pros**:
  - Stateless authentication (scales better)
  - Works well with SPAs
  - No server-side session storage needed
- **Trade-off**: 
  - Harder to revoke tokens (would need token blacklist)
  - Tokens can't be invalidated before expiry
  - For production, would add refresh token rotation and blacklisting

## Project Structure

```
IssueHub-a-Lightweight-Bug-Tracker/
├── issuehub_backend/          # Django project settings
│   ├── settings.py            # Main settings
│   ├── urls.py                # Root URL configuration
│   └── exceptions.py          # Custom exception handler
├── users/                     # User authentication app
│   ├── models.py              # Custom User model
│   ├── views.py               # Auth endpoints
│   ├── serializers.py         # User serializers
│   └── tests.py               # User tests
├── projects/                  # Projects app
│   ├── models.py              # Project and ProjectMember models
│   ├── views.py               # Project endpoints
│   ├── serializers.py        # Project serializers
│   ├── permissions.py        # Project permissions
│   └── tests.py               # Project tests
├── issues/                    # Issues app
│   ├── models.py              # Issue model
│   ├── views.py               # Issue endpoints
│   ├── serializers.py        # Issue serializers
│   ├── permissions.py        # Issue permissions
│   └── tests.py               # Issue tests
├── comments/                  # Comments app
│   ├── models.py              # Comment model
│   ├── views.py               # Comment endpoints
│   └── serializers.py        # Comment serializers
├── frontend/                  # React frontend
│   ├── src/
│   │   ├── pages/            # Page components
│   │   ├── contexts/         # React contexts
│   │   └── utils/            # Utilities
│   └── package.json
├── requirements.txt           # Python dependencies
├── seed_data.py              # Demo data script
└── README.md
```

## Setup Instructions

### Prerequisites

- **Python 3.8+** (tested with Python 3.12)
  - Download from [python.org](https://www.python.org/downloads/)
  - Make sure to check "Add Python to PATH" during installation
  
- **Node.js 16+** and npm (tested with Node 18+)
  - Download from [nodejs.org](https://nodejs.org/) (choose LTS version)
  - npm comes bundled with Node.js
  - Make sure to check "Add to PATH" during installation
  - Verify installation: `node --version` and `npm --version`
  
- **PostgreSQL** (optional, SQLite works for local dev)
  - Only needed if you want to use PostgreSQL instead of SQLite
  - Download from [postgresql.org](https://www.postgresql.org/download/)
  
- **Git** (for cloning the repository)
  - Download from [git-scm.com](https://git-scm.com/downloads)

### Environment Variables

Create a `.env` file in the root directory (optional for local development with SQLite):

```env
# Django Settings
SECRET_KEY=your-secret-key-here-change-in-production
DEBUG=True

# Database Configuration (PostgreSQL)
# Leave empty/unset to use SQLite for local development
DB_NAME=issuehub
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432

# Frontend API URL (optional, defaults to http://localhost:8000/api)
VITE_API_URL=http://localhost:8000/api
```

**Note**: For local development with SQLite, you don't need to create a `.env` file. The application will use SQLite by default.

### Database Setup

#### Option 1: SQLite (Default - No Setup Required)
SQLite is used by default. No additional configuration needed. The database file (`db.sqlite3`) will be created automatically when you run migrations.

#### Option 2: PostgreSQL (Production/Advanced)
1. Install PostgreSQL on your system
2. Create a database:
   ```sql
   CREATE DATABASE issuehub;
   CREATE USER your_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE issuehub TO your_user;
   ```
3. Update `.env` file with your database credentials
4. The application will automatically use PostgreSQL if `DB_NAME` is set in `.env`

### Backend Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd IssueHub-a-Lightweight-Bug-Tracker
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows (PowerShell)
   # If you get execution policy error, run this first:
   # Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   .\venv\Scripts\activate
   
   # On Windows (CMD/Command Prompt)
   venv\Scripts\activate.bat
   
   # On Windows (Git Bash)
   source venv/Scripts/activate
   
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```
   This creates all necessary database tables. You'll see output like:
   ```
   Operations to perform:
     Apply all migrations: admin, auth, comments, contenttypes, issues, projects, sessions, users
   Running migrations:
     ...
   ```

5. **Create superuser** (optional, for Django admin)
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin user.

6. **Seed demo data** (optional, recommended for testing)
   ```bash
   python manage.py shell
   >>> exec(open('seed_data.py').read())
   >>> exit()
   ```
   This creates:
   - 5 demo users (user1@example.com to user5@example.com, password: `password123`)
   - 2 projects with members
   - 20 issues with various statuses and priorities
   - Sample comments

7. **Start backend development server**
   ```bash
   python manage.py runserver
   ```
   Backend will be available at `http://localhost:8000`
   
   You should see:
   ```
   Starting development server at http://127.0.0.1:8000/
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install Node.js dependencies** (first time only)
   ```bash
   npm install
   ```
   This installs React, Vite, React Router, Axios, and other dependencies.

3. **Start frontend development server**
   ```bash
   npm run dev
   ```
   Frontend will be available at `http://localhost:5173`
   
   You should see:
   ```
   VITE v5.x.x  ready in xxx ms
   ➜  Local:   http://localhost:5173/
   ```

4. **Open in browser**
   Navigate to `http://localhost:5173` in your browser. You should see the login page.

## How to Run

### Running the Backend

```bash
# Activate virtual environment (if not already active)
# Windows (PowerShell/CMD)
.\venv\Scripts\activate

# Windows (Git Bash)
source venv/Scripts/activate

# Linux/Mac
source venv/bin/activate

# Start Django development server
python manage.py runserver

# Server runs on http://localhost:8000
# API available at http://localhost:8000/api
```

**Backend Endpoints:**
- API: `http://localhost:8000/api`
- Admin: `http://localhost:8000/admin`
- API Root: `http://localhost:8000/api/` (if browsable API is enabled)

### Running the Frontend

```bash
# Navigate to frontend directory
cd frontend

# Start Vite development server
npm run dev

# Server runs on http://localhost:5173
```

**Frontend Routes:**
- Login: `http://localhost:5173/login`
- Signup: `http://localhost:5173/signup`
- Projects: `http://localhost:5173/projects`
- Project Detail: `http://localhost:5173/projects/{id}`
- Issue Detail: `http://localhost:5173/issues/{id}`

### Running Tests

#### Backend Tests

```bash
# Activate virtual environment
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Run all tests
python manage.py test

# Run tests with verbose output
python manage.py test --verbosity=2

# Run specific app tests
python manage.py test users
python manage.py test projects
python manage.py test issues

# Run specific test class
python manage.py test users.tests.UserAuthTests

# Run with coverage (requires coverage.py)
pip install coverage
coverage run --source='.' manage.py test
coverage report
```

**Expected Test Output:**
```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
...
----------------------------------------------------------------------
Ran X tests in X.XXXs

OK
Destroying test database for alias 'default'...
```

#### Frontend Tests

Frontend tests are not included in this MVP. To add them:
```bash
npm install --save-dev @testing-library/react @testing-library/jest-dom vitest
```

### Running Both Servers

**Terminal 1 (Backend):**
```bash
# Windows (PowerShell/CMD)
.\venv\Scripts\activate

# Windows (Git Bash)  
source venv/Scripts/activate

# Linux/Mac
source venv/bin/activate

python manage.py runserver
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

Then open `http://localhost:5173` in your browser.


## API Endpoints

### Authentication
- `POST /api/auth/signup/` - User signup
- `POST /api/auth/login/` - User login
- `GET /api/me/` - Get current user profile
- `POST /api/auth/refresh/` - Refresh JWT token

### Projects
- `GET /api/projects/` - List user's projects
- `POST /api/projects/` - Create project
- `GET /api/projects/{id}/` - Get project details
- `PATCH /api/projects/{id}/` - Update project
- `DELETE /api/projects/{id}/` - Delete project
- `GET /api/projects/{id}/members/` - List project members
- `POST /api/projects/{id}/members/` - Add project member

### Issues
- `GET /api/projects/{id}/issues/` - List issues (with filters)
  - Query params: `q`, `status`, `priority`, `assignee`, `sort`
- `POST /api/projects/{id}/issues/` - Create issue
- `GET /api/issues/{id}/` - Get issue details
- `PATCH /api/issues/{id}/` - Update issue
- `DELETE /api/issues/{id}/` - Delete issue

### Comments
- `GET /api/issues/{id}/comments/` - List comments
- `POST /api/issues/{id}/comments/` - Add comment

### Authentication
All endpoints except `/api/auth/signup/` and `/api/auth/login/` require authentication via JWT token in the Authorization header:
```
Authorization: Bearer <access_token>
```

## User Roles

### User (Member)
- Can create, read, update, and delete their own issues
- Can comment on issues in projects they belong to
- Can view all issues in their projects

### Project Maintainer
- All member permissions, plus:
- Can update/assign/close any issue in their project
- Can manage project membership (add/remove members)
- Can change issue status and assignee

## Database Schema

### Users
- `id`, `email`, `name`, `password_hash`, `created_at`

### Projects
- `id`, `name`, `key`, `description`, `created_at`

### ProjectMembers
- `project_id`, `user_id`, `role` (member/maintainer), `created_at`

### Issues
- `id`, `project_id`, `title`, `description`, `status`, `priority`, `reporter_id`, `assignee_id`, `created_at`, `updated_at`
- Status: `open`, `in_progress`, `resolved`, `closed`
- Priority: `low`, `medium`, `high`, `critical`

### Comments
- `id`, `issue_id`, `author_id`, `body`, `created_at`

## Architecture Notes

### Backend Architecture

1. **Models**: Django ORM models define the database schema
2. **Serializers**: DRF serializers handle request/response data transformation
3. **Views**: ViewSets provide CRUD operations with proper permissions
4. **Permissions**: Custom permission classes enforce role-based access control
5. **URLs**: RESTful URL routing with nested resources

### Frontend Architecture

1. **Context API**: AuthContext manages authentication state
2. **API Client**: Axios instance with interceptors for token management
3. **Pages**: React components for each major view
4. **Routing**: React Router for client-side navigation
5. **State Management**: Local component state with React hooks

### Security Features

- Password hashing with Django's default password hasher
- JWT token-based authentication
- CORS configuration for frontend-backend communication
- Input validation with DRF serializers
- Role-based permission checks
- Protected API routes

## Development

### Adding New Features

1. **Backend**: Add models → serializers → views → URLs → tests
2. **Frontend**: Create components → add routes → integrate with API

### Code Style

- Backend: Follow PEP 8 and Django conventions
- Frontend: Follow React best practices and ESLint rules

## Demo Credentials

After running the seed script, you can use these demo accounts:

| Email | Password | Role |
|-------|----------|------|
| `user1@example.com` | `password123` | Maintainer (default for created projects) |
| `user2@example.com` | `password123` | Member |
| `user3@example.com` | `password123` | Member |
| `user4@example.com` | `password123` | Member |
| `user5@example.com` | `password123` | Member |

**Note**: All users have the same password for demo purposes. In production, users would set their own passwords.

## Known Limitations & Future Improvements

### Current Limitations

1. **No Email Notifications**
   - Users don't receive emails when assigned to issues or when comments are added
   - **Workaround**: Users must check the application manually

2. **No File Attachments**
   - Issues and comments are text-only
   - No image or file upload support
   - **Workaround**: Use external links or paste image URLs

3. **No Real-time Updates**
   - Changes don't appear instantly for other users
   - Requires page refresh to see updates
   - **Workaround**: Manual refresh or polling (not implemented)

4. **Limited Search**
   - Search only works on issue title and description
   - No full-text search across comments
   - **Workaround**: Use filters and manual browsing

5. **No Issue History/Audit Log**
   - Can't see who changed what and when
   - No version history for issues
   - **Workaround**: Check comments for context

6. **Basic Pagination**
   - Pagination exists but no infinite scroll
   - Limited to 20 items per page
   - **Workaround**: Use page navigation

7. **No Project Templates**
   - Must create projects from scratch
   - Can't duplicate projects or use templates
   - **Workaround**: Manual setup for each project

8. **No Bulk Operations**
   - Can't select multiple issues for bulk actions
   - No bulk status updates or assignments
   - **Workaround**: Update issues one by one

9. **No Issue Dependencies**
   - Can't link issues as blockers or dependencies
   - No issue relationships
   - **Workaround**: Mention in descriptions/comments

10. **No Advanced Permissions**
    - Only two roles: member and maintainer
    - Can't customize permissions per project
    - **Workaround**: Use maintainer role for admins

### What I'd Do With More Time

#### High Priority

1. **Email Notifications**
   - Send emails on issue assignment, status changes, new comments
   - User preferences for notification types
   - Use Django's email backend or Celery for async sending

2. **File Attachments**
   - Add file upload to issues and comments
   - Image preview in comments
   - Use Django's FileField with cloud storage (S3) for production

3. **Real-time Updates**
   - Implement WebSockets (Django Channels) or Server-Sent Events
   - Live updates when issues/comments change
   - Presence indicators (who's viewing what)

4. **Advanced Search**
   - Full-text search with PostgreSQL's `tsvector` or Elasticsearch
   - Search across comments, users, projects
   - Advanced filters (date ranges, multiple assignees)

5. **Issue History/Audit Trail**
   - Track all changes with django-simple-history
   - Show "who changed what and when"
   - Revert to previous versions

#### Medium Priority

6. **Issue Dependencies & Relationships**
   - Link issues as blockers, duplicates, related
   - Visual dependency graph
   - Automatic status updates based on dependencies

7. **Bulk Operations**
   - Multi-select issues
   - Bulk status/priority/assignee updates
   - Bulk delete with confirmation

8. **Project Templates**
   - Pre-configured project templates
   - Duplicate existing projects
   - Import/export project configurations

9. **Advanced Permissions**
   - Custom roles per project
   - Granular permissions (can edit title but not status)
   - Permission inheritance

10. **Dashboard & Analytics**
    - Project dashboards with charts
    - Issue velocity metrics
    - Burndown charts
    - Team performance stats

#### Nice to Have

11. **Markdown Support**
    - Rich text editing with Markdown
    - Code blocks with syntax highlighting
    - Tables, lists, formatting

12. **Issue Templates**
    - Pre-filled issue templates
    - Bug report template, feature request template
    - Custom templates per project

13. **Tags/Labels**
    - Add tags to issues
    - Filter by tags
    - Tag-based workflows

14. **Time Tracking**
    - Log time spent on issues
    - Time estimates vs actual
    - Reports by time

15. **API Documentation**
    - Swagger/OpenAPI documentation
    - Interactive API explorer
    - API versioning

16. **Mobile App**
    - React Native mobile app
    - Push notifications
    - Offline support

17. **CI/CD Integration**
    - Link issues to GitHub/GitLab PRs
    - Auto-close issues on merge
    - Commit message integration

18. **Export/Import**
    - Export issues to CSV/JSON
    - Import from Jira, GitHub Issues
    - Backup/restore functionality

## Live Demo (Optional)

**Note**: This section would be filled in if a live deployment exists.

If you have a live deployment, include:
- **Live URL**: `https://issuehub-demo.example.com`
- **Demo Credentials**: 
  - Email: `demo@example.com`
  - Password: `demo123`
- **Status**: Active / Under Maintenance / Archived

For deployment options, consider:
- **Backend**: Heroku, Railway, DigitalOcean, AWS, Google Cloud
- **Frontend**: Vercel, Netlify, GitHub Pages
- **Database**: Managed PostgreSQL (AWS RDS, Heroku Postgres, etc.)

## Troubleshooting

### Backend Issues

**Migration Errors:**
```bash
# Reset migrations (WARNING: deletes data)
python manage.py migrate --run-syncdb

# Or create fresh migrations
python manage.py makemigrations
python manage.py migrate
```

**Port Already in Use:**
```bash
# Use different port
python manage.py runserver 8001
```

**Import Errors:**
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

**Database Connection Errors (PostgreSQL):**
- Verify `.env` file has correct credentials
- Check PostgreSQL is running: `pg_isready`
- Test connection: `psql -U your_user -d issuehub`

**CORS Errors:**
- Verify `CORS_ALLOWED_ORIGINS` in `settings.py` includes frontend URL
- Check `django-cors-headers` is in `INSTALLED_APPS` and `MIDDLEWARE`

### Frontend Issues

**Module Not Found:**
```bash
# Clear and reinstall
rm -rf node_modules package-lock.json
npm install
```

**API Connection Errors:**
- Verify backend is running on `http://localhost:8000`
- Check `frontend/src/utils/api.js` has correct `API_BASE_URL`
- Check browser console for CORS errors
- Verify JWT token is being sent in headers

**Build Errors:**
```bash
# Clear Vite cache
rm -rf node_modules/.vite
npm run dev
```

**Port Already in Use:**
```bash
# Vite will automatically use next available port
# Or specify port in vite.config.js
```

### Common Issues

**PowerShell Execution Policy Error**
- Error: "cannot be loaded because running scripts is disabled on this system"
- **Solution 1** (Recommended for development): Change execution policy for current user
  ```powershell
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
  Then try activating again: `.\venv\Scripts\activate`
- **Solution 2**: Use Command Prompt (CMD) instead of PowerShell
  ```cmd
  venv\Scripts\activate.bat
  ```
- **Solution 3**: Bypass for single command (not recommended for regular use)
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
  Or: `powershell -ExecutionPolicy Bypass -File .\venv\Scripts\Activate.ps1`

**"No module named 'django'"**
- Virtual environment not activated
- Solution: 
  - Windows (PowerShell/CMD): `.\venv\Scripts\activate` (or `venv\Scripts\activate.bat` in CMD)
  - Windows (Git Bash): `source venv/Scripts/activate`
  - Linux/Mac: `source venv/bin/activate`

**"npm: command not found" or "node: command not found"**
- Node.js is not installed or not in PATH
- **Solution 1**: Install Node.js from [nodejs.org](https://nodejs.org/)
  - Download the LTS (Long Term Support) version
  - During installation, make sure "Add to PATH" is checked
  - Restart your terminal after installation
  - Verify: `node --version` and `npm --version`
- **Solution 2**: If using Git Bash and Node.js is installed but not found:
  - Try using PowerShell or CMD instead: `cd frontend && npm install`
  - Or add Node.js to Git Bash PATH (usually `C:\Program Files\nodejs\`)

**"Module not found: Can't resolve 'react'"**
- Node modules not installed
- Solution: `cd frontend && npm install`

**"CSRF verification failed"**
- This is normal for API endpoints
- JWT authentication handles security instead

**"401 Unauthorized"**
- Token expired or invalid
- Solution: Log out and log back in
- Check token refresh is working

**Database locked (SQLite)**
- Multiple processes accessing SQLite
- Solution: Use PostgreSQL for production, or ensure only one process accesses DB

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
