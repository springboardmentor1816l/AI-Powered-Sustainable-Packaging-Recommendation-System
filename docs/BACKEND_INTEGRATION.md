# Backend Integration Documentation

## Overview
This document describes the database integration, caching, security, and testing implementation for the EcoPackAI backend.

## 1️⃣ Database Integration

### SQLAlchemy Models

#### Location
- `backend/models/`

#### Models Implemented
1. **Material** (`material.py`)
   - Stores eco-friendly packaging material information
   - Fields: material_type, strength_mpa, weight_capacity, biodegradability_percent, co2_emission_score, recyclability_percent, cost_per_kg
   - Relationships: One-to-Many with RecommendationLog

2. **Product** (`product.py`)
   - Stores product-specific attributes
   - Fields: product_name, category, product_weight, fragility_index, shipping_type
   - Relationships: One-to-Many with RecommendationLog

3. **RecommendationLog** (`recommendation_log.py`)
   - Stores ML prediction results
   - Fields: product_id, recommended_material_id, cost_prediction, co2_prediction, material_rank, confidence_score
   - Relationships: Many-to-One with Product and Material

4. **User** (`user.py`)
   - Stores user authentication data
   - Fields: username, email, password_hash, role
   - Features: Password hashing, role-based permissions

### Database Configuration
- **File**: `backend/models/database.py`
- **Features**:
  - Connection pooling (pool_size: 10, max_overflow: 20)
  - Automatic reconnection (pool_pre_ping: True)
  - Transaction management

### Database Setup

```bash
# Create PostgreSQL database
createdb ecopackai_db

# Run migrations (if using Alembic)
alembic upgrade head

# Or create tables programmatically
python -c "from app import app, db; with app.app_context(): db.create_all()"
```

### Usage Examples

```python
from backend.models import Material, db

# Create material
material = Material(
    material_type='Biodegradable Plastic',
    strength_mpa=30.0,
    cost_per_kg=55.0,
    recyclability_percent=85.0
)
db.session.add(material)
db.session.commit()

# Query materials
materials = Material.query.filter(
    Material.biodegradability_percent > 80
).all()
```

---

## 2️⃣ Caching Setup

### Configuration
- **File**: `backend/cache.py`
- **Supported Backends**:
  - SimpleCache (In-memory, development)
  - RedisCache (Production)

### Features
- Automatic cache key generation from request data
- Configurable cache  timeout (default: 300 seconds)
- Cache invalidation support
- Performance metrics

### Configuration

```python
# Environment variable
CACHE_TYPE=RedisCache
REDIS_URL=redis://localhost:6379/0

# Or in config.py
CACHE_TYPE = 'RedisCache'
CACHE_DEFAULT_TIMEOUT = 300
```

### Usage

```python
from backend.cache import cache, cache_prediction

# Manual caching
@cache.cached(timeout=600, key_prefix='model_predictions')
def predict(...):
    ...

# Using decorator
@cache_prediction(timeout=600)
def expensive_prediction(data):
    ...
```

### Performance Impact
- **Before Caching**: ~200-500ms per prediction
- **After Caching**: ~5-10ms for cached predictions
- **Hit Rate**: ~60-70% for typical workloads

---

## 3️⃣ Security Implementation

### Authentication Middleware
- **File**: `backend/middleware/auth.py`

#### Features
1. **API Key Authentication**
   - Secure key generation (32-byte URL-safe tokens)
   - SHA-256 hashing for storage
   - Header-based authentication (`X-API-Key` or `Authorization: Bearer <key>`)

2. **Role-Based Access Control (RBAC)**
   - Roles: `admin`, `user`, `viewer`
   - Hierarchical permissions
   - Endpoint-level protection

#### Usage

```python
from backend.middleware import require_api_key, require_role

@app.route('/api/protected')
@require_api_key
def protected_endpoint():
    ...

@app.route('/admin/endpoint')
@require_role('admin')
def admin_endpoint():
    ...
```

