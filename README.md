# Gift Sharing App

A full-stack web + mobile PWA application for managing shared gift wishlists with friends and family, featuring passwordless authentication.

## Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.11+ with FastAPI |
| **ORM** | SQLModel (SQLAlchemy + Pydantic) |
| **Database** | SQLite (dev) / PostgreSQL (prod) |
| **Email** | Resend |
| **Frontend** | Vue.js 3 + Vite + TypeScript |
| **State** | Pinia |
| **i18n** | vue-i18n (ES/EN) |
| **PWA** | vite-plugin-pwa |

## Features

- 📧 **Passwordless Authentication** - Email OTP login
- 👥 **Groups** - Create and manage gift sharing groups
- 🎁 **Gifts** - Add immutable gift wishlists
- 🔒 **Privacy** - Gift owners never see who reserved their gifts
- 🔍 **Search Links** - Configurable store search buttons
- 🌐 **Multi-language** - Spanish and English support
- 📱 **PWA** - Installable as mobile app

## Quick Start

### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt

# Copy environment file
copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac

# Edit .env with your settings (optional for dev)

# Run server
uvicorn app.main:app --reload
```

Backend will be available at http://localhost:8000

API docs at http://localhost:8000/docs

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run dev server
npm run dev
```

Frontend will be available at http://localhost:5173

## Environment Variables

### Backend (.env)

```env
SECRET_KEY=your-secret-key-change-in-production
DATABASE_URL=sqlite+aiosqlite:///./gifts.db
RESEND_API_KEY=your-resend-api-key  # Optional for dev
EMAIL_FROM=noreply@yourdomain.com
FRONTEND_URL=http://localhost:5173
```

## API Endpoints

### Authentication
- `POST /api/auth/send-code` - Send OTP to email
- `POST /api/auth/verify-code` - Verify OTP and get token
- `GET /api/auth/me` - Get current user

### Groups
- `GET /api/groups` - List user's groups
- `POST /api/groups` - Create group
- `GET /api/groups/:id` - Get group detail
- `POST /api/groups/:id/join` - Request to join
- `POST /api/groups/:id/members/:userId/accept` - Accept member
- `POST /api/groups/:id/members/:userId/reject` - Reject member
- `DELETE /api/groups/:id/members/:userId` - Remove member
- `POST /api/groups/:id/close` - Close group

### Gifts
- `GET /api/groups/:id/gifts` - List gifts
- `POST /api/groups/:id/gifts` - Create gift
- `DELETE /api/gifts/:id` - Delete gift

### Reservations
- `POST /api/gifts/:id/reserve` - Reserve gift
- `DELETE /api/gifts/:id/reserve` - Unreserve gift
- `POST /api/gifts/:id/purchased` - Mark as purchased

## License

MIT
