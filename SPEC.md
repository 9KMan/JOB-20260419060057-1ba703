# SPEC.md — MusicSync Pro: Finish & Launch (AI Integration)

**Job:** [Upwork Full Stack Product Engineer SaaS](https://www.upwork.com/jobs/Full-Stack-Product-Engineer-SaaS-Finish-Launch-Integration_~022045380585946756818)
**Budget:** $25–47/hr | **Duration:** 3–6 months initial + ongoing | **Type:** Contract-to-hire
**Client:** Music/Booking SaaS (Gold Coast, Australia)
**GitHub:** https://github.com/9KMan/JOB-20260419060057-1ba703

---

## 1. Project Overview

**Product:** Music/booking SaaS platform — ~70% built, needs to finish core features, stabilize, launch, then ongoing development.
**Goal:** Finish and launch MVP, then continue with weekly sprints with a Product Manager.
**Start:** Immediately
**Team:** You + Product Manager (async, weekly sprints)

---

## 2. Technical Stack

| Layer       | Technology |
|-------------|------------|
| Frontend    | Next.js (React), Tailwind CSS |
| Backend     | Node.js |
| Database    | PostgreSQL (primary), Redis (cache/sessions) |
| AI/ML       | OpenAI GPT-4, Claude API (practical integrations) |
| Auth        | NextAuth.js (Google, email) |
| Deployment  | Docker, Docker Compose |
| API         | REST + Webhooks |

---

## 3. Architecture

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   Next.js    │────▶│  Node.js API  │────▶│  PostgreSQL  │
│   Frontend   │◀────│   Server     │◀────│              │
└──────────────┘     └──────────────┘     └──────────────┘
                            │                    │
                            ▼                    ▼
                     ┌──────────────┐     ┌──────────────┐
                     │  AI Service  │     │  Redis       │
                     │  (GPT-4 /    │     │  Sessions /  │
                     │   Claude)    │     │  Cache       │
                     └──────────────┘     └──────────────┘
```

---

## 4. Core Features

### 4.1 Booking & Scheduling (Core)
- Multi-resource booking (musicians, venues, equipment)
- Calendar integration (Google Calendar, iCal)
- Time slot availability engine (no double-booking)
- Booking confirmation + reminder emails (Resend/SendGrid)
- Cancellation + rescheduling flow
- Recurring bookings

### 4.2 User Management
- Email/password + OAuth (Google)
- Role-based access: Admin, Organizer, Artist, Client
- User profiles with media (avatars, bios, portfolios)
- Team/organization support

### 4.3 Communication
- In-app messaging (real-time: Socket.io)
- Email notifications (booking updates, reminders)
- Webhook integrations for third-party tools

### 4.4 AI Features (Practical — Required)

#### AI Booking Assistant
- Natural language parsing: "Book jazz duo for Friday 7pm for 50 people" → structured booking
- AI-generated booking summaries for admins
- Smart availability suggestions

#### AI Workflow Automation
- Auto-generate client proposals from booking details
- AI-powered follow-up messages (personalized, not spam)
- Auto-tag and categorize bookings by type/mood/genre

#### AI Content Generation
- Generate event descriptions from booking inputs
- AI assistance for pricing suggestions based on market data
- Automated thank-you / review request messages post-event

### 4.5 Dashboard & Reporting
- Booking volume, revenue, trends
- Occupancy rate by resource/artist
- Cancellation rate
- AI-generated weekly summary reports

### 4.6 Payments (Post-Launch)
- Stripe integration (hourly or fixed weekly billing)
- Invoice generation
- Refund handling

---

## 5. Database Schema

### Users
```
id, email, password_hash, name, role, avatar_url,
phone, timezone, created_at, updated_at
```

### Organizations
```
id, name, owner_id, plan, settings_json, created_at
```

### Resources (Artists, Venues, Equipment)
```
id, org_id, name, type, description, hourly_rate,
availability_rules_json, media_urls[], active, created_at
```

### Bookings
```
id, org_id, resource_id, client_id, Booker_id,
title, start_time, end_time, status (pending/confirmed/cancelled),
party_size, notes, ai_summary, created_at, updated_at
```

### Messages
```
id, conversation_id, sender_id, content, read, created_at
```

### AI Interaction Logs
```
id, user_id, action, input_text, output_text, model,
tokens_used, cost_usd, created_at
```

---

## 6. API Endpoints

### Auth
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`
- `POST /api/auth/oauth/google`

### Bookings
- `GET /api/bookings` — List (filter by date, resource, status)
- `POST /api/bookings` — Create (with AI parsing)
- `GET /api/bookings/:id`
- `PUT /api/bookings/:id` — Update status, time, notes
- `DELETE /api/bookings/:id` — Cancel
- `POST /api/bookings/:id/ai-suggest` — AI availability suggestions

### Resources
- `GET /api/resources` — List org resources
- `POST /api/resources` — Create
- `PUT /api/resources/:id` — Update
- `DELETE /api/resources/:id`
- `GET /api/resources/:id/availability` — Available slots

### AI
- `POST /api/ai/parse-booking` — NL → structured booking
- `POST /api/ai/generate-proposal` — Booking → proposal draft
- `POST /api/ai/summarize` — Booking → AI summary
- `POST /api/ai/follow-up` — Generate follow-up message

### Messages
- `GET /api/messages` — List conversations
- `POST /api/messages` — Send message

### Admin
- `GET /api/admin/dashboard` — Stats (bookings, revenue, occupancy)
- `GET /api/admin/reports/weekly` — AI-generated weekly report

---

## 7. AI Implementation Details

### OpenAI GPT-4 — Booking Parser
```
Input: "Book the jazz quartet for our wedding reception on March 15, 7pm to 11pm, about 80 guests"
Output: { resource_type: "jazz-quartet", date: "2026-03-15", start: "19:00", end: "23:00", party_size: 80 }
```

### Claude — Workflow Automation
- Proposal generation: booking details → formatted proposal document
- Follow-up messages: personalized, context-aware, compliant

### Prompt Engineering
- System prompts define tone: professional, warm, concise
- All AI outputs are editable before sending
- Cost tracking per AI call

---

## 8. Deployment

### Docker Compose (Development)
```yaml
services:
  frontend: next.js dev server
  backend: node.js + Express
  postgres: PostgreSQL 15
  redis: Redis 7
  ai-service: Node.js + OpenAI SDK
```

### CI/CD (GitHub Actions)
1. Push to `main` → build + test (Jest + Playwright)
2. Run type-check (tsc)
3. Deploy to Railway / Render / Fly.io

### Environment Variables
```
DATABASE_URL, REDIS_URL, NEXTAUTH_SECRET,
GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET,
OPENAI_API_KEY, ANTHROPIC_API_KEY,
STRIPE_SECRET_KEY,
SENDGRID_API_KEY
```

---

## 9. Milestones (4–8 Week Launch Plan)

| Milestone | Deliverable | Week |
|-----------|-------------|------|
| M1 Stabilize | Fix critical bugs, audit existing code, document gaps | 1 |
| M2 Booking Flow | Finish booking flow end-to-end, payments | 2 |
| M3 AI Features | Integrate GPT-4 parser, Claude automation | 3 |
| M4 Communications | Messaging, email notifications, webhooks | 4 |
| M5 Dashboard | Reporting, AI weekly summaries | 5 |
| M6 Launch | Production deploy, Stripe billing, go-live | 6–8 |

---

## 10. Testing

| Type       | Tool         | Target |
|------------|--------------|--------|
| Unit       | Jest         | >80% backend |
| Integration| Supertest    | All API endpoints |
| E2E        | Playwright   | Booking flow, auth |
| AI         | Eval harness | Parsing accuracy >90% |

**Critical flows:**
1. Register → Create booking → Receive confirmation
2. NL booking input → AI parse → Structured booking
3. Cancel booking → Refund trigger → Email confirmation
4. Weekly report generation (AI)

---

## 11. Documentation

- [ ] `README.md` — Setup, architecture, local dev
- [ ] `docs/API.md` — OpenAPI spec
- [ ] `docs/AI_PROMPTS.md` — All AI prompt templates
- [ ] `docs/BOOKING_FLOW.md` — End-to-end user journey
- [ ] `docs/ONBOARDING.md` — PM handoff doc

---

## 12. Risk Factors

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| Existing codebase debt | High | Audit first, budget 20% extra time |
| AI cost overruns | Medium | Token budgets, cache common queries |
| Scope creep | High | Weekly PM sprint planning, hard cutoffs |
| Payment integration complexity | Medium | Stripe only post-launch, manual invoicing first |

---

## 13. Nice-to-Have (Post-Launch)

- Mobile app (React Native)
- Multi-currency billing
- Integration with Spotify/SoundCloud APIs
- Waitlist management
- AI booking recommendations ("Artists similar to X are available")
