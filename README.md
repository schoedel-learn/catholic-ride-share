# Catholic Ride Share

A community-driven ride-sharing application connecting Catholics who need transportation to Mass, Confession, prayer events, and church social functions with volunteer drivers who are willing to help – especially in rural areas where distances can be long.

## Mission

To strengthen Catholic communities by ensuring that transportation is never a barrier to participating in the sacraments and church life.

## What We Are Building

At a high level, Catholic Ride Share is:

- A **volunteer ride network**: riders request help getting to church activities; drivers choose which rides they are willing to take.
- **Rural-friendly**: rides may be 10, 20, or more miles away; there is **no hard distance limit**. Distance is information, not a gate.
- **Privacy-conscious**: only the information needed to coordinate rides is stored; parish records only include **full name and address**, not Mass times or links that change frequently.
- **Donation-based**: riders can optionally offer donations after rides (via Stripe); there is no required payment for rides.
- **Admin-supported**: admins can verify drivers, monitor the system, and help resolve issues.

## Feature Overview

### Implemented (Backend foundation so far)

- **Authentication & accounts**
  - User registration with email and password.
  - JWT-based login (`access_token` + `refresh_token`).
  - Email verification with 6‑digit codes (required before using ride features).
  - Password reset flow with secure, single-use reset tokens.
- **User profiles**
  - Rider/driver/both/admin roles.
  - Basic profile data (name, phone, parish reference).
  - Optional profile photo upload (stored on S3, resized to 500×500 thumbnail).
- **Core data models**
  - `User` with optional last-known location (geospatial point).
  - `DriverProfile` for vehicle and driver status (verification fields to be extended).
  - `Parish` with **name + postal address + optional geospatial location** (no Mass times or URLs).
  - `RideRequest` and `Ride` models for requests and live rides.
- **Infrastructure**
  - Dockerized stack: FastAPI backend, Postgres + PostGIS, Redis, Celery worker.
  - Alembic migrations wired to the same settings as the app.

> Note: Many endpoints are still simple stubs; the backend structure is in place and being built out according to the strategic plan in `braingrid-improvements`.

### Planned (Under active development)

- **Driver experience**
  - Complete driver profile management (vehicle details, documents).
  - Multi-step verification workflow (background checks, safe environment, admin approval).
  - Availability (scheduled windows + “available now for X hours” sessions).
- **Rider experience**
  - Create ride requests with pickup + destination and optional parish reference.
  - Discover willing drivers, with distance shown but **no fixed 10‑mile limit**.
  - Real-time ride status updates from acceptance through completion/cancellation.
- **Messaging & notifications**
  - In-ride chat between rider and driver (WebSocket / Socket.IO).
  - Push notifications (Firebase Cloud Messaging) + email notifications.
- **Donations & reviews**
  - Post-ride rating and optional donations via Stripe.
  - Transparent handling of Stripe fees and net amounts.
- **Admin tools**
  - Admin endpoints for users, drivers, rides, and statistics.
  - Simple web/admin UI (future) to manage verifications and issues.
- **AI & assistance (future)**
  - AI-powered matching suggestions.
  - AI assistant for parish/ride questions (without storing or serving Mass times).
  - Multi-language support.

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

### Frontend / Clients

- **Current**: Backend-first; no production frontend yet.
- **Planned**:
  - Flutter mobile app (primary client) for riders and drivers.
  - Lightweight web/admin frontend for admins and operations.

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

The backend is versioned under `/api/v1`. Some endpoints are fully implemented; others are present as stubs and will be expanded.

### Authentication (implemented)

- `POST /api/v1/auth/register`  
  Register a new user (creates an account and sends a verification email).

- `POST /api/v1/auth/login`  
  Login with email + password and receive access/refresh tokens.

- `POST /api/v1/auth/verify-email`  
  Verify email using a 6‑digit code sent to the user’s email.

- `POST /api/v1/auth/resend-verification`  
  Request that a new verification email be sent (idempotent-style behavior).

- `POST /api/v1/auth/forgot-password`  
  Initiate a password reset; always returns a generic success message and is rate-limited to prevent abuse and email enumeration.

- `POST /api/v1/auth/validate-reset-token`  
  Check whether a reset token is still valid.

- `POST /api/v1/auth/reset-password`  
  Reset a user’s password using a valid, single-use reset token.

### Users (implemented)

- `GET /api/v1/users/me`  
  Get the currently authenticated user’s profile.

- `PUT /api/v1/users/me`  
  Update the current user’s profile (name, phone, parish reference, etc.).

- `POST /api/v1/users/me/photo`  
  Upload or replace the current user’s profile photo (JPEG/PNG/WebP ≤ 5MB, stored in S3 as a 500×500 thumbnail).

