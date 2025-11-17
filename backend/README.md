# Catholic Ride Share - Backend API

FastAPI-based backend for the Catholic Ride Share application.

## Quick Start

### With Docker
```bash
# From project root
docker-compose up -d

# Run migrations
docker-compose exec backend alembic upgrade head
```

### Without Docker
```bash
# Install dependencies
pip install -r requirements.txt

# Set up .env file
cp .env.example .env
# Edit .env with your configuration

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
app/
├── api/
│   ├── endpoints/      # Route handlers
│   │   ├── auth.py
│   │   ├── users.py
│   │   ├── rides.py
│   │   ├── drivers.py
│   │   └── parishes.py
│   └── deps/          # Dependencies
│       └── auth.py    # Authentication dependencies
├── core/              # Core configuration
│   ├── config.py      # Settings
│   └── security.py    # Security utilities
├── models/            # SQLAlchemy models
│   ├── user.py
│   ├── driver_profile.py
│   ├── parish.py
│   ├── ride_request.py
│   └── ride.py
├── schemas/           # Pydantic schemas
│   ├── user.py
│   └── token.py
├── services/          # Business logic
├── ai/               # AI/ML services
├── db/               # Database
│   └── session.py    # DB session
├── utils/            # Utilities
└── main.py           # FastAPI app
```

## Database Models

### Users
- Basic user information
- Role (rider, driver, both, admin)
- Parish affiliation

### Driver Profiles
- Vehicle information
- Verification status
- Availability toggle
- Statistics (rides, rating)

### Parishes
- Church information
- Location (PostGIS point)
- Contact details
- Mass times

### Ride Requests
- Pickup/destination locations
- Destination type
- Requested datetime
- Status tracking

### Rides
- Links request to accepted driver
- Real-time status updates
- Timing information
- Actual locations

## Development

### Testing
```bash
pytest
pytest --cov=app --cov-report=html
```

### Code Formatting
```bash
black .
isort .
```

### Type Checking
```bash
mypy app/
```

### Database Migrations

Create migration:
```bash
alembic revision --autogenerate -m "description"
```

Apply migrations:
```bash
alembic upgrade head
```

Rollback:
```bash
alembic downgrade -1
```

## Environment Variables

Required:
- `SECRET_KEY` - JWT secret
- `DATABASE_URL` - PostgreSQL connection

Optional:
- `GOOGLE_MAPS_API_KEY`
- `OPENAI_API_KEY` or `ANTHROPIC_API_KEY`
- `STRIPE_SECRET_KEY`
- Email/SMS configuration

See `.env.example` for complete list.
