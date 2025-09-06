# CouponZen 🎫

CouponZen is a modern coupon management system built with FastAPI and SQLModel, designed to help users efficiently track and manage their coupons with smart reminders.

## Features 🚀

- 👤 User authentication via Google OAuth
- 🎫 Coupon management with public/private visibility
- ⏰ Smart reminder system
- 📧 Process coupons from various sources (email, messages, etc.)
- 🔍 Advanced search capabilities
- 🎯 Personalized user preferences
- 📱 RESTful API for easy integration

## Quick Start 🏃‍♂️

1. **Clone the repository**
   ```bash
   git clone https://github.com/aman-kumar29/CouponZen.git
   cd CouponZen
   ```

2. **Set up environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5432/couponzen
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CLIENT_SECRET=your_google_client_secret
   GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback
   JWT_SECRET_KEY=your_jwt_secret_key
   ```

4. **Start the server**
   ```bash
   ./start.sh
   ```
   The API will be available at `http://localhost:8000`

## Project Structure 📁

```
CouponZen/
├── app/
│   ├── api/
│   │   └── routes/      # API endpoints
│   ├── core/            # Core configurations
│   ├── models/          # Database models
│   ├── services/        # Business logic
│   └── main.py         # Application entry point
├── docs/              # Documentation
├── requirements.txt   # Dependencies
└── start.sh          # Startup script
```

## API Documentation 📚

- **Swagger UI**: Access interactive API documentation at `http://localhost:8000/docs`
- **ReDoc**: Alternative API documentation at `http://localhost:8000/redoc`
- **Detailed Documentation**: See [DOCUMENTATION.md](docs/DOCUMENTATION.md)

## Features Documentation 📖

### User Management
- Google OAuth integration
- User preferences and settings
- Role-based access control

### Coupon Management
- Create, read, update, and delete coupons
- Public/private visibility settings
- Expiry tracking
- Metadata support

### Reminder System
- Custom reminder scheduling
- Flexible notification messages
- Batch processing for notifications

### Inbound Processing
- Process coupons from various sources
- Status tracking and error handling
- Batch processing capabilities

## Contributing 🤝

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License.

## Support 💬

For support, please open an issue in the repository.
