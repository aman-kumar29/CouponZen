# CouponZen Documentation

## Project Overview
CouponZen is a coupon management system that helps users track, manage, and get reminders for their coupons. The system is built using FastAPI and SQLModel, with PostgreSQL as the database.

## Architecture

### Core Components
1. **Models** (`/app/models/`)
   - `User`: Handles user data, preferences, and authentication
   - `Coupon`: Manages coupon information and metadata
   - `Reminder`: Handles coupon expiry reminders
   - `InboundItem`: Processes incoming items (emails, messages, etc.)

### Services (`/app/services/`)
1. **User Service** (`user_service.py`)
   - User CRUD operations
   - Google OAuth integration
   - User preferences management
   - Role-based access control

2. **Coupon Service** (`coupon_service.py`)
   - Coupon CRUD operations
   - Visibility control (public/private)
   - Soft delete functionality
   - Metadata management

3. **Reminder Service** (`reminder_service.py`)
   - Reminder creation and management
   - Scheduled notifications
   - Custom message support
   - Batch processing for pending reminders

4. **Inbound Service** (`inbound_service.py`)
   - Process incoming items
   - Status tracking
   - Error handling
   - Batch processing capabilities

5. **Token Service** (`token_service.py`)
   - JWT token management
   - Access token generation
   - Refresh token handling

6. **Google OAuth Service** (`google_oauth.py`)
   - Google authentication integration
   - User profile retrieval
   - Token exchange

### API Routes (`/app/api/routes/`)
1. **Authentication** (`auth.py`)
   - Google OAuth endpoints
   - Token refresh
   - Session management

2. **Base Routes** (`base.py`)
   - Health check
   - API status
   - Basic information

## Database Schema

### User Table
```sql
- id: UUID (Primary Key)
- email: String (Unique)
- google_id: String (Optional)
- name: String
- picture: String (Optional)
- preferences: JSON
- role: Enum (USER, ADMIN)
- metadata: JSON
- is_deleted: Boolean
- created_at: DateTime
- updated_at: DateTime
```

### Coupon Table
```sql
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key)
- title: String
- description: String (Optional)
- expiry_date: DateTime (Optional)
- visibility: Enum (PUBLIC, PRIVATE)
- status: Enum (ACTIVE, USED, EXPIRED)
- metadata: JSON
- is_deleted: Boolean
- created_at: DateTime
- updated_at: DateTime
```

### Reminder Table
```sql
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key)
- coupon_id: UUID (Foreign Key)
- reminder_date: DateTime
- custom_message: String (Optional)
- is_sent: Boolean
- sent_at: DateTime (Optional)
- metadata: JSON
- is_deleted: Boolean
- created_at: DateTime
- updated_at: DateTime
```

### InboundItem Table
```sql
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key)
- content: String
- item_type: Enum
- status: Enum (PENDING, PROCESSED, ERROR)
- error_message: String (Optional)
- source: String (Optional)
- metadata: JSON
- is_deleted: Boolean
- created_at: DateTime
- updated_at: DateTime
```

## Authentication Flow

1. **Google OAuth Flow**
   ```
   User -> /auth/google -> Google Login -> /auth/google/callback -> JWT Tokens
   ```

2. **Token Refresh Flow**
   ```
   User -> /auth/refresh (with refresh_token) -> New Access Token
   ```

## Error Handling
- HTTP status codes for API responses
- Detailed error messages in development
- Sanitized error messages in production
- Error logging and tracking

## Future Extensions

### Vector Search Integration
The system is designed to support future vector search capabilities:
- Metadata fields in models can store vector embeddings
- `vectordb.py` placeholder for vector database operations
- Extensible service layer for adding vector search methods

### Batch Processing
- Support for bulk coupon imports
- Batch reminder processing
- Background task processing for inbound items

## Security Considerations

1. **Authentication**
   - JWT-based authentication
   - Secure token storage
   - Regular token rotation

2. **Data Protection**
   - Soft delete implementation
   - User data isolation
   - Role-based access control

3. **API Security**
   - Rate limiting
   - Input validation
   - CORS configuration

## Monitoring and Logging

1. **Application Logs**
   - Request/Response logging
   - Error tracking
   - Performance metrics

2. **System Health**
   - Health check endpoints
   - Database connection monitoring
   - Service status tracking