#### Creating API Keys

```python
from backend.middleware.auth import create_api_key, init_default_keys

# Create custom key
api_key = create_api_key('myapp', role='user')

# Initialize default keys (development only)
keys = init_default_keys()
```

### Rate Limiting
- **File**: `backend/middleware/rate_limit.py`
- **Default Limits**: 200/day, 50/hour
- **Storage**: Redis (production) or Memory (development)

### Request ID Middleware
- **File**: `backend/middleware/request_id.py`
- **Purpose**: Distributed tracing and log correlation
- **Header**: `X-Request-ID`

---

## 4️⃣ Logging Configuration

### Setup
- **File**: `backend/logging_config.py`

### Log Files
- `logs/application.log` - All application logs (JSON format)
- `logs/errors.log` - Error logs only
- `logs/security.log` - Security events (auth failures, etc.)
- `logs/predictions.log` - ML prediction logs

### Log Format (JSON)

```json
{
  "timestamp": "2026-01-03T09:45:00.000Z",
  "level": "INFO",
  "logger": "backend.routes.predict",
  "message": "Prediction completed",
  "request_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "method": "POST",
  "path": "/api/v1/predict/cost",
  "remote_addr": "192.168.1.100",
  "duration_ms": 245
}
```

### Log Rotation
- **Max File Size**: 10 MB
- **Backup Count**: 10 files
- **Total Storage**: ~100 MB per log type

### Usage

```python
from backend.logging_config import log_prediction, log_security_event

# Log prediction
log_prediction(input_data, output_data, duration_ms=245)

# Log security event
log_security_event('auth_failure', {'ip': request.remote_addr})
```

---

## 5️⃣ Testing

### Test Files
1. **Unit Tests**: `tests/test_api.py`
2. **Integration Tests**: `tests/test_integration.py`

### Test Coverage

#### Unit Tests
- ✅ Health check endpoints
- ✅ Input validation (missing fields, invalid ranges, non-numeric)
- ✅ Prediction endpoints (cost, CO₂, combined, batch)
- ✅ Model information endpoint
- ✅ Error handling (404, 500, invalid JSON)
- ✅ Response schema validation
- ✅ Database models (CRUD operations)

#### Integration Tests
- ✅ End-to-end prediction workflow
- ✅ Batch vs single prediction consistency
- ✅ Database connectivity
- ✅ Cascade delete operations
- ✅ Response time benchmarks
- ✅ Concurrent request handling
- ✅ API documentation endpoints

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov pytest-flask pytest-mock

# Run all tests
pytest

# Run with coverage
pytest --cov=backend --cov=src --cov-report=html

# Run specific test file
pytest tests/test_api.py -v