- `DELETE /api/v1/users/me/photo`  
  Remove the current user’s profile photo (deletes the S3 object on a best-effort basis).

- `GET /api/v1/users/{user_id}`  
  Get another user’s public profile by ID (requires authentication).

### Rides, Drivers, Parishes (planned / partially stubbed)

These routes exist as placeholders and will be built out according to the strategic plan:

- `POST /api/v1/rides/` – Create ride request (planned: full request schema and matching).  
- `GET /api/v1/rides/` – List rides for the current user (planned).  
- `POST /api/v1/drivers/profile` – Create/update driver profile (planned).  
- `GET /api/v1/drivers/available` – Discover available/willing drivers nearby (planned; **no fixed distance limit**, distance used for ordering only).  
- `GET /api/v1/parishes/` – List parishes (full name + address only).  
- `GET /api/v1/parishes/{id}` – Get parish details (full name + address only).

## Environment Variables

Key environment variables (see `.env.example` for complete list):

- `SECRET_KEY` - JWT secret key (CHANGE IN PRODUCTION)
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `GOOGLE_MAPS_API_KEY` - For routing and geocoding (future features)

Email / notifications:
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USER`, `SMTP_PASSWORD` - Outbound email configuration
- `EMAILS_FROM_EMAIL`, `EMAILS_FROM_NAME` - From-address details

Storage:
- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` - AWS credentials
- `AWS_S3_BUCKET` - S3 bucket for profile photos and documents
- `AWS_REGION` - AWS region for the bucket

Payments:
- `STRIPE_SECRET_KEY`, `STRIPE_PUBLISHABLE_KEY`, `STRIPE_WEBHOOK_SECRET` - For donation processing (optional)

Background checks / notifications (future):
- `CHECKR_API_KEY` - For background check integration (optional)
- `FIREBASE_CREDENTIALS_PATH`, `FIREBASE_PROJECT_ID` - For Firebase Cloud Messaging

AI (future):
- `OPENAI_API_KEY` or `ANTHROPIC_API_KEY` - For AI assistant and matching features

## Contributing

This is a community project. Contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Security

**Catholic Ride Share takes security seriously.** This application handles sensitive user data for a non-profit organization serving the Catholic community.

### Security Features

- ✅ All passwords are hashed using bcrypt
- ✅ JWT tokens for authentication with access and refresh tokens
- ✅ Email verification for new accounts
- ✅ Secure password reset flow
- ✅ Input validation using Pydantic
- ✅ SQL injection protection via SQLAlchemy ORM
- ✅ CORS configuration for frontend access
- ✅ Environment variable management (never commit `.env` files)
- ✅ Automated security scanning with CodeQL and Dependabot

### Security Documentation

- **[Security Policy](SECURITY.md)** - Vulnerability reporting and security practices
- **[Repository Security Settings](docs/REPOSITORY_SECURITY_SETTINGS.md)** - Complete security configuration guide
- **[Branch Protection Setup](docs/BRANCH_PROTECTION_SETUP.md)** - Instructions for protecting branches

### Reporting Security Vulnerabilities

**Do not report security vulnerabilities through public issues.** Please refer to our [Security Policy](SECURITY.md) for instructions on how to report vulnerabilities privately.

### For Contributors

Before contributing, review our security requirements:
- Read the [Security Policy](SECURITY.md)
- Complete the [Security Checklist](CONTRIBUTING.md#security-checklist-for-all-prs) for all PRs
- Never commit secrets, API keys, or credentials
- Validate and sanitize all user inputs

## License

This project is built to serve the Catholic community. License TBD.

## Roadmap

The detailed technical roadmap is maintained in the `braingrid-improvements` document and implemented in phases. In summary:

- **Foundation**: Core backend, authentication, email verification, password reset, and profile photos.  
- **Drivers & availability**: Driver profiles, verification, and availability (scheduled + “available now”).  
- **Rides & lifecycle**: Ride requests, matching based on willing drivers (not strict radius), ride status transitions, and cancellation rules.  
- **Messaging & notifications**: In-app messaging, push notifications, and email alerts.  
- **Donations & reviews**: Post-ride ratings and optional donations via Stripe.  
- **Parishes**: Simple parish records (name + address only) with geospatial search.  
- **Admin & analytics**: Admin APIs and dashboards for verification, issues, and high-level stats.  
- **Clients & AI**: Flutter mobile app, admin web UI, and AI-assisted matching/assistant.

## Support

For questions or support, please open an issue on GitHub.

## Acknowledgments

Built with love for the Catholic community to ensure everyone can participate in the life of the Church.
