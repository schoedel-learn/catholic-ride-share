# System Architecture

## Overview

Catholic Ride Share is built using a modern, scalable architecture with Python/FastAPI backend, PostgreSQL with PostGIS for geospatial data, and AI/ML integration for intelligent matching and assistance.

## High-Level Architecture

```
┌─────────────┐
│   Mobile    │
│     App     │
│ (React      │
│  Native)    │
└──────┬──────┘
       │
       │ HTTPS/WSS
       │
┌──────▼──────────────────────────┐
│      Load Balancer              │
└──────┬──────────────────────────┘
       │
┌──────▼──────────────────────────┐
│     FastAPI Backend             │
│  ┌──────────────────────────┐  │
│  │   API Routes             │  │
│  ├──────────────────────────┤  │
│  │   Business Logic         │  │
│  ├──────────────────────────┤  │
│  │   AI/ML Services         │  │
│  └──────────────────────────┘  │
└────┬────────┬──────────┬────────┘
     │        │          │
     │        │          │
┌────▼─────┐ │  ┌──────▼────┐
│PostgreSQL│ │  │   Redis   │
│ PostGIS  │ │  │   Cache   │
└──────────┘ │  └───────────┘
             │
        ┌────▼─────┐
        │  Celery  │
        │  Worker  │
        └──────────┘
```

## Components

### Backend (FastAPI)
- RESTful API endpoints
- JWT authentication
- Real-time notifications via WebSockets
- Input validation with Pydantic
- Automatic API documentation

### Database (PostgreSQL + PostGIS)
- User and driver data
- Ride requests and history
- Parish information
- Geospatial queries for location-based matching
- Full ACID compliance

### Cache (Redis)
- Session storage
- Rate limiting
- Real-time pub/sub for notifications
- Caching frequently accessed data

### Background Tasks (Celery)
- Scheduled ride reminders
- Email/SMS notifications
- Periodic data cleanup
- ML model training updates

### AI/ML Services
- **Matching Algorithm**: Scores driver-rider pairs
- **Chatbot**: OpenAI/Claude for natural language interface
- **Safety Moderation**: Content filtering and pattern detection
- **Route Optimization**: Google Maps API integration

## Data Flow

### Ride Request Flow
1. Rider creates ride request via app
2. Backend validates request and stores in database
3. Geospatial query finds drivers within 10 miles
4. AI matching algorithm scores and ranks drivers
5. Push notifications sent to top drivers
6. Driver accepts ride
7. Real-time updates via WebSocket
8. Ride completion and optional donation

### Location Privacy
- Exact addresses hidden until ride accepted
- Location blur radius for privacy
- Option to use nearby landmarks
- Location data encrypted at rest

## Security Architecture

### Authentication
- JWT access tokens (30 min expiry)
- JWT refresh tokens (7 day expiry)
- Password hashing with bcrypt
- Optional 2FA via SMS/email

### Authorization
- Role-based access control (RBAC)
- Resource-level permissions
- API rate limiting

### Data Protection
- TLS/HTTPS for all communication
- Database encryption at rest
- Sensitive data (SSN, payment) encrypted
- Regular security audits

## Scalability Considerations

### Horizontal Scaling
- Stateless API servers
- Load balancer distribution
- Redis session storage
- Database read replicas

### Performance Optimization
- Database indexing on frequent queries
- Redis caching layer
- Background job processing
- Efficient geospatial queries with PostGIS

### Monitoring
- Application performance monitoring (APM)
- Error tracking (Sentry)
- Logging aggregation
- Database query performance

## AI/ML Architecture

### Matching System
```
Historical Data → Feature Engineering → Model Training → Scoring Service
                                              ↓
                                        Model Registry
                                              ↓
                                    Production Inference
```

### Chatbot Pipeline
```
User Message → Intent Classification → Entity Extraction → Response Generation
                                             ↓
                                      Knowledge Base (RAG)
                                             ↓
                                        LLM (GPT/Claude)
```

## Deployment Architecture

### Development
- Docker Compose for local development
- Hot reload for rapid iteration
- Local PostgreSQL + Redis containers

### Staging
- Cloud-hosted (AWS/GCP/Railway)
- Separate database instances
- Feature flag system for testing

### Production
- Multi-region deployment
- Auto-scaling groups
- Database backups and replication
- CDN for static assets
- Disaster recovery plan

## Technology Choices Rationale

### FastAPI
- High performance (async/await)
- Automatic validation and documentation
- Modern Python with type hints
- Growing ecosystem

### PostgreSQL + PostGIS
- Robust and reliable
- Excellent geospatial support
- ACID compliance
- Strong community

### Redis
- Fast in-memory storage
- Pub/sub for real-time features
- Versatile data structures
- Battle-tested

### Docker
- Consistent environments
- Easy deployment
- Microservices ready
- Developer productivity
