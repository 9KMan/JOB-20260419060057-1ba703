# MusicSync Pro

AI-Powered Music & Booking SaaS Platform for artists, venues, and event organizers.

## Features

- **Smart Scheduling**: AI-optimized booking times with conflict detection
- **Artist Discovery**: Find and book the perfect artists for your venue
- **AI Assistant**: GPT-4 and Claude integration for generating event descriptions and marketing copy
- **Booking Management**: Complete booking lifecycle from request to completion
- **Event Management**: Create, publish, and manage events
- **User Roles**: Support for artists, venues, bookers, and admins

## Tech Stack

### Backend
- FastAPI (Python 3.11+)
- SQLAlchemy with PostgreSQL
- Pydantic for data validation
- JWT Authentication
- OpenAI & Anthropic API integration

### Frontend
- Next.js 14 (React)
- TypeScript
- Tailwind CSS
- Zustand for state management
- TanStack Query for data fetching

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 20+
- PostgreSQL 15+
- Docker & Docker Compose (optional)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Set environment variables:
```bash
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/musicsync"
export OPENAI_API_KEY="your-openai-api-key"
export ANTHROPIC_API_KEY="your-anthropic-api-key"
```

Run the backend:
```bash
uvicorn main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
```

Set environment variables:
```bash
export NEXT_PUBLIC_API_URL="http://localhost:8000/api"
```

Run the frontend:
```bash
npm run dev
```

### Docker Compose

```bash
docker-compose up --build
```

## API Endpoints

### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/token` - Login and get JWT token
- `GET /api/auth/me` - Get current user profile

### Bookings
- `POST /api/bookings/` - Create booking
- `GET /api/bookings/` - List all bookings
- `GET /api/bookings/{id}` - Get booking details
- `PUT /api/bookings/{id}` - Update booking
- `DELETE /api/bookings/{id}` - Cancel booking

### Events
- `POST /api/events/` - Create event
- `GET /api/events/` - List events
- `GET /api/events/{id}` - Get event details
- `PUT /api/events/{id}` - Update event
- `DELETE /api/events/{id}` - Delete event

### AI Assistant
- `POST /api/ai/chat` - Chat with AI
- `POST /api/ai/generate-event-description` - Generate event description
- `GET /api/ai/usage` - Get AI usage statistics

## Running Tests

```bash
cd backend
pytest
```

## License

MIT License - see LICENSE file for details.
