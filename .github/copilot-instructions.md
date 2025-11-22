# GitHub Copilot Instructions for Catholic Ride Share

## Project Overview
Catholic Ride Share is a community-driven ride-sharing application connecting Catholics who need transportation to Mass, Confession, prayer events, and church social functions with volunteer drivers. This is a mission-driven project serving the Catholic community.

## Technology Stack
- **Backend**: Python 3.11+ with FastAPI
- **Database**: PostgreSQL with PostGIS (geospatial support)
- **Cache**: Redis
- **Task Queue**: Celery
- **Authentication**: JWT with OAuth2
- **Storage**: AWS S3 for profile photos and documents
- **Payments**: Stripe (for optional donations only)

## Code Style and Standards

### Python
- Use Python 3.11+ features and type hints for all function signatures
- Follow PEP 8 style guide strictly
- Format with Black (line length: 100)
- Sort imports with isort
- Use Pydantic for all data validation and schemas
- Prefer async/await for I/O operations
- Write comprehensive docstrings for all public functions and classes

### API Development
- Use RESTful conventions for endpoints
- Return appropriate HTTP status codes (200, 201, 400, 401, 404, etc.)
- Use Pydantic schemas for request/response validation
- Include proper error handling with HTTPException
- Document endpoints with docstrings (appears in OpenAPI/Swagger docs)
- Version all APIs under `/api/v1`

### Database
- Use SQLAlchemy ORM for all database operations
- Always use parameterized queries (ORM handles this automatically)
- Use Alembic for schema migrations
- PostGIS for geospatial queries (POINT, ST_DWithin, Geography type)
- Index frequently queried columns
- Store locations as POINT(longitude, latitude) in Geography type

### Security Practices
- NEVER commit secrets, API keys, or credentials
- Always use environment variables for sensitive data
- Hash passwords with bcrypt via passlib
- Validate and sanitize all user inputs
- Use JWT tokens with proper expiration
- Implement rate limiting on authentication endpoints
- Be aware of OWASP Top 10 vulnerabilities
- SQL injection protection via SQLAlchemy ORM

### Testing
- Write tests for all new features using pytest
- Aim for >80% code coverage
- Test both success and error cases
- Use fixtures for common test data
- Mock external services (S3, Stripe, email)

## Project Structure
```
backend/
├── app/
│   ├── api/
│   │   ├── endpoints/      # Route handlers (auth, users, rides, drivers, parishes)
│   │   └── deps/           # Dependencies (auth, database)
│   ├── models/             # SQLAlchemy models (User, DriverProfile, Parish, Ride, etc.)
│   ├── schemas/            # Pydantic schemas for request/response
│   ├── services/           # Business logic (email, storage, notifications)
│   ├── ai/                 # AI/ML services (future: chatbot, matching)
│   ├── core/               # Config, security, Redis
│   ├── db/                 # Database session management
│   └── utils/              # Utility functions
├── tests/                  # Test suite
├── alembic/                # Database migrations
└── requirements.txt        # Python dependencies
```

## Key Business Rules
- **No payment required**: Rides are volunteer-based; donations are optional
- **No hard distance limit**: Rural-friendly; 10-mile radius is suggested but not enforced
- **Email verification required**: Users must verify email before using ride features
- **Driver verification**: Multi-step process (background checks, safe environment training, admin approval)
- **Privacy-first**: Blur locations until ride is accepted; minimal data collection
- **Parish records**: Store only name + postal address (no Mass times or URLs that change frequently)

## Common Patterns

### Dependency Injection
```python
from app.api.deps.auth import get_current_active_user
from app.db.session import get_db

@router.get("/me")
async def get_profile(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    return current_user
```

### Error Handling
```python
from fastapi import HTTPException, status

if not resource:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Resource not found"
    )
```

### Geospatial Queries
```python
from geoalchemy2 import func

# Create a point from coordinates
point = func.ST_GeogFromText(f'POINT({longitude} {latitude})')

# Find nearby drivers within radius (in meters)
radius_meters = radius_miles * 1609.34
nearby = db.query(DriverProfile).filter(
    func.ST_DWithin(User.location, point, radius_meters),
    DriverProfile.is_available == True
).all()
```

### Async File Upload
```python
from app.services.storage import upload_file_to_s3

async def upload_photo(file: UploadFile):
    file_url = await upload_file_to_s3(
        file=file.file,
        filename=file.filename,
        content_type=file.content_type,
        folder="profile-photos"
    )
    return file_url
```

## Development Commands
```bash
# Start development server
uvicorn app.main:app --reload

# Run tests
pytest

# Format code
black . && isort .

# Type checking
mypy .

# Create migration
alembic revision --autogenerate -m "Description"

# Apply migrations
alembic upgrade head
```

## Important Context
- This serves the Catholic community - maintain respectful and appropriate code
- Privacy is critical - handle location data and personal information carefully
- Accessibility matters - consider users with disabilities in all features
- Multi-language support is planned - structure code for future i18n
- Rural focus - don't assume urban infrastructure (internet, GPS accuracy)

## Current Implementation Status
- ✅ Authentication (register, login, email verification, password reset)
- ✅ User profiles (name, phone, photo, parish reference)
- ✅ Profile photo upload to S3 with resizing
- ✅ JWT tokens with refresh
- ⚙️ Driver profiles (partial - needs verification workflow)
- ⚙️ Ride requests and matching (planned)
- ⚙️ In-ride messaging (planned)
- ⚙️ Push notifications (planned)
- ⚙️ Donations via Stripe (planned)
- ⚙️ AI assistant (future)

## Environment Variables
Key variables to be aware of (see `.env.example`):
- `SECRET_KEY` - JWT secret
- `DATABASE_URL` - PostgreSQL connection
- `REDIS_URL` - Redis connection
- `AWS_S3_BUCKET`, `AWS_REGION` - S3 storage
- `SMTP_*` - Email configuration
- `STRIPE_*` - Payment processing (optional)

## When Writing Code
1. Always add type hints to function signatures
2. Include docstrings with Args and Returns sections
3. Use Pydantic schemas for validation
4. Handle errors gracefully with appropriate HTTP status codes
5. Consider edge cases (empty lists, None values, invalid input)
6. Write tests alongside new features
7. Use async/await for database and external API calls
8. Never hardcode values - use config or environment variables
9. Log important events but avoid logging sensitive data
10. Follow existing patterns in the codebase for consistency

## References
- FastAPI docs: https://fastapi.tiangolo.com
- SQLAlchemy: https://docs.sqlalchemy.org
- Pydantic: https://docs.pydantic.dev
- PostGIS: https://postgis.net/documentation