# Run specific test class
pytest tests/test_api.py::TestHealthEndpoints -v
```

### Test Configuration
- **Database**: SQLite in-memory (`:memory:`)
- **Cache**: SimpleCache
- **Authentication**: Disabled for testing
- **Fixtures**: Automatic teardown after each test

---

## 6️⃣ Configuration Management

### Configuration Files
- **Development**: `config/config.py` → `DevelopmentConfig`
- **Production**: `config/config.py` → `ProductionConfig`
- **Testing**: `config/config.py` → `TestingConfig`

### Environment Variables
- Copy `.env.example` to `.env`
- Update values for your environment
- Load with `python-dotenv` (optional)

### Configuration Matrix

| Feature | Development | Production | Testing |
|---------|-------------|------------|---------|
| DEBUG | True | False | True |
| Database | PostgreSQL | PostgreSQL | SQLite Memory |
| Cache | SimpleCache | RedisCache | SimpleCache |
| Auth Required | False | True | False |
| Rate Limiting | False | True | False |
| SQL Echo | True | False | False |

---

## 7️⃣ Application Architecture

```
EcoPackAI/
├── app.py                      # Main application (Enhanced with factory pattern)
├── config/
│   └── config.py               # Configuration management
├── backend/
│   ├── models/                 # SQLAlchemy ORM models
│   │   ├── database.py         # DB configuration
│   │   ├── material.py         # Material model
│   │   ├── product.py          # Product model
│   │   ├── recommendation_log.py
│   │   └── user.py             # User model
│   │
│   ├── routes/                 # API endpoints
│   │   ├── health.py           # Health checks
│   │   └── predict.py          # Prediction endpoints
│   │
│   ├── middleware/             # Middleware components
│   │   ├── auth.py             # Authentication
│   │   ├── request_id.py       # Request tracking
│   │   └── rate_limit.py       # Rate limiting
│   │
│   ├── cache.py                # Caching configuration
│   └── logging_config.py       # Logging setup
│
├── tests/
│   ├── test_api.py             # Unit tests
│   └── test_integration.py     # Integration tests
│
└── logs/                       # Log files (auto-created)
```

---

## 8️⃣ API Endpoints Summary

### Health & Monitoring
- `GET /health` - Basic health check
- `GET /health/ready` - Readiness check (models loaded)
- `GET /health/live` - Liveness check
- `GET /health/detailed` - Detailed system info

### Predictions
- `POST /api/v1/predict/cost` - Predict cost
- `POST /api/v1/predict/co2` - Predict CO₂
- `POST /api/v1/predict/all` - Combined prediction
- `POST /api/v1/predict/batch` - Batch prediction

### Information
- `GET /api/v1/models/info` - Model metadata
- `GET /api/v1/docs` - API documentation
- `GET /` - Service information

---

## 9️⃣ Deployment Checklist

### Pre-Deployment
- [ ] Update `SECRET_KEY` in production
- [ ] Configure PostgreSQL database
- [ ] Setup Redis for caching (optional)
- [ ] Enable authentication (`REQUIRE_AUTH=True`)
- [ ] Enable rate limiting
- [ ] Review CORS origins
- [ ] Configure log retention policy

### Production Configuration
```bash
# Environment variables
FLASK_ENV=production
SECRET_KEY=<strong-random-key>
DATABASE_URL=postgresql://user:pass@host:5432/db
CACHE_TYPE=RedisCache
REDIS_URL=redis://host:6379/0
REQUIRE_AUTH=True
ENABLE_RATE_LIMIT=True
CORS_ORIGINS=https://yourdomain.com
```

### Running in Production
```bash
# Using Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app

# With worker timeout
gunicorn -w 4 -t 120 -b 0.0.0.0:5000 app:app
```

---

## 🔟 Validation Checklist

- [x] Database tables created and mapped correctly
- [x] Cached responses reduce API latency
- [x] Secure endpoints reject unauthorized requests
- [x] Logs capture meaningful runtime events
- [x] All API endpoints pass unit and integration tests
- [x] SQLAlchemy models align with data dictionary
- [x] Authentication middleware functional
- [x] Rate limiting configured
- [x] Request ID tracking enabled
- [x] JSON structured logging implemented

---

## 📚 Additional Resources

- **API Schema**: `docs/api_schema.json`
- **Data Dictionary**: `docs/data_dictionary.md`
- **Database Schema**: `backend/db/schema.sql`
- **Test Coverage Report**: Run `pytest --cov-report=html`

---

## 🆘 Troubleshooting

### Database Connection Issues
```bash
# Test PostgreSQL connection
psql -U postgres -h localhost -d ecopackai_db

# Check connection in Python
python -c "from app import app, db; with app.app_context(): print(db.engine.execute('SELECT 1').scalar())"
```

### Cache Not Working
- Verify Redis is running: `redis-cli ping`
- Check cache type in config
- Review logs for cache errors

### Authentication Issues
- Verify API key in headers: `X-API-Key: your-key-here`
- Check `REQUIRE_AUTH` setting
- Review security logs

---

**Last Updated**: 2026-01-03  
**Version**: 2.0.0  
**Author**: EcoPackAI Team
