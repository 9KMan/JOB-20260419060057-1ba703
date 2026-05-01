# SPEC.md — Music/Booking SaaS Finish & Launch

## 1. Concept & Vision

A SaaS platform in the music/booking space, ~70% built, needing a full-stack engineer to finish core features, stabilize, launch, and continue ongoing development. Not a chatbot project — a real product with booking/scheduling workflows, AI-driven automation, and weekly sprint delivery. The product serves music industry clients with real booking and scheduling needs.

---

## 2. Product Scope

### Core Features to Complete
1. **User Authentication & Authorization** — Sign-up, login, role-based access (admin, performer, venue, attendee)
2. **Booking Management** — Create, approve, reject, and manage booking requests; calendar view; status tracking
3. **Scheduling System** — Time slot management; conflict detection; calendar integration
4. **Communication Workflow** — In-app messaging or notification system for booking status updates
5. **AI-Driven Automation** (key differentiator):
   - Parse booking inquiry inputs (natural language → structured data)
   - Automate routine confirmation/rejection workflows
   - Generate useful outputs (availability suggestions, conflict alerts, summary reports)
6. **Payment Integration** (Phase 2 post-launch)

### Existing Codebase (~70% built)
- Frontend: React/Next.js (framework confirmed)
- Backend: Node.js
- Database: Not specified — audit required
- Auth: Not specified — audit required
- Existing features: Unknown — code review required

---

## 3. Technical Architecture

### Stack
- **Frontend:** Next.js, React
- **Backend:** Node.js (Express or similar)
- **Database:** PostgreSQL recommended (need to confirm with client)
- **Auth:** NextAuth.js or similar
- **AI:** OpenAI API / Claude API for LLM features
- **Deployment:** Vercel (frontend) + Railway/Render (backend)
- **Scheduling:** Custom calendar or Cal.com integration
- **Notifications:** SendGrid or Resend for email

### Data Model (Draft)
```
Users: id, email, password_hash, role, name, created_at
Venues: id, user_id, name, address, capacity, amenities
Performers: id, user_id, genre, bio, availability
Bookings: id, venue_id, performer_id, requested_date, status, notes, created_at
Messages: id, booking_id, sender_id, content, created_at
AI_Parse_Logs: id, booking_id, input_text, parsed_data, created_at
```

### API Endpoints
```
POST   /api/auth/register
POST   /api/auth/login
GET    /api/users/me
GET    /api/venues
POST   /api/venues
GET    /api/performers
POST   /api/performers
GET    /api/bookings
POST   /api/bookings
PATCH  /api/bookings/:id
DELETE /api/bookings/:id
GET    /api/bookings/:id/messages
POST   /api/bookings/:id/messages
POST   /api/ai/parse-booking-inquiry
GET    /api/calendar/slots?date=
POST   /api/ai/suggest-availability
```

---

## 4. Build Phases

### Phase 1: Audit & Stabilization (Week 1)
- Clone existing codebase and run locally
- Audit current architecture, DB schema, auth system
- Identify broken/incomplete features
- Fix critical bugs blocking basic flows
- Set up CI/CD if missing

### Phase 2: Core Features (Weeks 2-4)
- Complete user auth flows
- Finish booking CRUD
- Implement scheduling system
- Build communication/notifications

### Phase 3: AI Features (Weeks 4-6)
- Integrate OpenAI/Claude API
- Build booking inquiry parser
- Automate confirmation workflows
- Add availability suggestions

### Phase 4: Launch Prep (Weeks 6-8)
- Testing (unit + E2E)
- Performance optimization
- Mobile responsiveness
- Launch checklist

### Phase 5: Ongoing (Post-launch)
- New features based on user feedback
- Payment integration
- Analytics dashboard

---

## 5. Key Assumptions & Open Questions

1. **Database stack** — Client has not specified PostgreSQL/MySQL/MongoDB. Must confirm.
2. **Existing codebase quality** — 70% built by unknown developer.接手 risk is HIGH. Must audit before estimating.
3. **Hosting** — Not specified. Recommend Vercel + Railway for simplicity.
4. **AI provider** — Client mentioned OpenAI/Claude. Recommend OpenAI GPT-4o for parsing, Claude for generation.
5. **Payment** — Phase 2. Stripe integration post-launch.
6. **Client timezone** — Gold Coast, Australia (AEST, UTC+10). Weekly sprints likely overlap with early morning EU/US time windows.

---

## 6. Risk Factors

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| 接手烂尾代码 (inherited broken code) | HIGH | HIGH | Day 1 audit, clear scope document from client |
| Missing DB/auth specs | MEDIUM | HIGH | Confirm in kickoff meeting |
| Client communication gaps (timezone) | MEDIUM | MEDIUM | Async-first, Loom video updates |
| AI feature scope creep | MEDIUM | MEDIUM | Strict MVP scope, defer complex features |
| 70% codebase may have security issues | MEDIUM | HIGH | Full security audit in Phase 1 |
