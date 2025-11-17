# Development Environment Setup - Complete!

Your Catholic Ride Share development environment is now ready for use with Cursor.

## What Was Set Up

### ✅ Project Structure
- Full FastAPI backend with organized directory structure
- Database models for users, drivers, parishes, and rides
- API endpoints framework
- Configuration files

### ✅ Development Tools
- Python virtual environment at `backend/venv/`
- All Python dependencies installed
- Docker containers running:
  - PostgreSQL with PostGIS (port 5433)
  - Redis (port 6379)

### ✅ Cursor/VS Code Configuration
- `.vscode/settings.json` - Python, formatting, linting settings
- `.vscode/extensions.json` - Recommended extensions
- `.vscode/launch.json` - Debug configurations
- `.vscode/tasks.json` - Useful tasks (migrations, tests, etc.)
- `.cursorrules` - AI assistant guidelines for this project

### ✅ Environment Configuration
- `.env` file created with development settings
- Database URL: `postgresql://catholic_user:catholic_password@localhost:5433/catholic_ride_share`
- Generated SECRET_KEY for JWT authentication

## Next Steps

### 1. Open Project in Cursor
```bash
cd /Users/schoedel/development/catholic-ride-share
cursor .
```

### 2. Install Recommended Extensions
When Cursor opens, it will prompt you to install recommended extensions. Click "Install All".

### 3. Select Python Interpreter
1. Press `Cmd+Shift+P`
2. Type "Python: Select Interpreter"
3. Choose `./backend/venv/bin/python`

### 4. Create Initial Database Migration
```bash
cd backend
source venv/bin/activate
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

### 5. Start the Development Server

**Option A: Using Cursor's Debug Feature**
1. Go to Run & Debug panel (Cmd+Shift+D)
2. Select "FastAPI: Debug" from dropdown
3. Press F5 to start debugging

**Option B: Using Terminal**
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload
```

Visit http://localhost:8000/docs to see the API documentation.

### 6. Run Tests
```bash
cd backend
source venv/bin/activate
pytest
```

### 7. Format Code
```bash
cd backend
source venv/bin/activate
black .
isort .
```

## Useful Commands

### Database
```bash
# Create new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

### Docker
```bash
# Start services
docker-compose up -d db redis

# Stop services
docker-compose down

# View logs
docker-compose logs -f db
```

### Testing
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py
```

## Project Resources

- **API Docs**: http://localhost:8000/docs
- **GitHub Repo**: https://github.com/schoedel-learn/catholic-ride-share
- **Architecture Docs**: `docs/ARCHITECTURE.md`

## Troubleshooting

### Port Already in Use
If you get port conflicts:
```bash
# Check what's using the port
lsof -i :8000
lsof -i :5433

# Kill the process or change the port in docker-compose.yml
```

### Database Connection Issues
```bash
# Restart database
docker-compose restart db

# Check database is running
docker-compose ps
```

### Virtual Environment Issues
```bash
# Recreate virtual environment
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Development Workflow

1. Create feature branch: `git checkout -b feature/your-feature`
2. Make changes with hot reload active
3. Write tests for new features
4. Run tests and linting
5. Commit changes: `git commit -m "description"`
6. Push and create PR

## Important Files

- `backend/.env` - Environment variables (never commit!)
- `backend/app/main.py` - FastAPI application entry point
- `backend/app/models/` - Database models
- `backend/app/api/endpoints/` - API routes
- `docker-compose.yml` - Docker services configuration

## Ready to Code!

Your environment is fully configured. Start developing by:

1. Opening the project in Cursor
2. Creating the initial database migration
3. Starting the FastAPI server
4. Building your first feature!

Happy coding! 🚀
