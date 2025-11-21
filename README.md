# Catholic Ride Share

A community-driven ride-sharing application connecting Catholics who need transportation to Mass, Confession, prayer events, and church social functions with volunteer drivers in their area.

## Mission

To strengthen Catholic communities by ensuring that transportation is never a barrier to participating in the sacraments and church life.

## Features

### Current (Phase 1 - MVP)
- User registration and authentication
- Driver and rider profiles
- Location-based ride matching (10-mile radius)
- Real-time ride requests and notifications
- In-app messaging
- Driver verification workflow
- Parish database integration
- Donation system (optional, not required)

### Planned
- AI-powered driver-rider matching optimization
- AI chatbot assistant for Mass times and ride booking
- Route optimization for carpooling
- AI safety and content moderation
- Multi-language support
- Community features and parish integration

## Technology Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL with PostGIS (geospatial)
- **Cache**: Redis
- **Task Queue**: Celery
- **Authentication**: JWT with OAuth2

### AI/ML
- OpenAI/Anthropic APIs for chatbot
- scikit-learn for matching algorithms
- Google Maps API for routing

### Infrastructure
- Docker & Docker Compose
- PostgreSQL with PostGIS extension
- Redis for caching and pub/sub

## Project Structure

```
catholic-ride-share/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── endpoints/      # API route handlers
│   │   │   └── deps/           # Dependencies (auth, etc.)
│   │   ├── core/               # Config and security
│   │   ├── models/             # SQLAlchemy models
│   │   ├── schemas/            # Pydantic schemas
│   │   ├── services/           # Business logic
│   │   ├── ai/                 # AI/ML services
│   │   ├── db/                 # Database session
│   │   └── utils/              # Utilities
│   ├── tests/                  # Test suite
│   ├── alembic/                # Database migrations
│   ├── requirements.txt        # Python dependencies
│   └── Dockerfile
├── frontend/                   # Future: React Native or React
├── docs/                       # Documentation
├── docker-compose.yml
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.11+
- Docker and Docker Compose
- PostgreSQL (if not using Docker)
- Redis (if not using Docker)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/catholic-ride-share.git
   cd catholic-ride-share
   ```

2. **Set up environment variables**
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Using Docker (Recommended)**
   ```bash
   # Start all services
   docker-compose up -d

   # Run database migrations
   docker-compose exec backend alembic upgrade head

   # View logs
   docker-compose logs -f backend
   ```

4. **Manual Setup (Alternative)**
   ```bash
   # Create virtual environment
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt

   # Run migrations
   alembic upgrade head

   # Start the application
   uvicorn app.main:app --reload
   ```

### Accessing the Application

- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

## Development

### Running Tests
```bash
cd backend
pytest
```

### Code Quality
```bash
# Format code
black .

# Sort imports
isort .

# Lint
flake8 .

# Type checking
mypy .
```

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register new user
- `POST /api/v1/auth/login` - Login and get access token

### Users
- `GET /api/v1/users/me` - Get current user profile
- `PUT /api/v1/users/me` - Update current user profile

### Rides
- `POST /api/v1/rides/` - Create ride request
- `GET /api/v1/rides/` - List rides

### Drivers
- `POST /api/v1/drivers/profile` - Create driver profile
- `GET /api/v1/drivers/available` - Get available drivers

### Parishes
- `GET /api/v1/parishes/` - List parishes
- `GET /api/v1/parishes/{id}` - Get parish details

## Environment Variables

Key environment variables (see `.env.example` for complete list):

- `SECRET_KEY` - JWT secret key (CHANGE IN PRODUCTION)
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `GOOGLE_MAPS_API_KEY` - For routing and geocoding
- `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` - For AI features
- `STRIPE_SECRET_KEY` - For donation processing (optional)

## Contributing

This is a community project. Contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

## External Integrations

If you're using external tools like BrainGrid, GitHub Copilot, or other integrations with this repository, please see the [External Integrations Guide](docs/EXTERNAL_INTEGRATIONS.md) for setup instructions and troubleshooting.

## Security

- Never commit `.env` files or sensitive credentials
- All passwords are hashed using bcrypt
- JWT tokens for authentication
- Input validation using Pydantic
- SQL injection protection via SQLAlchemy ORM
- CORS configuration for frontend access

## License

This project is built to serve the Catholic community. License TBD.

## Roadmap

See the planning document for detailed phases:

- **Phase 1** (Current): Foundation and core ride-sharing
- **Phase 2**: Enhanced features (donations, ratings, verification)
- **Phase 3**: AI chatbot and basic matching
- **Phase 4-5**: Advanced AI features
- **Phase 6**: Admin dashboard
- **Phase 7**: Production polish
- **Phase 8**: Launch and iteration

## Support

For questions or support, please open an issue on GitHub.

## Acknowledgments

Built with love for the Catholic community to ensure everyone can participate in the life of the Church.
